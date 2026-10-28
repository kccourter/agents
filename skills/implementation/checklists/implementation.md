# Implementation Checklist

Use only the items relevant to the authorized task; this is not a new approval
or documentation gate.

- [ ] Confirmed outcome, invariants, ownership, resource limits, and existing authorization.
- [ ] Inspected affected code/callers and relevant current evidence.
- [ ] Preserved unrelated work and kept edits within the accepted outcome.
- [ ] Reused suitable code; chosen helpers/refactors for correctness and maintainability.
- [ ] Added or extended meaningful tests for changed behavior, reproduced defects, or consequential unprotected boundaries where needed.
- [ ] Ran required checks and addressed within-scope failures and review findings.
- [ ] Updated affected docs and the existing receipt with evidence and limitations.
- [ ] Reviewed the diff, staged only owned files, and ran `git diff --check`.
- [ ] Made the authorized local commit, unless explicitly reserved; reported commit/worktree state.

An unexpected file edit or new regression test within scope does not need a
new approval. Escalate actual changes to unapproved outcome, contracts,
ownership, dependency policy, resources, or external authority.
