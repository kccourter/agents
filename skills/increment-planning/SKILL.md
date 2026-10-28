---
name: increment-planning
description: Turn an authorized outcome and available evidence into a compact implementation contract or dependent increments. Use when work needs an explicit contract; do not require a separate plan for a sufficiently scoped local fix.
---

# Increment Planning

Plan an observable outcome at the smallest useful scale. Read the request,
existing authorization, relevant findings, and effective repository instructions.
A separately approved research document or PLAN 00 is not a prerequisite.
Resolve bounded unknowns while preparing a concrete proposal.

Use the existing task/plan surface. For a durable goal, contracts normally live
at `docs/goals/NN-GOAL_NAME/plans/INC-NN-short-title.md` with `# INC NN Title`
headings. [templates/increment-plan.md](templates/increment-plan.md) is a guide,
not a required document for every task.

Include the outcome, invariants and non-goals, ownership, relevant contract or
artifact identities, acceptance checks, dependencies, known uncertainties,
allowed experiments/resources, and escalation conditions. Expected files and
reuse targets are discovery hints; leave implementation details, tests, and
local refactors to the implementer within these boundaries.

Prefer one contract for one cohesive feature. Split only where outcomes can be
implemented and checked independently or real dependency/authority gates require
it. For coordinated work, keep a short `PLAN-00-roadmap-and-inventory.md`, name
producer/consumer gates, and expand the next executable slice as facts settle.
Do not create a fixed inventory/research increment for every feature or elaborate
uncertain downstream plans.

Planning itself does not authorize product changes. Present the concrete
contract for approval if implementation scope or a consequential boundary is
not already authorized. When the accepted request or approved plan already
covers it, record that authorization and continue without repeated approval.
Honor project-specific plan-commit requirements. A planning-only request ends
with the requested proposal, not unsolicited implementation.
