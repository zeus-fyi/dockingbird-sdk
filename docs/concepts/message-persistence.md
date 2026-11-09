---
title: Message persistence
summary: Where bus messages and deliveries are stored, what survives a restart, an update, a roll to a new engine and a take-over, what each delivery state means, and when old message bodies expire.
audience: daily
commands:
  - stop
  - inbox
  - read
  - clean
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Every message on the bus is a row in a PostgreSQL database that Dockingbird runs. A restart of an agent, of Dockingbird or of your computer leaves the rows where they were. This page says where they live, what each kind of restart keeps, how a delivery ends, and when a body is removed.

## Where messages are stored

Messages, their deliveries, threads and questions are rows of the PostgreSQL database in the Docker volume `dockingbird-state`. The same volume holds the agents' copies of your branches ([home layout](../reference/files/home-layout.md)).

| Command | What happens to the messages |
|---|---|
| `dockingbird stop` | Nothing is lost. Every message, delivery and open question stays in the volume. |
| `dockingbird clean NAME` | Deletes the stopped agent's copy, results and history, as [clean and uninstall](../guides/clean-and-uninstall.md) describes. |
| `dockingbird clean --all` | Removes the volume, so every message goes with it. It is the only command that does. |

A message is an envelope and a body. The envelope holds the sender, the kind, the subject, the thread and the timestamps. The body is the text and the payload. The two age out separately, as the retention section below shows.

## What a restart keeps

| Event | What survives |
|---|---|
| An agent's turn ends or its tool crashes | Its thread, its deliveries and its open questions. `dockingbird claude --as NAME` or `start --as NAME` picks the agent up where it left off, and a message sent to an ended agent waits until then. |
| Dockingbird's coordinator restarts, or you run `stop` and then `start` | Every message. An open question still takes your answer, and a question an agent asks during the restart is recorded once the restart ends. |
| The idle stop, 30 minutes with no agent running | Every message. The next command turns Dockingbird back on. |
| A rolling update | The same container, session and conversation, with the agent's deliveries and open questions kept. See [updates](../guides/updates.md). |
| An update that changes the engine | Each bus or screen agent moves to a new container at its next stopping point and keeps its name, session and conversation. Deliveries belong to the session, so the new container finds them. |
| Your computer restarts | The volume is on Docker's disk, so the rows are there when Docker starts again. |

At a rolling update, the agent's supervisor passes the set of deliveries it already fed to the agent to the supervisor of the new release, and settles the ones the agent had answered. You see the effect and not the hand-over: the agent is not fed a message twice, and an open question stays open.

### A take-over

A take-over is a new session that continues an ended one, for example when you pick an agent up with `--as NAME`. Each delivery still pending or accepted for the earlier session gets a successor for the new session, and the original settles as `superseded`. The successor keeps the original's read time. Its reminder count starts over, so the new session is reminded as a fresh target.

### Delivery is at least once

A restart can repeat a step, so each step is safe to repeat.

- A repeated reply settles nothing more.
- A repeated surface of a delivery counts once.
- A retry of a send reuses its key, so the bus returns the first result.

A marked message, one that stays open until its target replies or acknowledges, survives a container restart, a take-over and a rolling update. A session that takes over is reminded as a new target. The sender of an overdue message is not told twice. [Reliable messages](../guides/reliable-messages.md) describes marked messages.

## Delivery states

A message goes to one or more targets, and each target holds one delivery of it. A delivery has one state at a time.

| State | Meaning |
|---|---|
| `pending` | The target has not taken the message up yet. |
| `accepted` | The target took the work up and has not finished. |
| `responded` | The target answered it, acknowledged it, or read it when it needed no answer. |
| `declined` | The target refused it. |
| `withdrawn` | The sender took the message back. An accepted delivery stays `accepted` until its work stops, then settles `withdrawn`. |
| `expired` | The delivery stayed `pending` past its expiry. Accepted work never expires. |
| `superseded` | A take-over replaced it with a successor delivery. |

