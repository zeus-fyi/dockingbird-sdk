# The `--json` envelope

Give `--json` before the command (`dockingbird --json status`, `dockingbird --json fleet hosts`) and every message
Dockingbird prints is one line of JSON, an envelope: a script reads one JSON object per line and never parses a
sentence.

## The keys

| Key | What it holds |
|---|---|
| `ok` | `true` when `exit_code` is 0, else `false` |
| `exit_code` | the status the message ends the command with (below) |
| `id` | the message's id, such as `FLEET_HOSTS_SET`; `docs/troubleshooting.md` lists every id under a heading of its own, with when it comes and its next step |
| `lines` | the words a person sees, one string per line, never wrapped |
| `next_step` | the command the message suggests, when it suggests one; absent otherwise |
| `fields` | the values the lines were filled with, by name: counts are numbers, sizes are bytes, durations are seconds and lists are arrays |

A help screen is an envelope too (`dockingbird --json -h`, `dockingbird --json help status`): its `id` is `HELP`, its
`lines` the screen, and `fields.command` the command it explains, null for the top screen. Some envelopes carry a key
of Dockingbird's own beyond these, such as `detail`; a script leaves a key it does not know alone.

## What a script reads

A script reads `id` and `fields`, never `lines`. The words of `lines` change from one release to the next so that they
read better; an `id`, its `fields` and its `exit_code` are what [the compatibility promise](compatibility.md) covers.
After `dockingbird --json fleet hosts set lab --ssh lab.example`, for example, the last line is:

```json
{"ok": true, "exit_code": 0, "id": "FLEET_HOSTS_SET", "lines": ["lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml."], "fields": {"host": "lab", "route": "ssh", "target": "lab.example", "path": "~/.local/share/dockingbird/hosts.toml"}}
```

and a script that wants the host it added reads `fields.host` of the envelope whose `id` is `FLEET_HOSTS_SET`.

Results come on stdout and problems on stderr, each as its envelope, with one exception: the fleet's reads
(`fleet agents`, `fleet hosts`, and `fleet hosts set`, `rename` and `forget`) print their exit-1 refusals on stdout,
beside the rows they read. A script reads both streams, by `id`. Each row of `dockingbird --json status` is an
envelope of its own.

## Exit statuses

| Status | Meaning |
|---|---|
| 0 | done |
| 1 | a problem Dockingbird printed, with its next step |
| 2 | a usage error: a word, an option or a value the command does not take |
| the tool's own | `dockingbird claude` and `dockingbird codex` exit with Claude Code's or Codex's status once it has started, 0 when the agent keeps working without a terminal, and 1 when Dockingbird stopped before starting it |
| 69, 78 | the fleet scheduler's commands: its database did not answer (69), or answered with a refusal, such as a wrong role or password in `fleet.toml` (78) |

Each message has one exit status, which `docs/troubleshooting.md` gives under its heading, and the envelope's
`exit_code` is that status.
