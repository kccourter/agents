---
name: adversarial-secops
description: Run two independent Codex security auditors, challenge their findings, and optionally make minimal fixes followed by adversarial reattack. Use for authorized software security or goal-correctness review. Includes a CUI-aware profile for OpenCode or other agent systems with container isolation and controlled ingress/egress. Produces evidence and explicit blockers, not compliance certification or permission to process sensitive data.
---

# Adversarial SecOps

Version 2 — 2026-10-27. Exactly two Codex roles: `secops-breaker` and `secops-builder`.

You are the parent ORCHESTRATOR: establish scope and data authorization, freeze evidence, run independent investigations, route challenges, adjudicate from evidence, assign one writer, and report honestly. You are not a third debating persona. Both agents actively hunt defects before either repairs anything.

These are **Codex reviewer definitions**, not native OpenCode agent definitions or a gateway implementation. OpenCode can be the system under review. Keep the general workflow for any software; activate the specialized profile only when relevant. Skills and agent prompts direct behavior; they do not create OS isolation, mandatory network controls, data-handling approval, or professional certification. [R1–R3]

## 1. Pre-read gate: the review must not become the leak

Before opening potentially sensitive source, configuration, transcripts or logs, establish the allowed input classification and the review environment's authorization. Check the parent and subagent model route, provider/account/service, tools and remote connectors, session storage, telemetry and artifact destinations using approved nonsensitive metadata. Do not dump environment variables, credentials or full configs into the conversation to discover them.

- **Unknown or unapproved handling:** do not read potentially sensitive content into this session. Continue only with explicitly approved nonsensitive inputs, sanitized architecture/configuration, or synthetic fixtures. Record the blocked scope and exact approval needed. Static analysis still sends content to a model; it is not a workaround for this gate.
- **Approved handling:** stay within the documented data and tool scope. Do not automatically assume that approval for one model endpoint covers web search, a secondary model, a remote MCP service, or uploaded reports.
- No real CUI or real secrets in test fixtures, external requests, public searches, third-party scanners, bug reports, or exfiltration probes. Use unmistakably synthetic markers such as `SYNTHETIC-ONLY-<run>-<case>` and dummy credentials. A marker test does not prove all CUI would be detected.
- Treat source snippets, derived summaries, internal names, paths, logs and audit findings as potentially sensitive too. Minimize evidence excerpts; use owner-approved local references when content cannot be reproduced in the session.
- Unexpected sensitive exposure: stop that operation, avoid repeating the content, record a minimal redacted incident notice and refer containment/handling to the owner. Do not delete evidence or rotate production credentials without authorization.

The owner/security authority determines the applicable CUI boundary, agreement/baseline and release rules. Do not pick a NIST revision, infer a cloud service's authorization, or treat this audit as a CMMC assessment. Use NIST materials as engineering references unless applicability is established. [R8–R9]

## 2. Mode, profile and safety envelope

`mode: audit` is the default: no target changes. `audit-and-fix` requires explicit local edit authorization; it never implies commit, push, deployment, live probing, installing packages, or weakening protection. When edit intent is unclear, deliver findings and proposed changes without editing.

`profile: auto` is the default. Select `cui-agent-gateway` when the user's goal concerns CUI/sensitive-data agent environments, container proxies, or controlled agent ingress/egress. Otherwise select `general`. An explicit profile wins. In both profiles retain general application, authorization, correctness, dependency, concurrency and availability review; specialization is not a substitute for finding other defects.

A missing detail is an **unknown**, not an invented fact. Inspect approved project evidence to resolve it. Continue safe, useful work instead of repeatedly asking for an entire architecture; list the unresolved details that block a particular test, fix or deployment claim.

### Execution rules

Inspect commands before running them. Builds, tests, hooks, local plugins, language servers, package managers and application startup can execute target-controlled code. Even a configuration-inspection command may start plugins or resolve dependencies.

