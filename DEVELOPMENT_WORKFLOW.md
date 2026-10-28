# Development Workflow

This reusable workflow governs work where the project has adopted it. Read the
effective repository and workspace `AGENTS.md` files for ownership, runtime,
validation, and external-action policy. Instruction templates are examples;
they do not replace active local instructions. Honor the user's current scope
and existing authorization.

## Choose a proportional lane

| Lane | Minimum useful process |
| --- | --- |
| Local fix or maintenance | Requested outcome and acceptance checks; focused inspection and implementation; verification and diff review; short receipt and authorized commit. |
| Cohesive feature | Focused investigation; one approved implementation contract; implement, verify, review, and commit. Split only at independently verifiable outcomes. |
| Coordinated change | Goal and dependency order; producer contract and fixture gates; consumer waves; integration reconciliation and commits in each owning repository. |

Choose by actual scope and risk, not the number of files. A local fix does not
need a goal folder, research document, roadmap, and separate plan approval.
Use the existing task, issue, goal, or record as the authoritative state. Do not
create a second status system or documents that add no durable information.

## Authority and boundaries

The project navigator is the person steering the outcome and consequential
decisions. A sufficiently concrete request can authorize implementation; do
not ask again merely because it is being written into a plan. A request only
to investigate or plan does not authorize product changes.

Within the approved outcome, invariants, repository ownership, dependency
policy, and resource ceiling, choose implementation details, tests, and local
refactors autonomously. Investigate evidence that challenges the plan. Expected
files and reuse targets guide discovery; they are not an exhaustive edit list.
Record material tactical changes in the existing task or record.

Ask before changing an unapproved outcome, public contract, schema or fixture
contract, ownership boundary, dependency policy, resource ceiling, or external
authority. Resolve product preferences when they materially change the result.
An already approved boundary change does not need another approval. While a
decision is pending, continue independent authorized work.

Missing tests, unfamiliar code, an extra helper, or an unsuccessful diagnostic
probe are reasons to investigate within the existing scope and budget. They
are not automatic approval gates. If the authorized budget is exhausted or
progress depends on an unresolved consequential decision, report the evidence
and the specific decision needed.

## Investigation and planning

Start with relevant current findings, code, and validation paths. Recheck only
evidence whose source, environment, inputs, or assumptions may have changed.
Research ends when it supports the next decision; no fixed research ladder or
full repository survey is required. Bootstrap, investigation, and proposal
preparation may continue in one session without intermediate approval.

The implementation contract records the observable outcome, acceptance checks,
invariants and non-goals, ownership, relevant artifact identities, dependencies,
known uncertainties, allowed experiments/resources, and escalation conditions.
Keep it as short as the task permits. It can be the accepted request or an
existing plan; a separate implementation brief is unnecessary.

Review architecture when a major API, module boundary, data model, dependency,
or cross-repository design decision needs evaluation, during planning or when
implementation exposes material new evidence. Routine private helpers and
local refactors do not trigger architectural review. Review is not itself a
new approval gate; seek a decision only for unresolved or changed boundaries.

## Goal and record surfaces

For work needing a durable goal, use the project's existing convention. The
default for new goal directories is `docs/goals/NN-GOAL_NAME/`, with uppercase
snake case and the next number after the highest matching numbered directory.
Preserve legacy names instead of renaming historical evidence.

The goal `README.md` indexes outcome, scope, current position, decisions, plans,
and evidence. Put implementation contracts in `plans/`, execution receipts in
`records/`, and reusable findings in `reference/`. Create only useful files.
For multiple dependent increments, `plans/PLAN-00-roadmap-and-inventory.md`
holds the short roadmap; expand the next ready slice instead of elaborating
uncertain downstream work. Follow-on contracts use `INC-NN-short-title.md`
with `# INC NN Title` headings. PLAN 00 is planning work unless product work
was separately authorized. Commit approved plans first when project policy
requires it; do not introduce a plan-commit gate for every small task.

A receipt should identify changes and decisions, commands and results,
limitations, and the next action if any. Update the current index pointer when
preserving a finding. Include its conclusion or open hypothesis, supporting
evidence, applicability, and conditions that require rechecking it. Keep raw
logs in artifacts and link them. An inconclusive finding may remain open.

## Implementation, validation, and commits

Inspect the actual worktree and preserve unrelated changes. Use isolated
worktrees when needed; do not stash, reset, overwrite, or switch away from
ambiguous work to force a clean starting state.

Prefer the simplest maintainable solution that fully satisfies the outcome.
Reuse existing code where it fits, without forcing a one-line patch or hiding
complexity to minimize changed lines. Add or extend tests for changed behavior,
reproduced defects, and consequential unprotected boundaries. Test observable
behavior; do not require a new test for every reversible documentation edit.

Run the checks required by the task and the files actually touched, then
review the diff and affected documentation. Use focused checks while iterating
and required integration checks at their gates. Record command, result, source,
environment, and input/fixture identity to the extent needed for reproducibility.
Reuse evidence only when those identities still match. Report failed or
unexecuted checks honestly; recording a blocker does not make a required gate
pass. Use independent review for consequential behavior such as numerical
semantics, contracts, concurrency, authentication, or important integrations.

When this workflow is adopted, implementation approval includes the normal
local implementation commit after validation and review, unless the user or
project explicitly reserves commits. Stage only owned task files, inspect the
staged diff, and run `git diff --check`. Commit each completed increment before
its dependent work begins; do not combine already completed increments into a
late branch-wide commit. Use the project's naming convention, for example
`task: implement INC NN Title`, or a concise fix/maintenance subject.

Report the commit and worktree state, including any preserved unrelated work.
A task with an authorized commit requirement is not complete before that commit.
Use follow-up commits for later fixes; do not rewrite shared history without
authorization. Pushing, opening a remote PR, publishing, and other external
actions follow the user's authorization and effective project policy.

## Coordination and handoff

Delegate when independence, expertise, or elapsed time benefits. A compact
assignment supplies the outcome, owning repository/worktree, prerequisites and
input revisions, invariants, allowed actions and resource ceiling, acceptance
checks, escalation conditions, and expected evidence. Keep one writer per
worktree; isolate concurrent writers and make Git index/commit ownership clear.
One coordinator updates shared goal state; workers return receipts.

Consumers begin after required producer commits, contracts, checked fixtures,
and validation are reconciled. Preserve approved fixture bytes and identities
across repositories. An unexpected mismatch requires diagnosis or a contract
decision, not silent fixture replacement. Honor local repository/runtime
boundaries; do not add cross-repository coupling as a validation workaround.

A handoff identifies the outcome, repository/worktree and revision, changed
files, validation evidence, artifact/fixture identities when applicable, open
questions, commit, and worktree state. The coordinator verifies the evidence
and required integration gates; a worker's success claim alone is insufficient.
Optional or deferred work remains outside the accepted outcome.

## Closeout

Reconcile the existing status and evidence, affected documentation, and any
required reproduction instructions. Keep PR notes concise and prepare them
when requested, following the project's location/template and remote policy.
Do not require a new runbook, full independent audit, or separate close command
for every task. Completion means the authorized outcome, checks, review,
records, and applicable commits are accounted for, with limitations explicit.
