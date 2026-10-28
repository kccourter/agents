"""Observable receipt and recovery behavior; all commands are local fixtures."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import task_evidence as evidence


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        for name in ("source", "input", "environment"):
            (self.base / name).write_text(name)
        self.record = self.base / "task.md"
        self.script = Path(evidence.__file__)
        self.state = {
            "schema": "agent-task.v1", "task_id": "fixture", "outcome": "verify fixture",
            "constraints": ["local"], "resources": {"agents": 1}, "status": "active",
            "next_action": "review evidence", "checks": [{
                "id": "unit", "argv": [sys.executable, "-c", "print('verified')"],
                "cwd": ".", "watch": {"source": ["source"], "inputs": ["input"],
                                         "environment": ["environment"]},
                "env_keys": ["TASK_EVIDENCE_TEST_VALUE"], "timeout_seconds": 5,
                "receipt": None,
            }],
        }
        self.save()

    def save(self):
        self.record.write_text("# Fixture\n\n```agent-task\n" + json.dumps(self.state) + "\n```\n")

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.script), *map(str, args)],
                              capture_output=True, text=True, timeout=15, cwd=self.base)

    def capture(self, name="receipt.json"):
        self.save()
        proc = self.cli("run", self.record, "unit", "--output", name)
        result = json.loads(proc.stdout)
        self.assertNotIn("error", result, proc.stdout + proc.stderr)
        self.state["checks"][0]["receipt"] = {k: result[k] for k in ("path", "sha256")}
        self.save()
        return proc, result

    def summary(self):
        proc = self.cli("check", self.record)
        return proc, json.loads(proc.stdout)

    def check_status(self, expected):
        proc, report = self.summary()
        self.assertEqual(report["checks"][0]["status"], expected, report)
        self.assertEqual(proc.returncode == 0, expected == "passed", report)

    def test_real_success_receipt_logs_and_read_only_brief(self):
        proc, ref = self.capture()
        self.assertEqual(proc.returncode, 0, proc.stdout)
        receipt = json.loads(Path(ref["path"]).read_text())
        self.assertEqual(Path(receipt["logs"]["stdout"]["path"]).read_text(), "verified\n")
        self.assertEqual(receipt["before"], receipt["after"])
        self.assertIn("sha256", receipt["before"]["executable"])
        self.check_status("passed")
        self.state.update(status="accepted", processes=[{"pid": 1234}], dependencies=["decision"],
                          settings={"model": "recorded"}, findings=["done"])
        self.save()
        before = self.record.read_bytes()
        brief = self.cli("brief", self.record)
        self.assertEqual(brief.returncode, 0)
        self.assertIn("effective acceptance: true", brief.stdout)
        self.assertIn("liveness reconciliation", brief.stdout)
        self.assertIn("never resume automatically", brief.stdout)
        self.assertIn('"pid": 1234', brief.stdout)
        self.assertEqual(self.record.read_bytes(), before)
        parsed = json.loads(self.cli("brief", self.record, "--json").stdout)
        self.assertEqual(parsed["state"], self.state)

    def test_empty_checks_never_accept(self):
        self.state.update(checks=[], status="accepted")
        self.save()
        proc, report = self.summary()
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(report["status"], "no_checks")
        self.assertFalse(report["effective_acceptance"])

    def test_brief_and_check_never_execute(self):
        sentinel = self.base / "sentinel"
        self.state["checks"][0]["argv"] = [sys.executable, "-c", f"open({str(sentinel)!r}, 'w').write('ran')"]
        self.save()
        self.cli("brief", self.record)
        self.cli("check", self.record)
        self.assertFalse(sentinel.exists())

    def test_failure_keeps_output_and_never_passes(self):
        self.state["checks"][0]["argv"] = [sys.executable, "-c", "import sys; print('before failure'); print('failure', file=sys.stderr); sys.exit(7)"]
        proc, ref = self.capture()
        self.assertEqual(proc.returncode, 1)
        receipt = json.loads(Path(ref["path"]).read_text())
        self.assertEqual(receipt["returncode"], 7)
        self.assertIn("failure", Path(receipt["logs"]["stderr"]["path"]).read_text())
        self.check_status("failed")

    def test_timeout_keeps_evidence(self):
        self.state["checks"][0].update(argv=[sys.executable, "-c", "import time; print('starting', flush=True); time.sleep(10)"], timeout_seconds=0.15)
        proc, ref = self.capture()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(ref["status"], "timeout")
        self.assertEqual(Path(ref["path"] + ".stdout").read_text(), "starting\n")
        self.check_status("failed")

    def test_missing_executable_retains_receipt(self):
        self.state["checks"][0]["argv"] = ["task-evidence-fixture-does-not-exist"]
        proc, ref = self.capture()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable not found", Path(ref["path"] + ".stderr").read_text())
        self.check_status("failed")

    def test_missing_and_tampered_receipt(self):
        self.check_status("missing")
        _, ref = self.capture()
        receipt = Path(ref["path"])
        original = receipt.read_bytes()
        receipt.write_bytes(original + b" ")
        self.check_status("invalid")
        receipt.unlink()
        proc, report = self.summary()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(report["checks"][0]["status"], ("missing", "invalid"))

    def test_missing_and_tampered_logs(self):
        _, ref = self.capture()
        log = Path(ref["path"] + ".stdout")
        log.write_text("forged")
        self.check_status("invalid")
        log.unlink()
        self.assertNotEqual(self.summary()[0].returncode, 0)

    def test_source_input_environment_file_changes_stale(self):
        _, _ = self.capture()
        for name in ("source", "input", "environment"):
            with self.subTest(name=name):
                path = self.base / name
                old = path.read_bytes()
                path.write_text("changed")
                self.check_status("stale")
                path.write_bytes(old)
                self.check_status("passed")

    def test_environment_actual_value_is_hashed_and_unset_is_distinct(self):
        with patch.dict(os.environ, {"TASK_EVIDENCE_TEST_VALUE": "secret fixture"}):
            _, ref = self.capture()
            contents = Path(ref["path"]).read_text()
            self.assertNotIn("secret fixture", contents)
            self.check_status("passed")
            with patch.dict(os.environ, {"TASK_EVIDENCE_TEST_VALUE": "changed"}):
                self.check_status("stale")
        with patch.dict(os.environ):
            os.environ.pop("TASK_EVIDENCE_TEST_VALUE", None)
            self.check_status("stale")

    def test_watched_directory_tracks_additions_and_deletions(self):
        directory = self.base / "tree"
        directory.mkdir()
        (directory / "original").write_text("a")
        self.state["checks"][0]["watch"]["source"] = ["tree"]
        self.capture()
        (directory / "new").write_text("b")
        self.check_status("stale")
        (directory / "new").unlink()
        self.check_status("passed")
        (directory / "original").unlink()
        self.check_status("stale")

    def test_changed_source_during_successful_command_is_invalid(self):
        self.state["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; Path('source').write_text('modified')"]
        proc, ref = self.capture()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(ref["status"], "invalid")
        self.assertEqual(json.loads(Path(ref["path"]).read_text())["returncode"], 0)
        self.check_status("invalid")

    def test_admin_updates_do_not_stale_but_contract_changes_do(self):
        self.capture()
        self.state.update(status="accepted", next_action="another action", assignments=["new"],
                          decisions=["progress"], findings=["reviewed"], processes=[42],
                          resources={"agents": 1, "remaining_seconds": 100})
        self.save()
        self.check_status("passed")
        for key, value in (("outcome", "different"), ("constraints", ["different"])):
            with self.subTest(key=key):
                original = self.state[key]
                self.state[key] = value
                self.save()
                self.check_status("stale")
                self.state[key] = original
        self.state["checks"][0]["argv"].append("new argument")
        self.save()
        self.check_status("stale")
        self.assertIn("effective acceptance: false", self.cli("brief", self.record).stdout)

    def test_subset_check_does_not_accept_other_missing_check(self):
        self.capture()
        other = copy.deepcopy(self.state["checks"][0])
        other.update(id="other", receipt=None)
        self.state["checks"].append(other)
        self.state["status"] = "accepted"
        self.save()
        proc = self.cli("check", self.record, "unit")
        self.assertEqual(proc.returncode, 0)
        self.assertFalse(json.loads(proc.stdout)["effective_acceptance"])

    def test_output_is_exclusive_and_cannot_replace_watched_files(self):
        self.capture()
        prior = (self.base / "receipt.json").read_bytes()
        second = self.cli("run", self.record, "unit", "--output", "receipt.json")
        self.assertEqual(second.returncode, 2)
        self.assertEqual((self.base / "receipt.json").read_bytes(), prior)
        for output in ("source", "input", "environment"):
            original = (self.base / output).read_bytes()
            self.assertEqual(self.cli("run", self.record, "unit", "--output", output).returncode, 2)
            self.assertEqual((self.base / output).read_bytes(), original)
        (self.base / "blocked.json.stdout").write_text("retain")
        result = self.cli("run", self.record, "unit", "--output", "blocked.json")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / "blocked.json").exists())

    def test_output_inside_watched_tree_rejected(self):
        (self.base / "tree").mkdir()
        self.state["checks"][0]["watch"]["source"] = ["tree"]
        self.save()
        self.assertEqual(self.cli("run", self.record, "unit", "--output", "tree/receipt").returncode, 2)
        self.assertFalse((self.base / "tree/receipt").exists())

    def test_symlinks_ancestor_nested_and_dotdot_rejected(self):
        (self.base / "alias").symlink_to(self.base, target_is_directory=True)
        (self.base / "tree").mkdir()
        (self.base / "tree/link").symlink_to(self.base / "source")
        for selected in ("alias/source", "tree", "alias/../source"):
            with self.subTest(selected=selected):
                self.state["checks"][0]["watch"]["source"] = [selected]
                self.save()
                proc = self.cli("run", self.record, "unit", "--output", "receipt")
                self.assertEqual(proc.returncode, 2, proc.stdout)
                self.assertIn("symlink", proc.stdout)
        self.state["checks"][0]["watch"]["source"] = ["source"]
        self.save()
        proc = self.cli("run", self.record, "unit", "--output", "alias/receipt")
        self.assertEqual(proc.returncode, 2)

    def test_missing_watched_file_and_special_file_rejected(self):
        self.state["checks"][0]["watch"]["inputs"] = ["missing"]
        self.save()
        self.assertEqual(self.cli("run", self.record, "unit", "--output", "receipt").returncode, 2)
        os.mkfifo(self.base / "fifo")
        self.state["checks"][0]["watch"]["inputs"] = ["fifo"]
        self.save()
        proc = self.cli("run", self.record, "unit", "--output", "receipt")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unsupported file type", proc.stdout)

    def test_executable_bytes_change_stales(self):
        executable = self.base / "runner"
        executable.write_text("#!/bin/sh\nprintf 'fixture\\n'\n")
        executable.chmod(0o700)
        self.state["checks"][0]["argv"] = [str(executable)]
        self.capture()
        executable.write_text("#!/bin/sh\nprintf 'changed\\n'\n")
        self.check_status("stale")

    def test_explicit_cli_output_is_caller_relative(self):
        caller = self.base / "caller"
        caller.mkdir()
        proc = subprocess.run([sys.executable, str(self.script), "run", str(self.record),
                               "unit", "--output", "caller-receipt.json"],
                              capture_output=True, text=True, timeout=15, cwd=caller)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertEqual(json.loads(proc.stdout)["path"], str(caller / "caller-receipt.json"))
        self.assertFalse((self.base / "caller-receipt.json").exists())

    def test_core_parser_rejects_ambiguous_and_nonfinite_state(self):
        original = self.record.read_text()
        for text in (original + original, original + "```agent-task\n",
                     original.replace('"task_id": "fixture"', '"task_id": "fixture", "task_id": "duplicate"'),
                     original.replace('"agents": 1', '"agents": NaN'),
                     original.replace('"agents": 1', '"agents": Infinity'),
                     original.replace('"agents": 1', '"agents": -Infinity')):
            with self.subTest(text=text):
                self.record.write_text(text)
                proc = self.cli("brief", self.record)
                self.assertEqual(proc.returncode, 2, proc.stdout)
                self.assertEqual(json.loads(proc.stdout)["status"], "error")

    def test_malformed_records_and_checks(self):
        invalids = []
        for change in ({"watch": {"source": []}}, {"argv": "echo bad"},
                       {"timeout_seconds": True}, {"env_keys": ["A", "A"]},
                       {"receipt": {"path": "x", "sha256": "bad"}}):
            state = copy.deepcopy(self.state)
            state["checks"][0].update(change)
            invalids.append(state)
        state = copy.deepcopy(self.state)
        state["checks"].append(copy.deepcopy(state["checks"][0]))
        invalids.append(state)
        invalids.extend(({"schema": "bad"}, {**self.state, "checks": {}}))
        for state in invalids:
            with self.subTest(state=state):
                self.state = state
                self.save()
                proc = self.cli("check", self.record)
                self.assertEqual(proc.returncode, 2, proc.stdout)
                self.assertEqual(json.loads(proc.stdout)["status"], "error")
        self.record.write_text('```agent-task\n{"schema":"agent-task.v1", "schema":"agent-task.v1"}\n```\n')
        self.assertEqual(self.cli("brief", self.record).returncode, 2)
        self.record.write_text("no canonical fence")
        self.assertEqual(self.cli("brief", self.record).returncode, 2)


if __name__ == "__main__":
    unittest.main()