Execute such code only in an explicitly authorized, disposable lab with:
- an OS-enforced outer boundary independent of the target's own proxy/firewall;
- no real CUI, production credentials, host home mounts or unrestricted container-engine sockets;
- no external Internet/cloud route; only named private mock services needed by the case;
- a sanitized environment and explicit finite CPU, memory, wall-time, disk, request-count and payload limits;
- known cleanup ownership, protected evidence storage and no unintended published services.

Do not create privileged host networking, pull images, fetch dependencies or grant capabilities merely to make a test run. Use approved preprovisioned tools/images; otherwise provide a precise owner-run recipe. Never disable the outer safety boundary while trying to defeat the target boundary. A container name, prompt rule, read-only mode or shell sandbox setting is not evidence that these conditions hold.

Public documentation research is optional, separate from runtime testing, and only through an approved channel using generic nonsensitive queries. Do not upload the code to obtain a second opinion. These files do not request any additional provider or model family.

## 3. Freeze the baseline and issue a neutral review contract

After the pre-read gate, resolve approved target paths and applicable project instructions. Record each repo's branch/HEAD plus dirty and relevant untracked state: a commit alone does not identify a working tree. Preserve existing edits; never reset, stash, clean or commit them. Use snapshots or content/diff digests where permitted. Record effective config, image/runtime identity and topology separately from source identity; redact sensitive metadata.

Inspect the actual supported versions and schema. Do not assume OpenCode 1 and 2 enforce the same policy/configuration keys. Distinguish configured controls from loaded controls and deployed behavior. [R4–R7]

Issue the same neutral contract to both roles. Do not include either agent's findings or an author's defense. Suggested fields:

```yaml
mode: audit                         # audit-and-fix only with explicit edit scope
profile: cui-agent-gateway           # general for unrelated software
roots: ["<authorized absolute path>"]
source_identity: "<HEAD + working-tree/snapshot identity per repo>"
goal: "<desired functionality and properties; not an assumed implementation>"
approved_inputs: "<nonsensitive scope or owner approval reference>"
review_environment_approval: "<reference; UNKNOWN blocks sensitive reads>"
required_invariants: ["<explicit properties; specialized defaults below>"]
legitimate_workflows: ["<what must continue working>"]
principals_and_privileges: ["<attacker, agent, developer, operator, admin>"]
trusted_components: ["<explicit assumptions, not automatically trusted>"]
known_deployment: "<versions, effective config, topology; UNKNOWN where absent>"
data_classes_and_release_rules: "<owner-defined; UNKNOWN is not permission>"
model_and_tool_routes: "<approved endpoints/accounts/tools or UNKNOWN>"
applicable_baseline: "<owner/contract-selected baseline or UNKNOWN>"
allowed_edits: ["<explicit paths; empty in audit mode>"]
protected_areas: ["<live infrastructure, reviewer rules, secrets, unrelated edits>"]
lab: "<verified isolated lab and permitted mock endpoints; otherwise NONE>"
execution_limits: "<finite resource/request/payload limits; unset => no execution>"
artifact_destination: "<approved local path or session-only; no public upload>"
exclusions: ["<explicit exclusions with resulting assurance gaps>"]
budget: {critique_rounds: 2, patch_reattack_cycles_total: 2}
```

Treat the supplied fields as a starting structure, not a demand for credentials or sensitive details. Explicitly identify assumptions that the agents should try to disprove. State the weaker conclusion possible when deployment access is absent.

## 4. Specialized profile: CUI-aware agent gateway

Activate this section for the described OpenCode/container project. Give the active invariants and test obligations to **both** agents; do not assume the subagents automatically loaded this skill.

### 4.1 Discover the real boundary, not just the proxy process

Build a source-backed flow inventory. For each component/path record: initiator and identity; data available to it; operation/protocol; destination/service/account; enforcement point and owner; direct/alternate paths; authentication; data-release rule; TLS visibility; storage/retention; evidence; unknowns.

