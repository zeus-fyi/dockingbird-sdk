---
title: Start agents from your own Claude Code or Codex
summary: Install dockingbird mcp into your own harness so it starts agents, messages them, reads their replies and saves their results through eleven tools.
audience: integrator
commands:
  - mcp install
  - mcp install --check
  - mcp install --show
  - mcp install --connected
---

# Start agents from your own Claude Code or Codex

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

`dockingbird mcp` is an MCP server, over stdio, for the Claude Code or Codex you work in on this computer. Through eleven tools your harness starts agents in Dockingbird, sends them messages, reads what they send back, saves their results and stops them. Your harness starts the server. You never run it yourself. The tool table and arguments are also on [the integration reference](../reference/integration/mcp.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- Claude Code or Codex is installed, so `command -v claude` or `command -v codex` prints a path. Another harness takes step 3 instead.
- Your harness runs in the checkout whose configs you want, because the server works in whatever folder the harness runs in.

## Steps

1. Connect Dockingbird's tools to each harness it finds. For each one the command runs that harness's own `mcp add`, records the result, and prints the undo.

   ```bash
   dockingbird mcp install
   ```

   The step is done when the command prints these lines, once for each harness found.

   ```text
   Connected Dockingbird's tools to Claude Code: <path>
   To undo: claude mcp remove --scope user dockingbird
   ```

2. Check the recorded connections. The command reports a harness that lost them, a program that left your `PATH`, or a hand-made connection it cannot check.

   ```bash
   dockingbird mcp install --check
   ```

   The step is done when each harness reports this line and no "no longer has" line appears.

   ```text
   Claude Code already has Dockingbird's tools; nothing changed.
   ```

3. Connect another harness by hand. The definition below goes into that tool's MCP settings, and stdio carries the traffic. Afterwards you record it under the harness's name.

   ```bash
   dockingbird mcp install --show
   dockingbird mcp install --connected NAME
   ```

   Showing the definition connects nothing. A home other than the default adds an `env` entry with `DOCKINGBIRD_HOME` to it. The step is done when the first command prints this line, then the definition.

   ```json
   {"command": "dockingbird", "args": ["mcp"]}
   ```

   ```text
   Dockingbird's MCP server (stdio), for any tool's MCP settings:
   ```

4. Ask your harness to start an agent. It calls `agent_start` with a task, then `agent_wait`, `agent_read` and `agent_results` for the answer. Leave out `command` and Dockingbird chooses as `dockingbird start` does, taking the checkout's default command, else the default environment.

   ```text
   agent_start {"command": "review", "task": "Check the login flow"}
   ```

   The step is done when the reply names the new agent, such as review-1, and the command that applied.

## The eleven tools

| Tool | Required | Optional | What it does |
|---|---|---|---|
| `agent_start` | none | `command`, `task`, `name`, `harness` (`claude` or `codex`), `idempotency_key` | starts an agent, or continues one that ended when `name` names it; `task` is its first message |
| `agent_list` | none | `cursor` | one page of your agents with name, state, mode, model, effort and inbox counts |
| `agent_status` | `agent` | none | one agent: its last turn, model and effort, pending obligations and kept results |
| `agent_send` | `agent`, `text` | `kind`, `reply_to`, `artifacts`, `payload`, `reply_required`, `requires_ack`, `idempotency_key` | sends a new task (`task_request`, the default) or answers a question with `reply_to`; the first line of `text` is the subject; `reply_required` marks a `task_request`, `handoff` or `review_request` and `requires_ack` a `status`, `decision`, `review_result`, `alert`, `answer` or `question`, as `dockingbird send --reply-required` and `--requires-ack` do. `reply_required` on another kind is refused before anything is sent: `VALIDATION_FAILED`, with the details `{"field": "reply_required", "reason": "INCONSISTENT"}` |
| `agent_inbox` | none | `agent`, `cursor` | one page of the deliveries your agents sent you, or with `agent` the deliveries to that agent |
| `agent_read` | `delivery_id` | `cursor`, `idempotency_key` | one page of a delivery's body and its artifact ids, and records your read |
| `agent_wait` | none | `agent`, `timeout_s` (1 to 45) | waits for the next delivery from `agent` or from any agent; a timeout cancels nothing |
| `agent_results` | `agent` | `cursor` | one page of the agent's artifacts saved under `results/<agent>/` in Dockingbird's folder, small text inline |
| `agent_stop` | `agent` | `idempotency_key` | stops one agent's container; its results are kept |
| `agent_set` | `agent` | `model`, `effort`, `idempotency_key` | changes a running agent's model or effort from its next turn |
| `agent_artifact_put` | `agent`, `name`, `content` | `media_type`, `idempotency_key` | stores a document as an artifact and returns the id that `agent_send` takes in `artifacts` |

## How the server behaves

- The harness can name a command, a task, an agent's name and its tool. It can never name a path, a config's content, a mount or an environment.
- Everything an agent writes comes back framed as data, with `from`, `kind`, `provenance` and `body`, and control characters escaped. Dockingbird never acts on it. Whether your harness does is the harness's own setting.
- A tool that changes something takes an `idempotency_key` of the form `YYYYMMDD/uuid4` and returns it. A retry with the same key and arguments gets the first answer back without running again. The same key with other arguments is refused with `IDEMPOTENCY_CONFLICT`.
- The server keeps the last 256 answers while it runs and writes nothing to disk. A retry after an unknown outcome, or after the server restarted, runs again, so a message can then arrive twice.
- `agent_inbox` and `agent_wait` share their rows with `dockingbird inbox` and `dockingbird wait`. A delivery one of them showed does not show again as new in the others.
- The server reads the checkout's `.dockingbird/` configs and the configs `config add` registered, once, when it starts. Its instructions name the commands they add, the default first. See [your-own-commands.md](your-own-commands.md).
- `agent_start` first makes Dockingbird ready as `dockingbird start` does, starting Docker and Dockingbird when they are off. It never waits for a toolchain. While the repo's versions install it answers `PROJECT_BUSY` with the cause `TOOLCHAIN_FETCHING`, and the harness tries again. See [toolchains.md](toolchains.md).
- Apart from that, the server never starts Docker or Dockingbird. While Dockingbird is off, its reads say it is unavailable, and `dockingbird sync`, `claude` or `codex` turns it back on.
- It starts agents without a terminal only. The tool names, their arguments and `idempotency_key` are under [the compatibility promise](../reference/integration/compatibility.md).

## Undo

Run the undo line from step 1 to remove the tools from one harness. A full clean does it for every harness that `mcp install` connected, using each harness's own remove command, and prints one line for each.

```text
Disconnected Claude Code from Dockingbird.
```

A harness you connected by hand keeps its settings. The clean prints the remove command for you to run.

## When it fails

- With no usable `claude` or `codex` on your `PATH`, `install` prints [`MCP_NOT_FOUND`](../troubleshooting.md#mcp_not_found), connects nothing, and shows the definition for another tool.
- [`MCP_CONNECT_FAILED`](../troubleshooting.md#mcp_connect_failed) means the tool's own `mcp add` failed or did not answer. Run the `mcp add` command the message gives, then `dockingbird mcp install --connected claude` to record it.
- [`MCP_CHECKED`](../troubleshooting.md#mcp_checked) is what `--check` prints for a harness that lost the tools, a program missing from `PATH`, a hand-made connection, or an empty record.
- Running `install` twice gives [`MCP_ALREADY_CONNECTED`](../troubleshooting.md#mcp_already_connected), and nothing changes.
- During a full clean, [`MCP_DISCONNECT_FAILED`](../troubleshooting.md#mcp_disconnect_failed) means a harness's remove command failed. Run the printed command yourself.
- [`TOOLCHAIN_FETCHING`](../troubleshooting.md#toolchain_fetching) is the cause behind `PROJECT_BUSY`, because the repo's versions are still installing. Call `agent_start` again.
