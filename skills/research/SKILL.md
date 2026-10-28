---
name: research
description: Resolve repository questions with targeted investigation and preserve evidence useful to an authorized task. Use for feature discovery or bounded diagnosis; routine fixes do not require a separate research phase.
---

# Research

For causal ML or stateful-system investigations, use
[scientific debugging](references/scientific-debugging.md) when competing
explanations, paired evidence or replay capture matter. It adds guidance for
semantic preflight and first-divergence analysis; routine fixes need no extra
planning stages.

Answer the next decision-relevant question. Begin with current indexed findings,
applicable repository instructions, and the affected execution path. Search
with `rg` or `rg --files` before broad reads. Revalidate older findings when
sources, environments, inputs, or assumptions have changed.

Identify relevant behavior, reusable components, contracts, ownership,
invariants, existing tests, and validation paths. Expand along dependencies
only as the question requires. Distinguish observed facts, hypotheses, and
recommendations; cite paths/symbols, revisions, commands, or artifacts that
support them.

Missing coverage, unfamiliar code, failed probes, or unexpected complexity do
not force a stop. Choose bounded inspections, reproductions, or diagnostic
experiments that discriminate between explanations within authorized resources.
There is no fixed probe ladder. Do not run costly experiments, change external
state, or alter product behavior without the applicable authorization.

Preserve a concise answer, evidence, applicability, and open question in an
existing goal reference or task record when it will prevent rediscovery.
[templates/research-notes.md](templates/research-notes.md) is optional; omit
irrelevant sections and avoid a second document that repeats the current plan.
Update the existing index pointer for reusable findings. An inconclusive
investigation may be recorded as open with its next discriminating question.

Research is sufficient when the next decision is supported. It may flow into
proposal preparation without separate research approval. If implementation is
already authorized, continue bounded investigation and implementation within
that outcome; a research-only request does not authorize product changes.

Seek a decision only for unresolved outcome or preference changes, contracts,
ownership, dependency policy, resource ceilings, or external authority. Continue
independent authorized work while that decision is pending. At a budget limit,
return the evidence and a concrete next decision instead of silently extending
the investigation or presenting an open hypothesis as a conclusion.