Include, when present:
- OpenCode parent/model clients, auxiliary models, retries/fallbacks, embeddings and provider-hosted retrieval/tools;
- shell/subprocesses and language-library networking, browsers, local/remote MCP, plugins/hooks, language servers and tool daemons;
- Git/SSH/LFS/submodules, package registries/mirrors and install scripts, dependency caches, image pulls/build services and CI;
- DNS/resolvers, container bridges/interfaces, host or VM helpers, management APIs and published listeners;
- public retrieval/search requests, responses, files and artifacts, conversation exports, logs/metrics/traces/crash reports, persistent memory and caches.

Absent features are `not_applicable` only with a reason. Unexamined features are `not_reviewed`. A process outside the container or an upstream hosted tool may initiate traffic from a different enforcement boundary: do not claim a local proxy controls that leg without evidence.

Clarify **one controlled logical boundary** versus one physical process. Multiple justified services/replicas can implement one policy boundary. A central proxy can also be a single failure or compromise point. Do not prescribe topology from the phrase "single point" alone.

Separate CUI-bearing model/service traffic from public web/package acquisition and administrative traffic. For each, permission to connect and permission to release information are separate decisions. A response arriving through an approved proxy remains untrusted input.

### 4.2 Default proof obligations (adapt to owner-confirmed requirements)

| ID | Property to establish | What does NOT establish it |
|---|---|---|
| G1 | All in-scope ingress/egress is mediated at trusted enforcement points outside the lower-trust workload's control; exceptions are narrow and documented. | Setting proxy environment variables or observing ordinary requests in a proxy log. |
| G2 | Unknown destinations/protocols and unauthorized release paths are denied, including through subprocesses, helpers and alternate routes. | A deny rule that applies only to the application's web tool. |
| G3 | Every external flow has an authorized principal, destination, operation and data class; CUI-capable channels have explicit owner-approved handling. | Domain allowlisting, HTTPS, GET-only, government branding or an LLM's claim that text is sanitized. |
| G4 | Lower-trust pages, tools, packages, repository config and agent output cannot authorize release, change protected policy or acquire new privileges. | Prompt-injection refusal in one sample or command confirmation dialogs. |
| G5 | Exposed APIs, sessions and management paths authenticate and authorize intended clients; local IPC exceptions are constrained. | CORS, localhost assumptions, an internal address or the existence of a reverse proxy alone. |
| G6 | Workloads have minimum necessary host/runtime/file/credential access; users, sessions, caches and artifacts remain separated. | A container label, read-only application prompt or an image scan alone. |
| G7 | Startup, outage, invalid config/TLS, reload and revocation do not silently open direct routes or use unapproved provider fallbacks. | Healthy-state tests alone. |
| G8 | Decisions and changes are attributable and tamper-resistant enough for the stated threat model; evidence storage does not become a new leak. | Full prompt/body logging, or logging nothing to avoid leaks. |
| G9 | Required legitimate developer workflows remain functional under the controls. | Making all requests fail or disabling the protected feature. |
| G10 | Conclusions are tied to tested source/config/image/topology, with unknowns and residual trust assumptions explicit. | A source test presented as proof of production containment or CUI compliance. |

For G3, examine the fundamental information-flow problem: a process with CUI access and freedom to construct arbitrary public requests can potentially disclose data through otherwise approved destinations. Demand an owner-approved release design, not a promise that the model will behave. Consider constrained brokers, verified minimal request schemas, separate public-retrieval workers without CUI access, approved internal mirrors and explicit release approval. The boundary between those workers also needs enforcement. Do not claim a text filter can reliably classify every transformed or context-dependent CUI value.

For encrypted traffic, record what the control can actually observe. A generic CONNECT tunnel does not imply application-body inspection. Do not silently introduce TLS interception or disable certificate verification; either requires explicit design and trust decisions. Destination checks must address every relevant redirect/connection, not just the first URL. [R10]

