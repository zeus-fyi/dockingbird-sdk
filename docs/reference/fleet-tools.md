---
title: Fleet tools
summary: The ten fleet tools an agent on a joined home gets beside its bus tools, with who each can reach.
audience: integrator
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Fleet tools

An agent whose tools include `bus_send`, started on a home that joined a control plane, gets these ten tools beside its bus tools. [The control plane concept page](../concepts/control-plane.md) explains the fleet, and [the team fleet guide](../guides/team-fleet.md) joins a computer.

## The ten tools

| Tool | What it does | Reach |
|---|---|---|
| `fleet_send` | sends a message; a `question` sent to the operator is listed by `dockingbird questions` on the control plane's home and answered there with `dockingbird answer ROW` | a fleet agent by its fleet name, an agent of the control plane's home by its name, or, with no `to`, `parent`, the operator on the control plane's home |
| `fleet_inbox` | lists the deliveries of the agent's fleet inbox, which sits beside its own inbox | the agent's own fleet inbox |
| `fleet_read` | reads one delivery | the agent's own fleet inbox |
| `fleet_ack` | acknowledges a delivery | the agent's own fleet inbox |
| `fleet_wait` | waits for a delivery | the agent's own fleet inbox |
| `fleet_thread` | works with a fleet thread | the agent's own fleet session |
| `fleet_withdraw` | withdraws a message | the agent's own fleet session |
| `fleet_artifact_put` | puts an attachment, text of at most 262,144 bytes, that a message can name | the agent's own fleet session |
| `fleet_artifact_get` | gets an attachment a message names | the agent's own fleet session |
| `fleet_whoami` | tells the agent who it is in the fleet | the agent's own fleet session |

The harness shows each tool's arguments with the tool.

## Names and inboxes

| Item | Rule |
|---|---|
| fleet name | the computer's label, a dash and the agent's name, such as `lab-notes-1` |
| label | one to eight lowercase letters or digits, starting with a letter |
| name length | at most 63 characters less the label and its dash, else `FLEET_NAME_TOO_LONG` |
| two inboxes | the agent reads its own inbox and its fleet inbox, the more urgent delivery first |
| a choice or a plan to approve | asked on the control plane first, and on the agent's own home when the control plane does not take it |
| no answer at the start | the agent starts and works on its home, with `FLEET_SESSION_NOT_OPENED`, and gets its fleet inbox once the control plane answers |
| status line | `fleet: <label>-<name>, heartbeat <age>, asks <n>`, `fleet: not open` or `fleet: none` under each running agent in `dockingbird status` |

## Bus tools for reliable messages

The `bus` tool set, the default for an agent, holds the tools that mark a message and watch for one. The harness shows each tool's arguments with the tool. [Reliable messages](../guides/reliable-messages.md) explains what each field does.

| Tool | Field | What it does |
|---|---|---|
| `bus_send` | `requires_ack` | a boolean; the message stays open until its target replies or acknowledges it; it takes the kinds `status`, `decision`, `review_result`, `alert`, `answer` and `question` |
| `bus_send` | `reply_required` | a boolean; demands a reply to a `task_request`, `handoff` or `review_request`, so the end of the target's turn does not settle it |
| `bus_send` | `reply_to` | the 36-character id of the message this one answers; a reply to a marked message settles the sender's delivery of it |
| `bus_send` | `all`, `swarm`, `role` | sends to a group instead of `to`: every live agent, a swarm, a role, or a role within a swarm |
| `bus_ack` | `delivery_id`, `expected_version`, `outcome` | records the agent's disposition of a delivery; `outcome` is `accepted`, `responded`, `done`, `declined` or `needs_info`, and `note` takes at most 120 characters; `accepted` answers with a `next_step` member, and `declined` on an accepted delivery is refused with `VERSION_CONFLICT` |
| `bus_expect` | `kind`, `sender`, `within_s`, `subject_prefix`, `since` | registers a message the agent expects; `within_s` is 1 to 604,800 seconds; one alert arrives if none comes in time; only a row sent after the registration closes it, unless `since` is earlier |
| `bus_expectations` | `closed` | lists the agent's open expectations, or every state with `closed` |
| `bus_expect_withdraw` | `expectation_id` | withdraws an open expectation |

## Limits

| Limit | Value |
|---|---|
| a fleet call's wait for its answer | 30 seconds |
| an agent's own fleet inbox read or heartbeat | 10 seconds |
| deliveries waiting for one agent whose home is asleep or offline | at most 200 |
| a fleet attachment | at most 1,048,576 bytes |
| fleet calls while the control plane is silent | refused at once, until the member reconnects within 40 seconds |

## What does not cross

| Item | Rule |
|---|---|
| a home's work, runs, claims and publication | stay on the home |
| a fleet thread and a home thread | two threads; a message sent on one store is never seen on the other |
| the home's own `questions` list | shows none of the fleet's questions |
| an agent of another home that has not joined | no bus route; see [an agent that manages other agents](../concepts/agents-and-the-bus.md#an-agent-that-manages-other-agents) |
