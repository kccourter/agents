---
name: implementation
description: Deliver an authorized local fix, maintenance task, or feature increment through implementation, validation, review, and its authorized local commit. Investigate and choose tactics within the accepted outcome and boundaries.
---

# Implementation

Read the accepted request or contract, effective repository instructions, and
relevant existing evidence. A local fix may use the request itself as the
contract; do not require new goal/research/plan documents. Check repository,
branch/worktree, and ownership before editing; preserve unrelated work.

Within the approved outcome, invariants, ownership, dependency policy, and
resource ceiling, choose files, helpers, tests, and local refactors. Inspect
callers, reproduce defects, and investigate surprising evidence as needed.
Expected files are starting points, not an exhaustive edit list. Update
material tactical changes in the existing record without seeking new approval.

Prefer the simplest maintainable change that fully solves the problem. Reuse
existing behavior or code where it fits; avoid speculative abstractions and
unrelated cleanup. Minimum changed lines are not a substitute for correctness.
Keep future or optional outcomes outside this implementation.

Add or extend tests for changed behavior, reproduced defects, and consequential
unprotected boundaries, including existing behavior that lacks coverage.
Test observable behavior and meaningful failure modes. Reuse existing tests
when suitable; a new regression test is allowed. Do not impose a test count or
require tests that merely mirror a reversible documentation/configuration edit.

Use [checklists/implementation.md](checklists/implementation.md) and
[checklists/validation.md](checklists/validation.md) as proportional completion
aids. Run required focused and integration checks, review the diff, and update
only affected documentation. Record commands, outcomes, relevant source/input/
environment identities, and limitations in the existing task or increment
receipt. Fix within-scope failures and review findings before declaring success.
A blocked required check remains a completion limitation.

Request a decision before an unapproved change to outcome, public/schema/fixture
contracts, ownership, dependency policy, resources, or external authority.
Evaluate major architectural decisions during planning or on material new
evidence; routine local design choices do not need architecture review.
Previously approved changes need no repeated approval. Keep independent
authorized work moving while a decision is pending.

When the adopted workflow includes normal local commits in implementation
approval, complete the commit after validation and review unless the user or
project reserves commits. Stage only owned task files, inspect the staged diff,
and run `git diff --check`. Commit a completed increment before dependent work;
do not wait for a separate close instruction or combine completed increments
at branch end. Otherwise follow the existing commit authorization.

Return the outcome, changed files, checks and limitations, evidence pointers,
commit and worktree state, and any unresolved decision. Do not claim completion
until required checks, review, records, and authorized commits are accounted for.
