---
name: architecture-review
description: Evaluate consequential architecture choices during planning or when implementation exposes material new evidence. Use for major API, module, data-model, dependency, or cross-repository decisions, not routine local implementation choices.
---

# Architecture Review

Evaluate the consequential decision using the accepted outcome, current
contracts, relevant code, and existing architecture records. This skill can
support planning before implementation or a material discovery during it.
It produces a recommendation; it does not independently authorize product
changes or expand the task.

Review major changes to public APIs, ownership or module boundaries, core data
models, dependency policy, extension contracts, or cross-repository design.
A new private helper, file, or local refactor alone is not a trigger.

Compare the smallest viable options against compatibility, cohesion, coupling,
testability, operational risk, and maintenance cost. Prefer evolving existing
components when they fit. Investigate bounded unknowns needed for the decision;
do not require a full repository survey.

Record the problem, evidence, recommendation, meaningful alternatives and
tradeoffs, affected owners/contracts, validation implications, and open decision
in the existing plan or architecture record. Keep the recommendation concise.

Request a decision before implementing an unresolved change to outcome,
contracts, ownership, dependency policy, resources, or external authority.
If that decision is already approved and the evidence still supports it,
continue the authorized work without asking again. Keep independent authorized
work moving while a consequential decision is pending.