When a delivery settles, it records what settled it. The outcome is `accepted`, `responded`, `done`, `needs_info`, `declined` or `read`. A read settles an informational message as `responded` with the outcome `read`. A marked message needs a reply or an acknowledgment, and a read never settles it.

`dockingbird inbox --json`, `wait --json` and `read --json` carry the delivery's `state`, `surface_count`, `reply_required`, `reminder_due` and `ack_due_at` beside the row.

### Limits on pending work

- A delivery that stays `pending` for 7 days expires. `MESSAGE_EXPIRY_DEFAULT_DAYS` sets the figure, within 1 to 90 days. A sender that names no expiry gets it.
- A target session holds at most 200 pending deliveries. With 200 waiting, the next send to it is refused with `PROJECT_BUSY` and the reason `BACKPRESSURE`. `PENDING_DELIVERIES_MAX` sets the figure, within 10 to 10,000.
- An agent's turn report settles the report it sent before at the same priority. A home that runs a swarm for weeks therefore holds one pending report per session and priority. The earlier report stays readable by its id and in its thread.

## Retention

A retention pass runs at the start of a host command, at most once an hour, and deletes at most 10,000 rows per table. A large backlog takes several passes. The sweep that marks a body expired runs more often, at every host command and every 60 seconds in the coordinator container.

| What | Default | Bounds | Setting |
|---|---|---|---|
| Request receipts, the records that make a retried send return its first result | 90 days | 3 to 3,650 days | `DOCKINGBIRD_REQUEST_RECEIPT_RETENTION_DAYS` |
| Events, the bus's replay history | 30 days | 1 to 3,650 days | `DOCKINGBIRD_EVENT_RETENTION_DAYS` |
| Message bodies | 90 days | 1 to 365 days | `DOCKINGBIRD_MESSAGE_BODY_RETENTION_DAYS` |
| Rows deleted per table in one pass | 10,000 | 1 to 1,000,000 | `DOCKINGBIRD_RETENTION_PRUNE_BATCH_ROWS` |

A message body is marked expired 90 days after its message was created. A read of it is then refused with `CONTENT_EXPIRED`, and the next retention pass deletes the body rows. The envelope, with the sender, kind, subject, thread and timestamps, stays in the database.

The product design also names 365 days for summary metadata. The retention pass of this release deletes receipts, bodies and events only, so it deletes no envelope.

A closed expectation, one that [`dockingbird expect`](../guides/reliable-messages.md#expect-a-message-that-has-not-arrived-yet) registered, is deleted 90 days after it closed, as bodies are.

A body expiry does not touch work in flight. A pending delivery expires on its own 7-day schedule, and accepted work never expires.

### Change the retention

Retention is a runtime setting. Set it in the shell that runs `dockingbird`, then restart Dockingbird so it reads the new value.

```bash
export DOCKINGBIRD_MESSAGE_BODY_RETENTION_DAYS=30
dockingbird stop
dockingbird status
```

Dockingbird passes every exported setting to the containers that read it. After you change one, the next command says `Dockingbird is running with other settings than this terminal's.` and names `dockingbird stop`. The command after `stop` starts Dockingbird with the new value. [The environment variables page](../reference/environment-variables.md) has the rules for a setting.

A value outside its bounds stops the command before it runs.

```text
DOCKINGBIRD_MESSAGE_BODY_RETENTION_DAYS must be a whole number from 1 to 365.
Set a value in that range, or unset the variable, then run this again.
```

Shortening the body retention expires the bodies older than the new figure at the next pass. Lengthening it does not bring back a body that already expired or was deleted. The hourly interval of the retention pass and the 60-second interval of the message sweep have no setting.

## Related pages

| Page | What it adds |
|---|---|
| [Agents and the bus](agents-and-the-bus.md) | How a task reaches an agent and its answers come back. |
| [Reliable messages](../guides/reliable-messages.md) | Marks a message so it stays open until it gets a reply. |
| [Updates](../guides/updates.md) | Rolls a running home to a new release. |
| [Backup and restore](../guides/backup-and-restore.md) | Says what the `dockingbird-state` volume holds. |
