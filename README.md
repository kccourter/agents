# Agentic coding

Optional shareable copies of coding workflow skills and guidance. Develop and
test the active skills in your installed `.codex/skills` directory and maintain
project guidance in its own workspace or repository. Copy useful reusable
artifacts here when they are ready to share with coworkers.

This repository is not required at runtime and does not govern another
project's documentation. Teammates may deliberately install selected skills
into their own `.codex/skills` directory and adapt the optional examples.

## Develop and share

Implement and validate workflow changes in the active installed skills and
the owning project's documentation first. Then select the reusable artifacts
worth sharing and copy them here. Review those copies for project-specific
details and personal information before distribution. There is no automatic
mirroring or requirement to keep installed files or project documents equal
to this repository.

The [development workflow](DEVELOPMENT_WORKFLOW.md) is an optional example of
proportional local fix/maintenance, cohesive-feature, and coordinated-change
lanes. The [user manual](users-manual.md) illustrates how to request and
complete work under that workflow. A project may adapt these documents to its
needs; its effective `AGENTS.md` files, local workflow, and current user
authorization guide execution.

The examples under `agents_md_files/` require deliberate adaptation:

- `dot_codex/AGENTS.md`: optional global guidance; excluded from skill installation.
- `workspace/AGENTS.md`: shared workflow location and local coordination rules.
- `project/AGENTS.md`: project invariants and actual instruction lookup paths,
  without assuming a particular parent/worktree layout.

Do not replace an existing global or project instruction file as a side effect
of installing skills. Preserve unrelated instructions and installed skills.

## Deliberate skill installation

The list below is the complete allowlist for sharing and installing skill
files from this repository: six workflow skills plus `distill`, `manager`, their
compatibility pointer, and referenced templates/checklists/guidance.
`implementation-audit` is separately maintained: do not copy, rewrite, or
delete it as part of this distribution. System, plugin, and other skills,
client configuration, credentials, and personal files are outside this
allowlist.

Review the selected repository copies against your installed files and
preserve local changes or a needed backup before installing. From this
repository root, the example below installs all allowlisted files. To install
fewer skills, remove every entry for the unchosen skill directories, retaining
all listed templates/checklists for each chosen skill.

```sh
workflow_source="$PWD"
workflow_target="${CODEX_HOME:-$HOME/.codex}/skills"
while IFS= read -r workflow_file; do
  mkdir -p "$workflow_target/$(dirname "$workflow_file")"
  cp "$workflow_source/skills/$workflow_file" "$workflow_target/$workflow_file"
done <<'ALLOWED_FILES'
architecture-review/SKILL.md
goal-bootstrap/SKILL.md
goal-bootstrap/templates/goal-readme.md
goal-bootstrap/templates/plan-00.md
goal-bootstrap/templates/records-readme.md
research/SKILL.md
research/references/scientific-debugging.md
research/templates/research-notes.md
increment-planning/SKILL.md
increment-planning/templates/increment-plan.md
implementation/SKILL.md
implementation/checklists/implementation.md
implementation/checklists/validation.md
review/SKILL.md
review/templates/pr-notes.md
distill/SKILL.md
distill/DISTILL.md
manager/SKILL.md
manager/references/dispatch.md
manager/references/task-evidence.md
manager/scripts/task_record.py
manager/scripts/task_evidence.py
manager/scripts/usage_report.py
manager/tests/test_task_evidence.py
manager/tests/test_usage_report.py
ALLOWED_FILES
```

Copy only the selected allowlisted files and preserve unrelated files; do not
use directory-wide deletion. Sharing copies back here follows the same allowlist.
`distill/SKILL.md` provides discovery metadata and guidance;
`distill/DISTILL.md` preserves older evidence links as a compatibility pointer.

The optional [scientific debugging reference](skills/research/references/scientific-debugging.md)
covers competing explanations, semantic preflight, first-divergence comparisons,
and portable replay evidence for ML or stateful systems. It adds no mandatory
stage to routine fixes. These files were copied from the validated active
research skill; project diagnostic tools remain in their owning repositories.

For a sharing or installation copy, validate skill frontmatter with the
client's skill-creator validator when available, check referenced files, run
`git diff --check` in the affected repository, and compare the selected source
and destination files to verify the transfer. Record relevant provenance and
intentional adaptations; this does not establish ongoing parity requirements.
A client that caches its skill catalog may need a fresh session to expose a
newly installed skill. Validate policy changes where they are active with
meaningful workflow scenarios: an existing bug needing a new regression test,
a cohesive feature, a consequential contract change, and bounded diagnostic
uncertainty. Do not build extra automation or require product tests solely for
a documentation edit.

## Manager and specialist profiles

The [manager skill](skills/manager/SKILL.md) coordinates bounded assignments,
model/effort selection, evidence checks, and completion. The five files under
`agents/` are optional copies of the installed role profiles. After inspecting
differences and preserving local changes, install the selected files into your
Codex home's `agents/` directory:

```sh
workflow_target="${CODEX_HOME:-$HOME/.codex}/agents"
mkdir -p "$workflow_target"
for workflow_role in workflow_manager workflow_researcher workflow_implementer workflow_debugger workflow_reviewer; do
  cp "agents/$workflow_role.toml" "$workflow_target/$workflow_role.toml"
done
```

These profiles do not change the root model, permissions, or global defaults.
Model/effort values are pilot candidates; check availability in your client.
For tools with native role selection, select the role by name. For the
collaboration adapter that exposes model/effort without a role selector, the
manager reads the profile and passes its settings/instructions explicitly.
See [dispatch guidance](skills/manager/references/dispatch.md) for the distinction
and how to verify actual worker settings. A current session may need a refresh
to expose newly installed skills or native roles.

Develop and validate these files in the active `.codex` first, then update the
selected sharing copies here. Project documents remain independently owned.

For durable recovery or repeatable measurement, the manager includes optional
standard-library helpers. Keep one `agent-task` block in an existing project
record, derive a brief, capture authorized checks with evidence identities, and
report usage for explicitly selected task turns including coordinator/setup.
Read [task evidence guidance](skills/manager/references/task-evidence.md) for the
schema, commands, tests, and coverage limits. Install the scripts, tests, and
references together when choosing this capability. Routine fixes do not require
a structured record; these helpers add no database, service, scheduler, or
global model/configuration changes.
