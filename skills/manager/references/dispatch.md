# Dispatch adapters and evidence

Profiles live in the active Codex home under `agents/workflow_*.toml`; the
manager skill is alongside existing installed skills. Use the actual configured
home (normally `~/.codex`), not a workspace-relative path assumption. Profile
`name`, `model`, `model_reasoning_effort`, and `developer_instructions` are the
values to use. Read only profiles needed by the task.

## This session's collaboration adapter

When `collaboration.spawn_agent` exposes `model` and `reasoning_effort` but no
`agent_type`, it does not select a native role file automatically. Read the
chosen profile, include its `developer_instructions` with the bounded task in
`message`, and supply:

```text
task_name: a unique task name
fork_turns: none
model: the selected profile's model
reasoning_effort: the selected profile's model_reasoning_effort
message: role instructions + concrete assignment + evidence/receipt destination
```

For this adapter, `fork_turns: all` inherits parent model/effort and does not
accept overrides. Reusing a child preserves its context/settings; do not claim
an in-place switch. Use a new bounded child when a new setting is needed.
Respect the tool's actual slot limit. An explicit assignment can choose a
different available model/effort when justified by evidence; record the reason.

## Native Codex roles

Where the spawn tool exposes native custom-agent selection, select the installed
role by name. Standalone user roles are discovered under `~/.codex/agents/`;
the required fields are `name`, `description`, and `developer_instructions`.
Role-file model/effort settings override explicit spawn values and defaults.
To evaluate a different setting, use a supported override path that is not
overridden by the selected role, such as a default agent with explicit settings
and the role instructions. Roles inherit parent permissions; a read-only role
instruction is not a separate sandbox. These details are documented in
[OpenAI's subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Do not assume TOML parsing or `codex features list` proves native discovery.
Fresh-process role discovery and actual dispatch are separate checks. A session
whose tool surface lacks native role selection can use the explicit adapter
above; report which path was tested. No global config edit is needed for it.

## Verify a routed run

For a pilot, locate each child's own rollout through `session_meta` parent/thread
identity and `source.subagent.thread_spawn.agent_path`. Inspect its
`turn_context.model` and `effort` for executed turns. Top-level
`token_usage_record` entries show actual response usage; join by thread/turn and
deduplicate `response_id`. The configured runtime setting plus completed
responses verifies the client execution path, not independent backend identity.
Parent spawn requests, worker self-description, and thread-summary settings
alone are insufficient. If traces are unavailable, say verification is limited.

Keep selected settings, timestamps/overlap, prerequisite revisions, check results,
and evidence paths in the existing receipt. Detailed logs belong in ignored
artifacts. Report input, cached input, and output separately; reasoning tokens
are a subset of output. Do not infer money or savings from tokens alone. Broader
telemetry automation and comparative evaluation can follow an observed need.
