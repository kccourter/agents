---
name: implementation-audit
description: Independently audit an implementation or branch before PR for evidence-backed correctness defects, integration failures, and regression gaps. Use for critical implementation scrutiny with High/Medium/Low priorities, not routine closeout, style review, or implementing fixes.
---

# Independent Implementation Audit

Produce actionable, independently justified findings. A passing suite and an
implementation record are evidence to examine, not proof of correctness.
Finding no confirmed defects is a valid outcome. Do not manufacture a quota.

## Independence and scope

- Prefer a new agent/session that did not implement the changes. A skill cannot
  erase existing context. If you authored the implementation or inherited its
  conversation, disclose that limitation; do useful verification without claiming
  independent review. Do not require another approval merely to inspect code.
- Establish the requested repositories/worktrees, target revision and comparison
  base. For pre-PR review, start with the branch diff and follow affected callers,
  producers, consumers and runtime paths beyond changed lines. Audit the entire
  implementation only when that broader scope was requested.
- Use local instructions and user-approved requirements to establish intended
  behavior. Discover entry points and trace actual behavior yourself before
  reading the implementer's conclusions or previous findings when practicable.
  Afterwards, reconcile those records and test claims against your own evidence.
  Do not disregard legitimate design constraints to preserve a theory.
- Record exact revisions, dirty files and relevant environment assumptions.
  Never clean up, stash or overwrite user work. Distinguish committed code from
  dirty changes actually inspected. If the target changes during review, identify
  which evidence is stale and recheck affected findings.
- This skill authorizes an audit, not repairs, contract changes, commits, pushes,
  dependency changes or production operations. Create bounded reproductions and
  outputs in temporary/ignored locations. Write the requested audit report using
  the repository's documentation convention; do not alter production code or
  durable tests to make a finding or a check pass.

## Build your own evidence

1. **Map the behavior.** Read the relevant contracts, configuration, entry points,
   source and tests. Identify supported workflows, important invariants, ownership
   boundaries and externally visible outcomes. Inspect a real producer and its
   consumer rather than assuming matching names imply compatibility. Prioritize
   changed or high-impact paths; document what you did not inspect.
2. **Form falsifiable hypotheses.** For each suspicious path, name a realistic
   trigger, expected behavior, observed/code-derived behavior and consequence.
   Trace reachability. Check guards, callers, alternate branches and the approved
   contract for reasons your hypothesis might be wrong. Search for existing
   helpers/tests before proposing missing behavior.
3. **Exercise the boundary.** Run the smallest existing check or reproduction that
   distinguishes expected behavior from the suspected defect. Use independent
   expectations derived from the contract, not a copy of the implementation.
   Prefer real serialization, command routing, request framing and artifact
   ingestion across the relevant boundary. A mock that supplies the missing field
   or replaces the failing function cannot establish that the integration works.
   Identify exactly what was real and what was stubbed.
4. **Probe failure paths selectively.** Follow risks present in the code: negative
   results versus execution failures, malformed/partial input, cancellation and
   cleanup, stale identities, numeric edge cases, schedule/resume behavior or
   missing evidence. Do not apply a giant checklist unrelated to the change.
   Use bounded timeouts and clean up only processes/artifacts you created.
5. **Compare with the base.** For a failing check, establish whether it reproduces
   on the comparison revision under equivalent conditions. A baseline copy must
   retain any Git metadata, fixtures and runtime routing the check depends on;
   a different setup failure is not reproduction of the same bug. If a comparison
   is unavailable, report attribution as unknown. Do not weaken the check or
   rename a failure as environmental without evidence.
6. **Reconcile coverage.** Run relevant broader checks when focused results justify
   them. Record exact commands, outcomes, exclusions, skips and timeouts. Tests
   blocked at collection did not execute. A smoke proves execution, not production
   quality, numerical parity, model quality or exhaustive correctness. Identify
   the next discriminating check if expensive integration remains untested; do not
   launch campaigns, frozen exams or external services solely to finish an audit.

Keep candidate notes as working hypotheses. Consolidate duplicate symptoms of
one cause. Drop disproven claims. If an adjacent pre-existing defect is confirmed,
report it separately without silently expanding the audit into a cleanup project.

## Evidence and priority

A confirmed finding needs either an executed reproduction or a complete source/
contract proof: reachable input, violated invariant, missing effective guard and
observable consequence. Label which kind of proof you have. Never imply a test
ran when the conclusion came from reading code.

Use these priorities based on impact and realistic exposure, not file size,
code complexity, confidence or how easy a fix appears:

| Priority | Criteria | Default disposition |
| --- | --- | --- |
| High | Blocks a primary supported workflow; silently corrupts important results or evidence; loses data; violates an important security/authority boundary; or causes an unbounded failure with substantial operational impact. State the concrete trigger and affected users/workloads. | Recommend resolving before merge or an explicit navigator decision accepting the demonstrated risk. |
| Medium | Incorrect behavior in a supported but narrower workflow, a broken integration/failure path, or a bounded reliability problem with meaningful user impact. | Recommend correction; explain whether the affected path makes it a merge blocker or suitable for an explicit follow-up. |
| Low | A demonstrated, limited-impact defect in behavior, diagnostics, or an executable/documented workflow; a practical workaround exists and core results remain reliable. | Usually suitable for follow-up. |

Keep evidence confidence separate from priority:

- **Confirmed:** reproduction or complete source/contract proof supports the claim.
- **Unresolved hypothesis:** a concrete suspicion with a missing proof step. Put
  it under open questions, state the possible impact conditionally, and identify
  the smallest check needed. Do not count it as a confirmed High/Medium/Low bug.

Classify attribution independently: introduced by this change, pre-existing,
environment/setup limitation, or unknown. A serious pre-existing bug may still
matter for shipping, but must not be attributed to the branch without evidence.
Style preferences, speculative future needs and requests to rewrite working code
are not correctness findings. A missing test alone is a coverage gap; identify
the actual unverified behavior rather than inventing a runtime defect.

## Deliverable

Lead with confirmed findings ordered High, Medium, Low. Use stable IDs such as
AUDIT-001. For each, provide:

- Priority, concise title, evidence type and regression attribution.
- Exact repository/file/line references at the audited revision.
- Supported trigger and expected versus actual behavior.
- Concrete consequence and affected scope; avoid unsupported worst-case claims.
- Reproduction command and decisive output, or the complete source proof.
- Relevant counterevidence considered, and limits/stubs of the proof.
- Smallest corrective direction and a regression check that would catch it;
  leave implementation to a separate task/agent.

Then include:

- A compact validation table: command, result, baseline comparison, limitations.
- Open questions and coverage gaps, separate from confirmed findings.
- Scope/revisions/environment, inspected paths and unreviewed areas.
- Merge assessment: blockers, bounded follow-ups, and prerequisites still untested.
  Say "no confirmed defects in the inspected scope" when appropriate, not
  "nothing is broken" or "safe to merge" without qualification.

Use a user-specified report path first, otherwise an existing goal's audit/record
convention, otherwise a new uniquely named report under `docs/audits/`. Keep raw
logs/reproductions ignored. Do not overwrite historical reports or automatically
commit the report. If writing is not authorized, provide the report in the reply.

For a follow-up audit, independently rerun each claimed fix and inspect nearby
behavior. Record resolved/unresolved/new IDs against the new revision; the
implementer's completion statement is not verification. Recommend separate fix
and verification passes so diagnosis does not become defense of your own patch.