For G7/G8, establish the approved handling of policy/logging failures and existing connections after revocation. If auditable release is mandatory and its enforcement path is unavailable, do not silently continue unaudited release. Flag missing semantics as a requirement gap rather than inventing operational behavior.

### 4.3 Mandatory adversarial test-plan matrix

Plan these cases where applicable. Execution is conditional on the lab gate. Each row must end as `pass`, `fail`, `blocked`, `not_run`, or `not_applicable` with evidence/reason. Select bounded representative variants; do not claim exhaustive coverage.

| Case | Challenge | Required observation |
|---|---|---|
| T01 | Remove/change proxy variables, use an ignoring library/raw client, vary NO_PROXY and child-process environment. | Actual network enforcement still prevents unauthorized direct access; permitted mediated requests work. |
| T02 | Exercise available IPv4/IPv6, DNS paths, alternate ports/protocols, host gateways and additional interfaces. | Unauthorized paths are denied at the relevant boundary, not merely unsupported by the chosen test client. |
| T03 | Use mock redirects, DNS changes, private/link-local targets, authority mismatches and hostname/URL edge cases. | Policy holds at the actual destination and each hop; never contact a real metadata service. |
| T04 | Place synthetic restricted markers in query/path/headers/body/filenames and an allowed-destination request; use bounded transformed variants. | Release rules prevent the prohibited flow; the mock recipient confirms delivery or non-delivery. Marker recognition alone is not a general CUI guarantee. |
| T05 | Exercise permitted TLS/tunnel/CONNECT/WebSocket paths and invalid certificates. | No unsupported inspection claim, certificate bypass, arbitrary tunnel or unexpected credential forwarding. |
| T06 | Exercise parent, auxiliary and fallback model routes and hosted-tool configuration with local synthetic services. | Every route is inventoried and restricted; unavailable approved endpoints do not trigger an unapproved route. Upstream behavior remains separately verified/unknown. |
| T07 | Supply hostile synthetic web/tool/repository instructions requesting policy changes or data release. | Deterministic controls block forbidden actions even when the agent attempts them; test explicit tool requests as well as bounded end-to-end agent trials. |
| T08 | Simulate package/plugin/hook/LSP/build activity, alternate registry/Git URLs and install-time network use. | Runtime and bootstrap paths follow the intended policy; inspect host-side helpers and artifact integrity. No real unapproved installs. |
| T09 | Attempt access to synthetic protected mounts, sockets, capabilities, config/CA files and host-service stand-ins. | The workload principal cannot change enforcement or acquire host/other-session access; no actual host escape attempts. |
| T10 | Exercise an unauthorized lab client against APIs, admin routes, sessions, browser-origin paths and published ports. | Authentication, authorization and session boundaries hold on the actual exposed path. |
| T11 | Interrupt mock gateway/resolver/policy dependencies; test startup/reload, malformed config, invalid TLS and revocation. | Approved fail-closed behavior holds, including established-connection semantics and recovery. No unapproved fallback. |
| T12 | Attempt lower-trust project/environment overrides, policy writes and provider changes. | Trusted policy wins in the deployed version; ineffective or unsupported settings are detected. |
| T13 | Run two synthetic users/sessions and inspect permitted transcript/cache/log/artifact outputs. | No cross-session access or unapproved storage/export; useful audit metadata remains without gratuitous payload retention. |
| T14 | Correlate client, gateway and mock-receiver observations, including a denied and an allowed request. | Test and observation channels are alive; an empty proxy log is not accepted as proof of no bypass. |
| T15 | Run approved normal model, public-doc retrieval, dependency acquisition and local-IPC workflows as applicable. | Necessary behavior works without broadening release rules or bypassing the boundary. |
| T16 | Recheck a shared assumption using a second evidence source and compare source intent with effective deployment. | Common-mode blind spots and lab/deployment differences are tested or explicitly left unresolved. |

