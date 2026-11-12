---
title: Next release, draft
summary: The draft notes of the next Dockingbird release, written as its changes land.
audience: daily
commands:
  - dockingbird status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Next release, draft

| | |
|---|---|
| Entries | Marked messages and the agents that must answer them |
| Released versions | [v0.6.5.md](v0.6.5.md) has its own page, and [v0.7.0 to v0.15.28](changes-v0.7.0-to-v0.15.28.md) share one page |
| Changelog | [CHANGELOG.md](../../CHANGELOG.md) |

## Marked messages

- A marked `status`, `decision`, `review_result` or `alert` opens its first turn with a note that it requires an acknowledgment or a reply. Before, the agent learned it at the reminder, a second turn. In a terminal session, the hold at the end of a turn now names the read and then the reply or `bus_ack`.
- `bus_ack` with the outcome `accepted` answers with a `next_step` member: the delivery stays open until it is acknowledged `done` or its required reply is sent. `declined` on an accepted delivery is refused with `VERSION_CONFLICT`.
- An agent whose message is open only at agents that ended at least 300 seconds ago gets one `alert` whose subject starts with `target ended:`. It tells the agent to send the work again with `supersedes`, or to tell its parent. A message of yours gets none. See [reliable messages](../guides/reliable-messages.md#2-what-happens-while-it-is-open).
- `bus_context` reports each delivery's own `reply_required`. It said `false` for every row.
- The operator's MCP tool `agent_send` takes `reply_required` and `requires_ack`. `reply_required` on a kind that is not `task_request`, `handoff` or `review_request` is refused before anything is sent, with the argument named.
- The rules every bus agent starts with now say which messages must be answered and that an agent with nothing left but a wait registers it with `bus_expect`, and the MCP server's opening text no longer asks for a report as an artifact unless one is asked for.
