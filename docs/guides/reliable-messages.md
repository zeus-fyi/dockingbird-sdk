---
title: Reliable messages
summary: Mark a message so it stays open until its target replies, demand a reply to a task, expect a message and be alerted when it never arrives, and send one message to a group of agents.
audience: daily
commands:
  - send
  - send --requires-ack
  - send --reply-required
  - send --all
  - send --role
  - send --swarm
  - expect
  - inbox
  - read
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Reliable messages

A plain message is read once and then it is done. A message that must be answered stays open until its target replies to it or acknowledges it, shows up again while it waits, and tells the sender once when the deadline passes. This guide marks such messages, registers a message you expect, and sends one message to a whole group.

## Before you start

- You know how to [delegate a task](delegating-tasks.md): `start`, `send`, `inbox` and `read`.
- At least one agent runs. A mark needs a target that can reply.

## 1. Mark a message

A message is marked in one of two ways, and the kind of message decides which.

| You want | Option | Kinds it takes |
|---|---|---|
| Only a reply or an acknowledgment settles it | `--requires-ack` | `status`, `decision`, `review_result`, `alert`, `answer`, `question` |
| A reply to a piece of work, whatever the turn does | `--reply-required` | `task_request`, `handoff`, `review_request` |

A mark on any other kind is refused. A plain `dockingbird send NAME TEXT` with no open question makes a `task_request` from your text, so `--reply-required` fits it as it is.

```bash
dockingbird send claude-1 --reply-required "Run the migration check and tell me the result."
```

Done when the line names the kind, the agent and the message.

```text
Sent task_request to claude-1 (message <id>).
```

Message id `SENT`. To mark a `status`, `decision` or another kind, give the kind and its payload: `dockingbird send claude-1 --kind decision --payload '{"decision_key": "db", "revision": 1}' --requires-ack "Use Postgres."`. `dockingbird send -h` lists each kind's payload keys.

### What settles a marked message

- The target replies. A reply is a message of any kind whose reply-to is the marked message, sent by the target. An agent replies with `bus_send` and `reply_to`.
- The target acknowledges it with `bus_ack`.

A read never settles a marked message. A task sent with `--reply-required` is not settled when the agent's turn ends: the agent's own turn summary settles nothing. A reply from a third agent, a reply to an unmarked message and a status in the thread with another parent settle nothing.

A `question` keeps its own rule: an `answer` from the target, or a reply from you, closes it. A message you send without a mark keeps its kind's default.

## 2. What happens while it is open

The target sees the message again on a schedule, on every path an agent reads from. Each reminder feeds the delivery again with the note `Reminder: this delivery is still unanswered.`

| Item | Value |
|---|---|
| Time between reminders of one message | 300 seconds (`SURFACE_REMINDER_INTERVAL_S`, 60 to 3,600) |
| Reminders per message | at most 2 (`STOP_REMINDERS_MAX`, 0 to 5) |

A reminder never accepts, settles or expires the message. The agent's stop hook holds the agent at the end of a turn while a P0 or marked message has been shown fewer than 2 times, so a reminder cannot trap it in a loop.

At the deadline, the sender gets one `alert` in the message's thread. Its subject starts with `reply overdue:`. The alert is sent once, because the alert in the thread is the guard against a second one.

| Message priority | Deadline after the send | Setting |
|---|---|---|
| P0 | 120 seconds | `DOCKINGBIRD_P0_ACCEPTANCE_DEADLINE_S` (10 to 3,600) |
| P1 | 900 seconds | `DOCKINGBIRD_P1_ACCEPTANCE_DEADLINE_S` (60 to 86,400) |
| P2 | 14,400 seconds | `DOCKINGBIRD_P2_ACCEPTANCE_DEADLINE_S` (300 to 604,800) |
| P3 | 86,400 seconds | `DOCKINGBIRD_P3_ACCEPTANCE_DEADLINE_S` (3,600 to 604,800) |

P0 must stay below P1, and P1 below P2. A value that breaks the order stops the command before it runs. [Environment variables](../reference/environment-variables.md) says how a setting reaches Dockingbird.

When the sender is you, the alert reaches every client session of the project that has not ended, so it reaches `dockingbird inbox` as an `alert` row.

### When the check runs

The check that sends overdue alerts runs at the start of every host command except `status`. It also runs every 60 seconds in Dockingbird's coordinator container, so a home with no command typed still sends them. It stops when the coordinator stops with no agent running, and the next command runs it again.

### See it in the inbox

`dockingbird inbox --json`, `wait --json` and `read --json` add four fields to a delivery.

| Field | Value |
|---|---|
| `surface_count` | how many times the message was shown to its target |
| `reply_required` | `true` when the sender demanded a reply |
| `reminder_due` | `true` when the message is marked and its next reminder is due |
| `ack_due_at` | the deadline, as an RFC 3339 UTC time, or `null` |

Every message sent before 0.15.24 has `reply_required` `false`.

## 3. Expect a message that has not arrived yet