**Harness validity:** use the actual enforcement implementation/topology, not only an HTTP-client mock. Identify the principal/namespace making each request. A negative test needs a functioning mock destination, valid synthetic request and independent confirmation that the observation path works, for example from a separate authorized reference client within the lab. A DNS error, dead sink, broken test or absence of a log is not proof of enforcement. A positive control must not require opening the target's denied route. Record all lab deviations from deployment. Docker networking/port-publishing rules can affect host-firewall assumptions; verify the actual runtime path. [R11]

**Evidence receipt:** case/property/finding ID; snapshot/config/image/topology identity; principal; lab authorization; synthetic fixture ID; exact command or runner case; finite limits; expected result; actual result/exit status; trusted observation references; applicability and limitations. Store only in the approved destination. When safe and authorized, use a known-vulnerable baseline or a temporary mutant in a disposable copy to show the regression detects the failure. Never weaken a live deployment or the lab's outer boundary.

## 5. Two genuinely separate first passes

Spawn exactly the two named roles using the installed Codex orchestration interface. Do not invent tool parameters. Each receives the neutral contract, approved source access, active profile and their own role instructions:

- **Breaker:** forward from lower-trust input to forbidden outcome; attack paths and bypasses.
- **Builder:** backward from required property to every enforcement point; independent defect hunting, not implementation defense.

Do not forward findings until **both** ledgers are complete. Prefer fresh contexts without inherited findings and role-private notes. Keep findings out of shared target files. If the runtime forks full conversation history, or shared artifacts were read, record degraded independence. Separate contexts/worktrees help with methodology and source consistency but are not automatically confidentiality boundaries. Use snapshots only with authorized filesystem access and include user changes.

Do not change providers to obtain diversity. Both agents remain Codex and may share failure modes. Different prompts, models from the same provider or reasoning levels do not prove independent judgments. Require evidence from different routes and the final common-mode check. If either role cannot be instantiated, report an incomplete dual-agent run; do not simulate it with two parent personas. No nested subagent teams.

Require each first pass to return its own threat/invariant map, examined/unexamined surfaces, ranked evidence-led findings, falsifiers, negative tests and legitimate-use controls. The parent must not coach one agent with the other's progress.

## 6. Bounded cross-examination and adjudication

After both first passes, exchange ledgers. Round 1: independently re-read the other agent's primary evidence and challenge every material claim. Use `supported`, `narrowed`, `contradicted`, or `needs_validation`; link to its ID and state the decisive observation or missing fact. Round 2: exchange only challenges, rebuttals and new evidence. Stop earlier when no decisive evidence is added. No debate-for-debate's-sake, vulnerability quotas or pressure to agree.

The parent checks disputed source and available independent observations. Do not decide by voting, confidence scores, eloquence or model agreement. Keep a credible unresolved concern even when only one agent raised it. A failed reproduction is not itself a refutation.

Consolidate related claims into stable `SEC-001` IDs while retaining original B/D IDs. Keep separate dimensions:

```text
claim_type: security_defect | correctness_defect | requirement_gap | hardening
finding_state: confirmed | needs_validation | refuted
evidence_kind: runtime_reproduction | conclusive_static_trace | assumption_only
remediation_state: not_started | patch_applied | validated | unresolved | deferred
coverage_state: pass | fail | blocked | not_run | not_applicable
```

A confirmed defect requires a concrete property, source/config identity, lower-trust principal and controllable input for security claims, reachable mechanism, affected boundary and supported consequence. Conclusive static evidence can establish a source defect; it cannot prove unknown deployment configuration. Separate observed impact from worst-case assumptions. Give demonstrated severity to confirmed security defects; keep serious unverified risks prominent with conditional impact and validation priority, not a fabricated definitive score.

Each finding records: stable/original IDs; dimensions above; property; actor/prerequisites; source/config anchors; input-to-outcome trace; observations versus assumptions; evidence/receipt references; what would falsify it; impact/priority; peer challenges/disposition; narrow fix; regression expectation; residual risk and owner decision needed. A requirement gap is not silently upgraded into an exploitable vulnerability. A refuted finding remains traceable.

