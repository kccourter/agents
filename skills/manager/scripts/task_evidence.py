#!/usr/bin/env python3
"""Read task context and capture/check explicit, locally reviewed validation.

The record is trusted authority, not a permission boundary. Only ``run`` executes
commands; neither brief nor check dispatches or edits the canonical record.
Watched paths/cwd/output paths reject symlink traversal. Executable PATH aliases
are resolved to their actual target bytes and checked again after execution.
Explicit watch scope and before/after snapshots do not qualify unwatched state
or detect a change that is completely reverted between the two snapshots.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import signal
import stat
import subprocess
import sys
import time

from task_record import load_record, resolve_path, unique_object

WATCH_KEYS = ("source", "inputs", "environment")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest_file(path):
    result = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def absolute(base, value):
    raw = resolve_path(base, value)
    # Inspect lexical ancestors before normalizing '..', which can otherwise hide
    # a symlink traversal. Missing ancestors are diagnosed by safe_path later.
    for parent in raw.parents:
        if parent.is_symlink():
            raise ValueError(f"symlink path is unsupported: {parent}")
    return Path(os.path.abspath(raw))


def safe_path(path, *, missing_leaf=False):
    """Inspect rather than resolve: resolving first hides symlink ancestors."""
    path = Path(path)
    for part in reversed((path, *path.parents)):
        try:
            mode = part.lstat().st_mode
        except FileNotFoundError:
            if missing_leaf and part == path:
                return path
            raise ValueError(f"missing path: {part}") from None
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink path is unsupported: {part}")
        if part != path and not stat.S_ISDIR(mode):
            raise ValueError(f"non-directory ancestor: {part}")
    return path


def inspect_tree(path):
    safe_path(path)
    entries = []

    def visit(item, relative):
        mode = item.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink path is unsupported: {item}")
        if stat.S_ISREG(mode):
            entries.append({"path": relative, "type": "file", "sha256": digest_file(item),
                            "mode": stat.S_IMODE(mode)})
        elif stat.S_ISDIR(mode):
            entries.append({"path": relative, "type": "directory"})
            for child in sorted(item.iterdir()):
                visit(child, str(Path(relative) / child.name) if relative != "." else child.name)
        else:
            raise ValueError(f"unsupported file type: {item}")

    visit(path, ".")
    return {"path": str(path), "entries": entries}


def validate_checks(state):
    checks = state.get("checks", [])
    seen = set()
    required = {"id", "argv", "cwd", "watch", "env_keys", "timeout_seconds", "receipt"}
    for check in checks:
        if not isinstance(check, dict) or set(check) != required:
            raise ValueError("each check must have exactly id, argv, cwd, watch, env_keys, timeout_seconds, receipt")
        name = check["id"]
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("check ids must be nonempty and unique")
        seen.add(name)
        argv = check["argv"]
        if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and "\0" not in x for x in argv) or not argv[0]:
            raise ValueError(f"{name}: argv must be a nonempty string array with an executable")
        if not isinstance(check["cwd"], str) or not check["cwd"]:
            raise ValueError(f"{name}: cwd must be a path")
        watch = check["watch"]
        if not isinstance(watch, dict) or set(watch) != set(WATCH_KEYS):
            raise ValueError(f"{name}: watch requires source, inputs, environment")
        for key in WATCH_KEYS:
            if not isinstance(watch[key], list) or not all(isinstance(p, str) and p for p in watch[key]):
                raise ValueError(f"{name}: watch.{key} must contain paths")
        if not watch["source"]:
            raise ValueError(f"{name}: watch.source must not be empty")
        env_keys = check["env_keys"]
        if not isinstance(env_keys, list) or not all(isinstance(k, str) and k and "=" not in k and "\0" not in k for k in env_keys) or len(set(env_keys)) != len(env_keys):
            raise ValueError(f"{name}: env_keys must be unique environment names")
        timeout = check["timeout_seconds"]
        if isinstance(timeout, bool) or not isinstance(timeout, (float, int)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError(f"{name}: timeout_seconds must be positive and finite")
        receipt = check["receipt"]
        if receipt is not None and (not isinstance(receipt, dict) or set(receipt) != {"path", "sha256"} or not isinstance(receipt["path"], str) or not receipt["path"] or not isinstance(receipt["sha256"], str) or not DIGEST.fullmatch(receipt["sha256"])):
            raise ValueError(f"{name}: receipt must be null or a path/sha256 object")
    return checks


def definition(check):
    return {k: v for k, v in check.items() if k != "receipt"}


def contract(state):
    return {k: state.get(k, [] if k == "constraints" else {}) for k in
            ("task_id", "outcome", "constraints")}


def executable(argv0, cwd, env):
    if os.sep in argv0:
        candidates = [Path(os.path.abspath(resolve_path(cwd, argv0)))]
    else:
        candidates = [Path(os.path.abspath(resolve_path(cwd, part or "."))) / argv0
                      for part in env.get("PATH", os.defpath).split(os.pathsep)]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            # PATH aliases (e.g. python3 -> python3.12) bind the actual bytes.
            target = candidate.resolve(strict=True)
            safe_path(target)
            return {"path": str(target), "sha256": digest_file(target)}
    return None


def snapshot(check, base, env):
    cwd = safe_path(absolute(base, check["cwd"]))
    if not cwd.is_dir():
        raise ValueError(f"cwd is not a directory: {cwd}")
    runtime_path = Path(sys.executable).resolve(strict=True)
    safe_path(runtime_path)
    return {
        "cwd": str(cwd),
        "watch": {key: [inspect_tree(absolute(base, value)) for value in check["watch"][key]]
                  for key in WATCH_KEYS},
        "environment": {key: {"present": key in env,
                               "sha256": hashlib.sha256(env[key].encode()).hexdigest() if key in env else None}
                        for key in sorted(check["env_keys"])},
        "executable": executable(check["argv"][0], cwd, env),
        "runtime": {"python": platform.python_version(), "platform": platform.platform(),
                    "executable": str(runtime_path), "sha256": digest_file(runtime_path)},
    }


def validate_destinations(paths, identity):
    watched = [tree for group in identity["watch"].values() for tree in group]
    selected_files = {identity["runtime"]["executable"]}
    if identity["executable"]:
        selected_files.add(identity["executable"]["path"])
    for path in paths:
        safe_path(path, missing_leaf=True)
        if path.exists():
            raise ValueError(f"output already exists: {path}")
        if str(path) in selected_files:
            raise ValueError(f"output collides with selected executable: {path}")
        for tree in watched:
            root = Path(tree["path"])
            if path == root or (tree["entries"][0]["type"] == "directory" and root in path.parents):
                raise ValueError(f"output overlaps watched path: {path}")


def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def exclusive(path):
    return os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600), "wb")


def run_check(state, base, check, output):
    # Reject non-JSON contract values (e.g. NaN) before any execution/output.
    encoded(contract(state))
    encoded(definition(check))
    env = dict(os.environ)
    before = snapshot(check, base, env)
    output = absolute(Path.cwd(), output)
    stdout_path, stderr_path = Path(str(output) + ".stdout"), Path(str(output) + ".stderr")
    validate_destinations([output, stdout_path, stderr_path], before)
    # Reserve all outputs exclusively before dispatch. Never overwrite even on error.
    created = []
    try:
        receipt_stream = exclusive(output)
        created.append((output, receipt_stream))
        stdout = exclusive(stdout_path)
        created.append((stdout_path, stdout))
        stderr = exclusive(stderr_path)
        created.append((stderr_path, stderr))
    except OSError:
        for path, stream in created:
            stream.close()
            path.unlink()
        raise
    started, start = timestamp(), time.monotonic()
    status, returncode, error = "failed", None, None
    try:
        try:
            if before["executable"] is None:
                raise FileNotFoundError(f"executable not found: {check['argv'][0]}")
            proc = subprocess.Popen(check["argv"], executable=before["executable"]["path"],
                                    cwd=before["cwd"], env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                returncode = proc.wait(timeout=check["timeout_seconds"])
                status = "passed" if returncode == 0 else "failed"
            except subprocess.TimeoutExpired:
                if os.name == "posix":
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    proc.kill()
                proc.wait()
                returncode, status = proc.returncode, "timeout"
        except OSError as exc:
            error = f"{type(exc).__name__}: {exc}"
            stderr.write((error + "\n").encode())
    finally:
        stdout.close()
        stderr.close()
    try:
        after = snapshot(check, base, dict(os.environ))
        if before != after:
            status = "invalid"
            error = "selected evidence changed during execution"
    except (OSError, ValueError) as exc:
        after, status, error = None, "invalid", f"post-run snapshot failed: {exc}"
    receipt = {"schema": "agent-check-receipt.v1", "task_contract": contract(state),
               "check": definition(check), "started_at": started, "finished_at": timestamp(),
               "elapsed_seconds": time.monotonic() - start, "status": status,
               "returncode": returncode, "error": error, "before": before, "after": after,
               "logs": {key: {"path": str(path), "sha256": digest_file(path)}
                        for key, path in (("stdout", stdout_path), ("stderr", stderr_path))}}
    with receipt_stream:
        receipt_stream.write(encoded(receipt) + b"\n")
    return {"path": str(output), "sha256": digest_file(output), "status": status}


def check_one(state, base, check):
    result = {"id": check["id"], "status": "invalid", "reason": ""}
    reference = check["receipt"]
    if reference is None:
        return {**result, "status": "missing", "reason": "no receipt reference"}
    try:
        path = safe_path(absolute(base, reference["path"]))
        if not path.is_file():
            raise ValueError("receipt is not a regular file")
        if digest_file(path) != reference["sha256"]:
            raise ValueError("receipt digest mismatch")
        receipt = json.loads(path.read_text(), object_pairs_hook=unique_object)
        if receipt.get("schema") != "agent-check-receipt.v1":
            raise ValueError("unsupported receipt schema")
        for key in ("stdout", "stderr"):
            log = receipt["logs"][key]
            log_path = safe_path(absolute(path.parent, log["path"]))
            if not log_path.is_file() or digest_file(log_path) != log["sha256"]:
                raise ValueError(f"{key} log digest mismatch")
        if receipt["task_contract"] != contract(state) or receipt["check"] != definition(check):
            return {**result, "status": "stale", "reason": "task contract or check definition changed"}
        if receipt["status"] != "passed" or receipt["returncode"] != 0:
            status = "invalid" if receipt["status"] == "invalid" else "failed"
            return {**result, "status": status, "reason": f"recorded check status: {receipt['status']}"}
        if receipt["before"] != receipt["after"]:
            raise ValueError("selected evidence changed during execution")
        current = snapshot(check, base, dict(os.environ))
        if current != receipt["after"]:
            return {**result, "status": "stale", "reason": "selected evidence identity changed"}
        return {**result, "status": "passed", "reason": "receipt and selected evidence verified"}
    except FileNotFoundError as exc:
        return {**result, "status": "missing", "reason": str(exc)}
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return {**result, "reason": str(exc)}


def evidence_summary(state, base, check_id=None):
    checks = validate_checks(state)
    if check_id is not None and not any(c["id"] == check_id for c in checks):
        raise ValueError(f"unknown check id: {check_id}")
    all_results = [check_one(state, base, check) for check in checks]
    results = [r for r in all_results if check_id is None or r["id"] == check_id]
    valid = bool(results) and all(r["status"] == "passed" for r in results)
    task_valid = bool(all_results) and all(r["status"] == "passed" for r in all_results)
    return {"status": "passed" if valid else ("no_checks" if not results else "not_accepted"),
            "evidence_valid": valid, "effective_acceptance": state["status"] == "accepted" and task_valid,
            "checks": results}


def brief(state, summary):
    lines = [f"Task {state['task_id']} — recorded status: {state['status']}",
             f"Outcome: {state['outcome']}",
             f"Evidence: {summary['status']}; effective acceptance: {str(summary['effective_acceptance']).lower()}"]
    for key in ("phase", "constraints", "resources", "repositories", "revisions", "owned_changes",
                "assignments", "dependencies", "settings", "decisions", "processes", "findings"):
        if key in state:
            lines.append(f"{key}: {json.dumps(state[key], ensure_ascii=False, sort_keys=True)}")
    lines.append("Recorded process IDs require liveness reconciliation; never resume automatically.")
    for result in summary["checks"]:
        lines.append(f"Check {result['id']}: {result['status']} ({result['reason']})")
    lines.append(f"Next action: {state['next_action']}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("brief")
    show.add_argument("record")
    show.add_argument("--json", action="store_true")
    run = sub.add_parser("run")
    run.add_argument("record")
    run.add_argument("check_id")
    run.add_argument("--output", required=True,
                     help="new receipt path, relative to the caller's current directory; parents must exist")
    verify = sub.add_parser("check")
    verify.add_argument("record")
    verify.add_argument("check_id", nargs="?")
    args = parser.parse_args(argv)
    try:
        state, base = load_record(args.record)
        checks = validate_checks(state)
        if args.command == "run":
            check = next((c for c in checks if c["id"] == args.check_id), None)
            if check is None:
                raise ValueError(f"unknown check id: {args.check_id}")
            result = run_check(state, base, check, args.output)
            print(json.dumps(result, sort_keys=True))
            return 0 if result["status"] == "passed" else 1
        summary = evidence_summary(state, base, getattr(args, "check_id", None))
        if args.command == "brief":
            print(json.dumps({"state": state, "evidence": summary}, sort_keys=True) if args.json else brief(state, summary))
            return 0
        print(json.dumps(summary, sort_keys=True))
        return 0 if summary["evidence_valid"] else 1
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
