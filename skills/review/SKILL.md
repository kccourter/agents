---
name: review
description: Review a completed local task or increment for correctness, scope, evidence, and affected documentation. Prepare PR artifacts when requested; use a deeper independent audit only when requested or warranted by consequential behavior.
---

# Review

Compare the actual diff and behavior with the accepted request or implementation
contract, relevant repository instructions, and validation evidence. Confirm the
outcome, invariants, ownership boundaries, and compatibility. Review maintenance
and local fixes proportionally; do not require goal documentation they do not
need.

Check meaningful behavior and failure modes, test adequacy, affected docs, and
unnecessary complexity. Add or fix regression coverage when needed to satisfy
the authorized outcome. Correct within-scope defects when the task authorizes
fixes; a review-only request returns findings without implementation.

For consequential numerical, contract, concurrency, authentication, or
integration behavior, independent scrutiny may be warranted. Use a separately
available audit capability when appropriate; its installation is not assumed.
Give an independent reviewer requirements, revisions, environment, and evidence,
and let them trace the behavior before relying on the implementer's explanation.

Reconcile commands/results with the actual source, environment, and inputs.
Re-run checks when changes or unresolved concerns invalidate evidence; do not
repeat passed checks without reason. Required checks that failed or were not
run remain limitations, not a passing gate merely because they were recorded.
Separate completed scope, unresolved defects, and optional follow-up work.

Keep findings and disposition in the existing task or record. If the adopted
workflow authorizes the local implementation commit, finish it after review
passes unless the user reserves commits; report the commit/worktree state.
Review does not introduce a new approval gate for an already authorized outcome.

Prepare PR notes when requested using the project's template or
[templates/pr-notes.md](templates/pr-notes.md). Follow user authorization and
project policy for remote PR creation, pushing, and other external actions.
Do not infer permission for them from a request only to prepare notes.