## 7. Repair and reattack (fix mode only)

Only after both investigations and the finding gate, give `secops-builder` exclusive ownership of a small authorized fix batch. `secops-breaker` remains target-read-only; any independent test file goes in authorized separate scratch. The parent coordinates; no concurrent edits to target source/tests/config. Never change this skill, agent files or review criteria as a way of passing the target audit.

1. Builder states the confirmed root cause, invariant, authoritative enforcement point, minimal change, preserved functionality, test plan and rollback. Changes to the trust model/release policy or additional privileges/dependencies require a separate owner decision; local fix permission does not authorize weakening protection.
2. Capture a discriminating pre-fix failure in the verified lab where feasible. Pin the regression and fixtures before implementation. If not executable, label the missing baseline evidence and provide a static patch/recipe; do not invent a red test.
3. Patch only authorized files, preserving user edits. Run allowed targeted tests, positive controls and relevant broader checks. Record exact changes, failures, passes and source/config identity. Installing a dependency or changing a live firewall is not an implied part of this step.
4. Freeze the patched state. Before receiving the builder's persuasive rationale, have Breaker derive attack variants from the invariant and inspect the actual diff/state. Check original failure, alternate clients/entrypoints, state/error cases, side effects and legitimate behavior. A fresh agent instance of the same role is optional within the two-role limit; disclose context inheritance.
5. Exchange concrete challenges. Builder must produce evidence, narrow a claim or patch again. Every new patch invalidates affected earlier results and must be reattacked. Parent independently checks receipts/observations rather than accepting self-reported success.
6. Cap the **entire run at two patch/reattack cycles** by default, not two per finding indefinitely. When the cap is reached, report unresolved holes. An applied patch is not a validated fix; a validated local fix is not deployment authorization.

Unconfirmed findings remain validation work unless the owner separately authorizes a clearly labeled hardening change. No hiding failures by changing expected results, removing features, enlarging allowlists, disabling TLS checks, suppressing accountability or altering the threat model. Without a safe runtime, source changes may be proposed or explicitly authorized, but remain `patch_applied`/unverified rather than `validated`.

## 8. Common-mode challenge and closure

Before closure, independently ask each role: **"What assumption could make both Codex reviewers wrong, and what different observation would expose it?"** For this profile, prioritize one route outside the proxy's ordinary logs, a deployed-versus-declared control difference, and the distinction between approved destination and approved data release. Check the answers against available primary evidence; preserve what cannot be checked.

Return:
1. **Scope and authorization:** goal, mode/profile, approved input scope, reviewed source/deployment identities, assumptions and exclusions; no secret values.
2. **Boundary/invariant map:** actual flows, enforcement owners, data-release decisions and coverage, including missing deployment or provider facts.
3. **Findings and debate:** supported defects, refutations, conditional risks, unchallenged claims and unresolved disagreements with evidence links.
4. **Fixes and tests:** exact changed files, baseline/post-fix receipts, independent reattack, positive controls and residual/rollback concerns.
5. **Decision gates:** separate audit completion, local patch validation and deployment readiness. Use `not_assessed`, `blocked`, or `candidate_for_owner_review` for deployment; none is an authorization to process CUI.

Do not say "secure," "CUI compliant," "zero leaks," or "production approved" from this run. No confirmed findings is not proof of absence. State which exact cases and environments passed and which did not run. A missing runtime test may leave an otherwise completed static review with incomplete deployment validation; do not blur the two.

Default blockers for real CUI use include unknown review/provider handling authorization, unknown data-release rules, unproven mandatory mediation, a confirmed unresolved boundary bypass, or missing deployment validation for the claimed environment. These are engineering review gates, not a complete compliance assessment. The authorized organizational owner makes release and risk-acceptance decisions. [R8–R9, R12]

## 9. Installation and invocation

Keep these three files at the project root:

