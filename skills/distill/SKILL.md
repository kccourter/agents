---
name: distill
description: Preserve reusable diagnostic or strategy findings with evidence, applicability, and a current index pointer. Use before valuable session context is lost; partial findings may remain explicitly open.
---

# Distill

Convert useful investigation into durable knowledge so the next session need
not reconstruct the conversation. Use this for a supported conclusion, chosen
strategy, confirmed dead end, or partial investigation worth continuing.
Skip one-off exchanges that have no future use. This skill does not authorize
product changes or create implementation plans.

Update an existing finding when possible. Use the owning goal's `reference/`
for reusable knowledge or `records/` for an increment-specific investigation;
otherwise use the project's established evidence location. Create a separate
note only for a distinct reusable question, not for every diagnostic probe.

Capture, concisely:

- The question or symptom and the conclusion, decision, or **open hypothesis**.
- Evidence: relevant paths/symbols and revisions, commands/results, input or
  artifact identities, and links to detailed logs. Separate observation from
  inference and state what the evidence actually rules out.
- Applicability: the source, architecture, schema, environment, checkpoint,
  population, or runtime assumptions that matter to this finding, and changes
  that would require rechecking it. Include only dimensions relevant here.
- Rejected approaches worth not repeating, unresolved questions, and the next
  discriminating check or action with its owner when known.
- Any older finding superseded or limited by this evidence.

Update the existing current index (goal `README.md`, reference index, or task
index) with a link, short status/conclusion, applicability, and supersession
pointer when relevant. The durable note and current pointer are one deliverable;
do not create a parallel decision/status system.

Do not retell the conversation or paste large logs. Preserve only reasoning
needed to assess the conclusion and avoid repeated work. An inconclusive
session remains open even if no next action is known: state the missing
evidence or decision. Do not require a pause or invent a conclusion to distill
partial findings. Future sessions should start here, then revalidate when the
recorded applicability conditions no longer hold.