`dockingbird expect` registers the message you wait for. When it arrives, the expectation closes. When none arrives by the due time, you get one alert.

```bash
dockingbird expect status --from test-1 --prefix tested --within 1800
```

`KIND` is the kind of message, `--from` the agent that sends it, `--prefix` the start of its subject and `--within` the seconds from now. Without `--prefix`, any subject matches. `--since TIME` sets the earliest send time that counts, as a time with an offset. Done when the line names the kind, the agent and the due time.

```text
Expecting a status from test-1 whose subject starts with "tested", by <time> (expectation <id>).
```

Message id `EXPECTED`. A message that already arrived since `--since` closes the expectation at once. `--within` must be above 0 and at most the message expiry, 7 days by default (604,800 seconds).

The alert is an `alert` row in your inbox. Its subject is `expected row missing: KIND from NAME`, with `: PREFIX` added when you gave one.

| Command | What it does |
|---|---|
| `dockingbird expect --list` | Lists your open expectations, newest first (`EXPECTATIONS`). |
| `dockingbird expect --list --closed` | Lists every state. |
| `dockingbird expect --withdraw ID` | Takes an open expectation back. It sends no alert (`EXPECTATION_WITHDRAWN`). |

Closed expectations are deleted 90 days after they close. An agent registers the same watch with `bus_expect`, and lists and withdraws with `bus_expectations` and `bus_expect_withdraw` ([the agent's bus tools](../reference/fleet-tools.md#bus-tools-for-reliable-messages)).

## 4. Send one message to a group

One `send` can reach a group of live agents instead of one name.

| Command | Who gets it |
|---|---|
| `dockingbird send --all TEXT` | every live agent of the project |
| `dockingbird send --role ROLE TEXT` | every live agent of that role |
| `dockingbird send --swarm SWARM TEXT` | every live agent of that swarm |
| `dockingbird send --swarm SWARM --role ROLE TEXT` | every live agent of that role in that swarm |

```bash
dockingbird send --role reviewer "Freeze merges until I say so."
```

Every word after the options is the message. A group message is a `status` unless `--kind` names another, and it answers no question. Done when the line counts the agents.

```text
Sent status to 2 agents, role reviewer (message <id>).
```

Message id `SENT`. The group is one message with one delivery per agent. Each recipient must pass the same `send_to` check as a send by name. An agent's own `bus_send` takes `all`, `swarm` and `role` the same way. `RECIPIENTS_MAX` bounds a send's fan-out only when you set it, and 0 bounds nothing.

A group with no live agent is refused with `GROUP_EMPTY`, so a message never goes to nobody. A group send reaches the agents live at the send and not the ones that start later.

## 5. A message to a screen agent

An agent that runs on a screen of its own gets a message as typed text. Dockingbird pastes the text and types Enter 1 second later (`TUI_PASTE_ENTER_DELAY_MS`, 1,000 milliseconds), because Claude Code 2.1.319 drops an Enter that lands with the paste when a line ends in a picture's file name such as `.png` or `.jpg`.

| Rule | Value |
|---|---|
| Delay from the paste to Enter | 1 second |
| Enter typed again while the paste sits unsent | every 3 seconds, at most 2 times |
| Window for the tool to take the message | 10 seconds |
| End of a message to Claude Code | one space, so a last word such as `:72` or an `@` name does not open a list that takes the Enter |
| A tab in the message | arrives as four spaces |

A message the tool never takes is emptied from the box, unless a person typed in it. The sender is told: `No prompt named the paste within 10 s; Enter was typed again, and the box emptied unless a person typed in it.` (`TURN_UNSIGNALLED`). Dockingbird types nothing into a box that holds your own unsent text.

## When it fails

- `--requires-ack` or `--reply-required` on a kind that does not take it is refused, and nothing is sent. Use the kind in the table in section 1.
- [`SEND_GROUP_CONFLICT`](../troubleshooting.md#send_group_conflict) says `--all` takes no `--role` or `--swarm`. Send to part of a swarm with `--swarm` and `--role`.
- [`SEND_GROUP_NO_REPLY`](../troubleshooting.md#send_group_no_reply) says a group takes no `--reply-to` and no `--kind answer`. Reply to the agent that asked by its name.
- `GROUP_EMPTY` says no live agent belongs to the group. Check `dockingbird status`.
- With 200 deliveries pending for one agent, the next send to it is refused with `PROJECT_BUSY` and the reason `BACKPRESSURE`. Wait for the agent to work through them.
- [`TURN_UNSIGNALLED`](../troubleshooting.md#turn_unsignalled) says a screen agent never took a message. Send it again.
- [`EXPECTED`](../troubleshooting.md#expected), [`EXPECTATIONS`](../troubleshooting.md#expectations) and [`EXPECTATION_WITHDRAWN`](../troubleshooting.md#expectation_withdrawn) are the lines of `expect`.

What a restart keeps, and when a body expires, is on [message persistence](../concepts/message-persistence.md).
