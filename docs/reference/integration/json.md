---
title: The --json envelope
summary: The keys of the one-line JSON envelope every message becomes under --json, and how a script reads it.
audience: integrator
commands:
  - dockingbird --json status
  - dockingbird --json fleet hosts
  - dockingbird --json fleet hosts set
  - dockingbird --json -h
  - dockingbird --json help
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# The `--json` envelope

Give `--json` before any command and Dockingbird prints each message as a single line of JSON, which this page calls an envelope.
Six keys make up an envelope.
A script that reads three of them, the id, the fields and the exit code, keeps working when a release rewords a message.

## The keys

| Key | What it holds |
|---|---|
| `ok` | `true` when `exit_code` is 0, else `false` |
| `exit_code` | the status the message ends the command with ([exit codes](exit-codes.md)) |
| `id` | the message's id, such as `FLEET_HOSTS_SET`; [the catalogue](../../troubleshooting.md) lists every id under a heading of its own, with when it comes and its next step |
| `lines` | the words a person sees, one string per line, never wrapped |
| `next_step` | the command the message suggests, when it suggests one; absent otherwise |
| `fields` | the values the lines were filled with, by name: counts are numbers, sizes are bytes, durations are seconds and lists are arrays |

## Other envelopes

| Envelope | What it holds |
|---|---|
| a help screen (`dockingbird --json -h`, `dockingbird --json help status`) | `id` is `HELP`, `lines` holds the screen, and `fields.command` names the command it explains, null for the top screen |
| an extra key | some envelopes carry a key of Dockingbird's own beyond these, such as `detail`; a script leaves a key it does not know alone |
| a row of `dockingbird --json status` | an envelope of its own, with the keys in the next table |

## Keys a status row adds

| Row | Keys it adds |
|---|---|
| an agent | `name`, `tool`, `repo`, `branch`, `state` (`working`, `idle`, `waiting`, `preparing`, `stopped` or `crashed`), `terminal`, `next_step`, `next_argv`, `screen`, `container`, `attach_argv` |
| a `preparing` agent | `step` (`environment` or `dependencies`), `since`, `last_output_at` |
| a repo heading | `behind`, `both_moved`, `head` |
| `today` | `count`, `names` |
| a kept copy under "Needs your attention" | `state` (`stopped` or `crashed`), `terminal`, `next_step`, `next_argv`, `mode`, `command` |
| the first line | `claude` and `codex`, each `api-key`, `signed-in` or `none` |

## What a script reads

| Read | Why |
|---|---|
| `id`, `fields` and `exit_code` | the compatibility promise covers them; see [compatibility.md](compatibility.md) |
| `lines` | never; its words change from one release to the next so that they read better |

## Example, the last line of `dockingbird --json fleet hosts set lab --ssh lab.example`

A script that wants the host it added reads `fields.host` of the envelope whose `id` is `FLEET_HOSTS_SET`.

```json
{"ok": true, "exit_code": 0, "id": "FLEET_HOSTS_SET", "lines": ["lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml."], "fields": {"host": "lab", "route": "ssh", "target": "lab.example", "path": "~/.local/share/dockingbird/hosts.toml"}}
```

## Streams

Results come on stdout and problems on stderr, each as its envelope, with one exception.
The fleet's reads print their exit-1 refusals on stdout, beside the rows they read.
Those reads are `fleet agents`, `fleet hosts`, and `fleet hosts set`, `rename` and `forget`.
A script reads both streams and tells the messages apart by `id`.

## Exit statuses

Each message has one exit status, and the envelope's `exit_code` is that status.
[Exit codes](exit-codes.md) holds the one table of statuses, with what a script does on each, and the catalogue gives each id's status under its heading.
