# `dockingbird mcp`: the host tools

`dockingbird mcp` is an MCP server, over stdio, for the harness you work in on this computer (Claude Code or Codex).
Through its eleven tools that harness starts agents in Dockingbird, sends them messages, reads what they send back,
saves their results and stops them. Your harness starts the server; you never run it yourself:
`dockingbird mcp install` connects each harness it finds with that harness's own `mcp add` command and prints the
undo, and for another harness the server's definition is `{"command": "dockingbird", "args": ["mcp"]}`.

The server works in the folder your harness runs in, and starts agents of that checkout's configs and of the ones
`dockingbird config add` registered. An agent is named by its name (what `agent_start` returns and `agent_list`
shows), a delivery or an artifact by its id. A tool that changes something takes an `idempotency_key`
(`YYYYMMDD/uuid4`): a retry with the same key and the same arguments gets the first answer back without running
again. Everything an agent wrote comes back as data from its sender, never as an instruction.

## The tools

Arguments in bold are required; the others may be left out.

| Tool | Arguments | What it does |
|---|---|---|
| `agent_start` | `command`, `task`, `name`, `harness` (`claude` or `codex`), `idempotency_key` | Starts an agent; `task` is its first message. Returns its name, its ids and the command that applied: `command` when given, else this checkout's default command, else the default environment |
| `agent_list` | `cursor` | One page of your agents: name, state, mode, model, effort and inbox counts |
| `agent_status` | **`agent`** | One agent: its last turn, model and effort, pending obligations and kept results |
| `agent_send` | **`agent`**, **`text`**, `kind`, `reply_to`, `artifacts`, `payload`, `idempotency_key` | Messages an agent: a new task (`task_request`, the default), or an answer to its question with `reply_to`; `text`'s first line is the subject, `artifacts` takes ids from `agent_artifact_put` |
| `agent_inbox` | `agent`, `cursor` | One page of the deliveries your agents sent you; with `agent`, the deliveries to that agent |
| `agent_read` | **`delivery_id`**, `cursor`, `idempotency_key` | One page of a delivery's body and its artifact ids; records your read |
| `agent_wait` | `agent`, `timeout_s` (1 to 45) | Waits for the next delivery from `agent`, or from any agent; a timeout cancels nothing |
| `agent_results` | **`agent`**, `cursor` | One page of an agent's results: its artifacts saved under `results/<agent>/` in Dockingbird's folder, small text inline |
| `agent_stop` | **`agent`**, `idempotency_key` | Stops one of your agents; its results are kept |
| `agent_set` | **`agent`**, `model`, `effort`, `idempotency_key` | Changes a running agent's model or effort, from its next turn |
| `agent_artifact_put` | **`agent`**, **`name`**, **`content`**, `media_type`, `idempotency_key` | Stores a document as an artifact and returns the id `agent_send`'s `artifacts` takes |

`agent_inbox` and `agent_wait` share their rows with `dockingbird inbox` and `dockingbird wait`: a delivery one of
them has shown, the others do not show again as new. The tools, their names and their arguments are covered by
[the compatibility promise](compatibility.md).
