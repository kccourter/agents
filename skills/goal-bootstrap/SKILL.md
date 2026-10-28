---
name: goal-bootstrap
description: Set up a durable goal index and the planning surfaces needed for an authorized feature or coordinated change. Skip routine local fixes and maintenance that need no goal folder.
---

# Goal Bootstrap

Create only the durable structure useful for the requested work. Read effective
repository instructions and inspect existing goal names and indexes first.
Reuse an existing goal when it owns the outcome. This skill creates planning
artifacts; product implementation requires authorization for that outcome.

Use the project's naming convention. The default for new goals is
`docs/goals/NN-GOAL_NAME/`, using uppercase snake case and the next number after
the highest matching numbered directory. Preserve legacy directory names.

Start from [templates/goal-readme.md](templates/goal-readme.md). Capture the
outcome, scope, acceptance checks, authorization, owner/worktree, current
position, and canonical evidence. For one cohesive feature, one implementation
contract may suffice. For dependent increments, use
[templates/plan-00.md](templates/plan-00.md) as
`plans/PLAN-00-roadmap-and-inventory.md`; identify producer/consumer dependencies
and meaningful gates without elaborating uncertain downstream work.

Use `plans/` for contracts, `records/` for execution receipts, and `reference/`
for reusable findings. Create directories/indexes as they become useful or as
local policy requires. [templates/records-readme.md](templates/records-readme.md)
is optional. Do not populate empty boilerplate files to satisfy a fixed tree.

Bootstrap, targeted investigation, and preparation of the next ready contract
can continue under the same authorization. Do not insert a pause between these
thinking stages. Request a decision only when requirements or consequential
boundaries cannot be resolved from existing authorization. If implementation
is already authorized, continue it through the applicable implementation
workflow; a bootstrap-only request remains planning work.
