# Bounded scientific debugging

Use this guidance when an ML or stateful-system failure needs a causal
explanation. A routine reproducible code defect does not need a hypothesis
ledger or an experiment plan.

Start from the failing observable and the decision it affects. Separate the
measurement from the explanation. Record the checkpoint/source, architecture,
population/split, encoding, inference flags, runtime and RNG identities that
matter. Reuse earlier findings only where those conditions still apply.

Keep competing explanations and the next distinguishing observation in the
existing task record. A compact table of hypothesis, prediction, control,
evidence, and supported/refuted/inconclusive status is enough. Choose the
cheapest informative probe from retained artifacts, fixed inputs/tensors,
paired interventions, or a new physical run; there is no mandatory ladder and
no new increment for each hypothesis. Keep immediate debugging with the agent
that has useful context. Escalate a bounded unresolved question with evidence.

Before reserving compute or starting a worker, run the project's semantic
preflight. Check the *role* of each manifest, selected membership/order, source
and fixture identities, and whether the retained bytes are actually available.
A worker-development configuration and an evaluation panel may legitimately
name different populations. Report the first meaningful disagreement. Preserve
the failed attempt and its charged reservation; stale evidence is not authority
to repeat a run. Continue within the user's existing experiment allowance.

Trace the first differing boundary: observation, encoding/mask, policy output,
selected wire action, applied action, transition, reward and terminal outcome.
Distinguish changed metadata from changed control/physical facts. Missing fields
are unavailable evidence, not equality. After paired trajectories diverge,
later states no longer provide the same-state counterfactual. Report the common
prefix and the point where that comparison stops being valid.

For interventions, keep the intended changed factor explicit and preserve
controls. Where matching RNG is meaningful, record draw ordering and consume
the same draws before overrides; matching seeds alone does not ensure matching
streams. Use the actual sampling unit (often scenario/episode) for comparisons,
not correlated transitions as independent examples. A diagnostic panel or
training population does not establish deployment or unseen-set qualification.

Retain evidence for the next plausible offline question. Bounded complete
episode/batch capture can include raw observations, exact stored encodings,
tensor dtypes/shapes/masks and order, actions/old log probabilities/values,
targets with unit conventions, RNG before/after, and retrievable checkpoint
and optimizer payloads. Record correspondence that is only caller-declared.
Capture should leave actions, RNG, parameters and default traces unchanged.
Demonstrate restore from retained payloads; hashes and aggregate statistics do
not reconstruct missing tensors. Successful-batch export does not preserve
an interrupted collector unless that case is explicitly supported.

Use the owning repository's validators and offline diagnostic tools. Keep raw
logs/tensors in retained artifacts, selected findings and limitations in the
context brief, and the reusable conclusion in the current reference index.
Do not rerun physics to answer a question already determined by retained bytes.
When a new run is necessary, explain what new observation it will provide and
respect the accepted outcome, authority, and remaining resource allowance.
