# Using the workflow

Read the effective repository/workspace `AGENTS.md` files and the adopted
`DEVELOPMENT_WORKFLOW.md`. This package supplies reusable guidance; local
ownership, runtime, and external-action rules still apply. Work in the correct
repository/branch or worktree and preserve unrelated changes.

Choose the amount of process the outcome needs:

| Work | Example request | Expected completion |
| --- | --- | --- |
| Local fix or maintenance | “Fix the empty-input crash, add regression coverage, run the relevant checks, and commit.” | Focused inspection and fix, verification, diff review, concise receipt and commit. No new goal folder required. |
| Cohesive feature | “Add CSV export for the current filtered view. Keep the existing API and dependencies; investigate and prepare one implementation contract.” | Resolve bounded unknowns and propose one concrete outcome. After implementation authorization, complete it without another approval at every thinking stage. |
| Coordinated change | “Plan the versioned artifact change across the producer and consumers, preserving independent ownership.” | Goal/dependency order, contract and fixture decisions, ready increments, and integration gates. |

A concrete request to implement may already supply the contract and approval.
A request only to research or plan stops at that deliverable. Once the outcome
is authorized, the agent chooses files, helpers, tests, local refactors, and
bounded diagnostic probes within the agreed invariants and resources. It asks
again only when consequential boundaries or unresolved product preferences
change. Missing tests and routine uncertainty are reasons to investigate.

For a durable feature/coordination goal, use the existing naming convention or
`docs/goals/NN-GOAL_NAME/`. The goal `README.md` is the current index. Use
`plans/`, `records/`, and `reference/` as needed. A short PLAN 00 is useful for
dependent increments; it is not a mandatory research stage for every task.
Expand the next ready slice instead of fully planning uncertain downstream work.

Useful requests include:

- “Investigate this failure within the existing test budget; continue local
  probes and record any open hypothesis. Ask before an external run.”
- “I approve the proposed outcome and checks; implement and complete its normal
  local commit.”
- “Distill these findings with evidence, applicability, and the current index
  pointer. Keep unresolved conclusions open.”
- “Review the completed outcome and prepare PR notes under our project policy.”

Under this adopted workflow, implementation approval includes normal local
commits after verification and review unless you reserve them. No separate
“close the increment” instruction is needed. Each completed increment is
committed before dependent work. Review the reported evidence and limitations;
a recorded blocker does not mean a required check passed.

Remote PR creation, pushing, publishing, and other external actions follow
explicit user authorization and project policy. Preparing PR notes alone does
not authorize those operations. Keep optional work separate from completion.
