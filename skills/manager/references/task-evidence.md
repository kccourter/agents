# Task state, briefs, receipts, and usage

Use these helpers when a task needs durable recovery or repeatable measurement.
An ordinary local fix can keep its existing short receipt. Python 3.10+ and the
standard library suffice; no service, database, or project imports are needed.

Keep exactly one `agent-task` JSON fence in the existing goal README or task
record. The coordinator owns updates. Other documents link there. A brief is
generated from that state and is never a second status document. Paths in state
are relative to its Markdown file, or explicit absolute/`~` paths. Generated
receipts and logs normally belong in the project's ignored artifact directory.

Minimal state (add the fields that make this task recoverable):

```agent-task
{
  "schema": "agent-task.v1",
  "task_id": "feature-example",
  "outcome": "Approved observable behavior and acceptance boundary.",
  "status": "active",
  "next_action": "Inspect current evidence, then perform the next ready assignment.",
  "constraints": ["Preserve the agreed contract and unrelated work."],
  "resources": {"remaining": "Bounded local checks; no external compute."},
  "decisions": [],
  "repositories": [{"path": "../..", "revision": "recorded full commit", "owned_changes": []}],
  "assignments": [],
  "processes": [],
  "findings": [],
  "checks": []
}
```

Status is `planned`, `active`, `blocked`, or `accepted`. Assignments record the
agent/role, dependencies, owned paths, observed model/effort, progress, and
remaining allowance. Processes record run/session IDs, owner, and last observed
state. Pending decisions and unresolved findings stay visible. Keep details in
linked evidence instead of copying logs into the state. The helpers validate
the machine-consumed fields; they do not judge prose, authorization, or whether
all necessary checks/resources were declared.

## Resume and validate

Use the installed skill's actual location, normally:

```sh
python3 ~/.codex/skills/manager/scripts/task_evidence.py brief path/to/record.md
python3 ~/.codex/skills/manager/scripts/task_evidence.py check path/to/record.md
```

`brief --json` is available for structured consumers. Briefs include recorded
state and current check applicability. Reconcile Git HEAD/dirty work, dependency
commits, and process liveness before dispatch; recorded identifiers are not
proof that a process is still running or stopped. These read-only commands do
not resume processes, issue assignments, or rerun checks. A stale check requires
investigation, not an automatic retry or new experiment reservation.

Declare an authorized check in `checks`:

```json
{
  "id": "unit",
  "argv": ["python3", "-B", "-m", "unittest", "discover", "-s", "tests"],
  "cwd": "../..",
  "watch": {
    "source": ["../../src", "../../tests"],
    "inputs": ["../../fixtures/example.json"],
    "environment": ["../../requirements.lock"]
  },
  "env_keys": ["PYTHONPATH"],
  "timeout_seconds": 60,
  "receipt": null
}
```

All three watch lists are required; inputs/environment can be empty. At least
one source path is required. Directories include file additions/deletions;
choose a narrow relevant tree and keep generated outputs elsewhere. Symlinks
and special file types in watched paths are rejected. The resolved executable
is bound separately. Selected environment variable values are hashed, not
printed; hashes are evidence identities, not a secret store. Declare relevant
environment/config/fixture inputs explicitly. An unlisted dependency is outside
the check's coverage. Whole-repository revisions are not implicit freshness
gates: use an existing commit-set validator and watch its exact input when
revisions are part of acceptance.

```sh
python3 ~/.codex/skills/manager/scripts/task_evidence.py run path/to/record.md unit --output path/to/artifacts/unit-001.json
```

This executes the explicit argv without a shell, with a timeout, and retains
stdout/stderr beside a new receipt. It never overwrites an existing receipt or
edits the task state. Add the returned `{path, sha256}` to that check's `receipt`
field only after inspecting the result. Preserve failed attempts; choose a new
output name on retry. Command execution still requires the task's existing
authorization. A declaration is not an approval or a sandbox.

`check` verifies receipt and output digests, successful execution, stable inputs
during capture, and current contract/source/input/environment/executable
identities. A failed, timed-out, missing, tampered, or stale check cannot pass.
Changing task outcome, constraints, or check definition invalidates evidence;
changing administrative progress/next-action fields does not. The caller's
Python/platform identity is included. External mutable state, adversarial
races, and undeclared environment are not attested. Watch existing container
receipts or immutable image/environment manifests when those identities matter.

This is evidence applicability, not a replacement for domain validators or
independent review. Receipt hashes detect accidental alteration; a coordinator
can deliberately edit both a receipt and its digest, so this is not a signed
security attestation. Keep receipt/log payloads retrievable; references alone
are insufficient. No checks means no automated acceptance evidence.

## Measure the accepted task

Add `usage` to the same task state:

```json
{
  "root_turn_ids": ["exact authorized turn id"],
  "sources": [
    {"path": "~/.codex/sessions/date/root-rollout.jsonl", "label": "coordinator"},
    {"path": "~/.codex/sessions/date/child-rollout.jsonl", "label": "worker"}
  ],
  "scope": "Coordinator, setup and all declared workers for this accepted task.",
  "outcome": {
    "status": "accepted",
    "quality": "Acceptance checks and independent review recorded in linked evidence.",
    "rework": null,
    "acceptance_refs": ["record.md"]
  },
  "started_at": "2026-01-01T10:00:00Z",
  "accepted_at": "2026-01-01T10:05:00Z"
}
```

```sh
python3 ~/.codex/skills/manager/scripts/usage_report.py path/to/record.md --output path/to/artifacts/usage-001.json
```

Select explicit rollout paths and root-turn IDs. The root thread often contains
unrelated tasks: never attribute its entire history to one task. Include setup,
coordinator, workers, retries and review in a whole-task comparison; label them
so overhead is visible. Sources are declared coverage, not proof that no unseen
descendant exists. The current root's open turn produces an incomplete snapshot;
finalize after that turn ends. Do not manufacture completion to obtain totals.

The report sums per-response usage, deduplicates response IDs, and joins observed
turn model/effort. It ignores cumulative counters. Cached input is a subset of
input and reasoning output is a subset of output. Neither is added twice.
Missing context, counters, completion, sources or selected turns, malformed or
partial records, and conflicting duplicates prevent complete evidence. Runtime
settings describe the observed client path, not independent backend identity.

When source ordinals exist, gaps, reordering, or mixed missing ordinals make the
snapshot incomplete; exact replayed records are deduplicated. Sources without
ordinals explicitly report continuity unavailable. Start/usage/completion order
is checked for observed selected turns. These checks cannot detect an omitted
event that leaves no observable discontinuity or an undeclared source.

Operator-supplied acceptance/quality/rework remains explicitly separate from
measured tokens. Null means unknown. Task elapsed time uses supplied start and
acceptance timestamps (including human wait unless separately accounted for).
Selected response span is a narrower observation; parallel spans are not added
into task latency. Dollars remain null: token counts alone are not billing.

Compare reports with equivalent task boundaries, acceptance quality, coverage,
and source/environment conditions. Report rework and failures alongside tokens
and elapsed time. Changing scope or excluding the coordinator cannot establish
savings. The JSON supports later aggregation without another tracking system;
repeat representative tasks before changing default model/effort policy.

For helper changes, run the focused tests with the scripts directory on
`PYTHONPATH`, for example:

```sh
PYTHONPATH="$HOME/.codex/skills/manager/scripts" python3 -B -m unittest discover -s "$HOME/.codex/skills/manager/tests"
```
