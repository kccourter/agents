# Project Agent Instructions — Example

Adapt deliberately before installing. Resolve the actual repository/worktree
and any governing workspace instructions; do not assume a parent `../AGENTS.md`
exists. Record verified paths or the project's documented lookup procedure for
the shared workflow and workspace rules, using code paths that survive the
chosen layout.

Keep only consequential project constraints that are easy to miss:

- Ownership and public contract boundaries.
- Runtime/environment, data/units, hardware, or other correctness invariants.
- Required validation gates and canonical command/document locations.
- Local commit and remote-action policy, where it differs from shared defaults.

Reuse the adopted workflow's proportional lanes and existing authorization.
Local helpers, tests, refactors, and bounded investigation within an accepted
outcome do not need repeated approval. Document deliberate local overlays here;
keep setup guides and architecture descriptions in their canonical docs.
