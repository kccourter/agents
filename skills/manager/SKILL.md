---
name: manager
description: Coordinate an authorized feature or dependent task through bounded specialists, model/effort routing, verified evidence, and local completion. Use when delegation improves the outcome; keep simple fixes with one agent.
---

# Manager

Read the accepted outcome, effective project instructions, and current task
record. Reconcile revisions, owned dirty work, live processes, prerequisites,
resource limits, and pending decisions before dispatching. A concrete request
may already authorize implementation and normal local commits. Planning-only
requests do not authorize product changes.

Keep one current task/goal record. Write only the next ready assignments and
their dependency order; use existing plans/receipts instead of a parallel state
system. Record the human decisions actually needed. Ask about changes to outcome,
contracts, ownership, dependencies, resources, or external authority; continue
independent authorized work while waiting. Do not manufacture approval gates
to exercise the workflow.

For work needing resumable state or repeatable measurement, use
[task evidence guidance](references/task-evidence.md): one structured block in
the existing record, a generated brief, applicable validation receipts, and
outcome-linked usage including coordinator/setup costs. The installed helpers
are read-only unless explicitly asked to run a declared check. Do not require
this structure for an ordinary local fix or treat a brief as process liveness.

## Choose and dispatch

Use deterministic commands for exact checks. Delegate when independence,
specialization, or elapsed time benefits; do not instantiate every role for
every task. Installed profiles under `.codex/agents/` are the defaults:

- `workflow_researcher`: bounded discovery or independent acceptance probes.
- `workflow_implementer`: scoped implementation and immediate debugging.
- `workflow_debugger`: unresolved or conflicting evidence needing deeper diagnosis.
- `workflow_reviewer`: independent correctness and evidence review.
- `workflow_manager`: a fresh coordinator for a self-contained delegated outcome.

Read the selected profile's model, effort, and instructions. These are pilot
defaults, not universal model rankings. Verify the model/effort is available to
the current client. Do not silently substitute an unavailable model or describe
an inherited setting as an explicit selection. Existing root settings persist;
the manager profile does not change the current session or global defaults.

Use [references/dispatch.md](references/dispatch.md) for the current tool adapter
and runtime verification. For collaboration tools, select the profile's model
and reasoning effort explicitly with a fresh, bounded assignment. Include its
role instructions. A full-history fork inherits parent settings and cannot
serve as proof of model switching. Native custom-role overrides may take
precedence over spawn settings; verify rather than assume.

Each assignment supplies outcome, owned paths/worktree, base revision and
prerequisites, invariants, allowed actions and resource ceiling, checks, commit
ownership, escalation conditions, and expected evidence. Give relevant entry
points and uncertainty, not the whole conversation. Workers may investigate and
change tactics within the contract; expected files are starting points.

Keep one writer per worktree and one owner of its Git index. Parallelize
independent investigations or isolated writes, within actual available slots.
Workers return receipts; the manager alone edits shared task state. Do not
delegate more workers merely because slots exist.

## Escalation and acceptance

Diagnose missing evidence, environment failures, and bad inputs before spending
more reasoning. Keep straightforward corrections with the implementer. When a
well-chosen bounded probe leaves a consequential uncertainty, route the specific
question to the debugger or a stronger available setting. Supply the evidence
and what the new attempt will change; avoid identical blind retries. Respect
the existing budget and seek a decision only when that boundary is reached.

Before accepting a worker, inspect its actual change and evidence, verify the
execution settings when routing is being evaluated, and reconcile checks with
source/input/environment identities. A worker's success claim or requested
model setting alone is not verification. Required blocked checks remain gates.
Independent reviewers should receive the contract and submitted revision,
not instructions to confirm the implementer's conclusion.

Commit a reviewed coherent increment before dependent implementation or
integration. Consumers require reconciled producer commits, contracts, and
fixtures. Revalidate evidence invalidated by a correction, not every previously
passing check. Keep optional work outside acceptance.

Complete when required outcomes, checks, review findings, records, and authorized
commits are accounted for. Report actual settings, limitations, remaining human
decisions, and worktree state. Distill reusable findings and update the existing
index. A pilot demonstrates observed behavior; it does not establish cost or
quality superiority without a comparison.