```text
.codex/agents/secops-breaker.toml
.codex/agents/secops-builder.toml
.agents/skills/adversarial-secops/SKILL.md
```

For personal availability use `~/.codex/agents/` and `~/.agents/skills/`. Check discovery in the installed CLI; restart if necessary. The agent files deliberately contain no model, provider, permission or sandbox overrides. Current Codex subagents inherit parent permissions/provider; behavioral read-only instructions are not an independently enforced sandbox. Configure actual restrictions and approved endpoints in the parent/managed environment. Do not weaken them to load these roles. [R1–R2]

Example request after the pre-read authorization is established:

```text
Use $adversarial-secops on /absolute/path/to/the/project.
Profile: cui-agent-gateway.
Mode: audit-and-fix.
Goal: Preserve developer functionality while proving that agents, their tools,
child processes, libraries and supporting services cannot bypass the approved
information-flow boundary or release sensitive information through unapproved
channels. Review ingress as well as egress and all relevant data stores.
Review input authorization: <approved nonsensitive copy or owner approval reference>.
Allowed edits: local source, tests and checked-in deployment/configuration files
inside this repository; preserve existing changes. No commits, pushes, deployment,
live infrastructure changes, additional providers, dependency installation or real CUI tests.
Testing: synthetic data only in an independently isolated, authorized lab.
If the lab is unavailable, do static review and label runtime validation blocked.
Treat missing architecture, provider approvals and baseline details as unknowns.
Run independent first passes, evidence-based cross-examination and at most two
patch/reattack cycles. Return findings, evidence, changes and unresolved gates.
```

For another project use `Profile: general` with its own goal and invariants. For review only use `Mode: audit` and no allowed edits. The same pre-read and safe-execution rules apply.

## 10. Primary references and version discipline

Consulted 2026-10-27. These are methodology/schema references, not evidence about the target deployment. Prefer the installed version's primary documentation and exact source revision. Do not fetch them from a sensitive environment unless its research channel is approved. The review contract and test matrix above are this skill's proposed engineering workflow, not a verbatim standard or a claim that these references endorse this package.

- **R1 — OpenAI, Codex subagents:** <https://learn.chatgpt.com/docs/agent-configuration/subagents>. Standalone role files, orchestration, inheritance and permission limits.
- **R2 — OpenAI, Build skills:** <https://learn.chatgpt.com/docs/build-skills>. SKILL.md metadata and local discovery.
- **R3 — OpenCode security model:** <https://github.com/anomalyco/opencode/blob/dev/SECURITY.md>. Read the deployed revision; app permissions are not the isolation boundary. Upstream's accepted threat model need not match this deployment's obligations.
- **R4 — OpenCode permissions:** <https://opencode.ai/docs/permissions/>. Tool-level behavior; do not equate it with containment.
- **R5 — OpenCode networking:** <https://opencode.ai/docs/network/>. Proxy variables, certificates and necessary local IPC considerations.
- **R6 — OpenCode plugins:** <https://opencode.ai/docs/plugins/>. Startup/plugin/dependency paths to inventory.
- **R7 — OpenCode policies:** <https://opencode.ai/docs/policies/>. Version-dependent policy support; verify the actual installed release.
- **R8 — NIST SP 800-171 Rev. 3:** <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html>. Information-flow, boundary and data-protection engineering references; applicability and revision remain owner/contract decisions.
- **R9 — NIST SP 800-190:** <https://csrc.nist.gov/pubs/sp/800/190/final>. Container risk and isolation review context.
- **R10 — OWASP SSRF Prevention Cheat Sheet:** <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>. Destination validation and redirect/network-layer considerations.
- **R11 — Docker packet filtering and firewalls:** <https://docs.docker.com/engine/network/packet-filtering-firewalls/>. Verify actual bridge/port-publishing/firewall behavior rather than assuming host rules apply.
- **R12 — OWASP AI Agent Security Cheat Sheet:** <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html>. Least privilege, data boundaries, adversarial cases and validation evidence.
