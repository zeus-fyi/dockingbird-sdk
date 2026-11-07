---
title: app.toml, the keys of a config
summary: Every key of a config file such as .dockingbird/app.toml, with its values, its default and what it fixes.
audience: daily
commands:
  - dockingbird config add
  - dockingbird config list
  - dockingbird config remove
  - dockingbird start --command
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# app.toml, the keys of a config

Each TOML file in the `.dockingbird` folder at the top of a checkout is a config, and the commands it adds exist in that checkout only.
A config you add with `config add` works in every repo instead.
Every key is optional, and a key you leave out takes the default in the tables below.

## Where a config lives

| Place | What it is |
|---|---|
| `.dockingbird/*.toml` at the top of a checkout | this repo's own configs; their commands exist in that checkout only, and each file is read again at every start |
| `dockingbird config add PATH` | an added config, copied into your Dockingbird home so its commands work in every repo; add it again after a change |
| `[commands.NAME]` tables | several commands in one file, in place of `command`, `default` and `skill` at the top |

## Keys of a command

| Key | Values | Default | What it does |
|---|---|---|---|
| `command` | text | the file's name, `app` | the command's name, as in `dockingbird review`; a name Dockingbird keeps (`status`, `start`, `claude`) refuses the whole config |
| `summary` | text | none | one line shown by `dockingbird -h`, `config list` and, for your own harness, `dockingbird mcp` |
| `default` | `true` or `false` | `false` | `dockingbird start` with no `--command` runs this command in this checkout; `claude` and `codex` never use it |
| `skill` | path to a Markdown file | none | on the bus, the file's text with `$TASK` replaced by the task is the first turn |
| `[skills]` | table of `path` and `into` | none | skills the agent's tool lists as its own (Claude Code's Skill tool and `/` menu, Codex's `$` mention); [its keys](#keys-of-skills) are below, and [skills.md](../../guides/skills.md) gives them step by step |
| `instructions` | path | none | role text given to the agent after Dockingbird's own rules |
| `harness` | `claude` or `codex` | `claude` | the tool; once set it is fixed, and `--harness` on a start cannot change it |
| `workspace` | `repo` or `scratch` | `repo` | a copy of this repo, or an empty folder of its own that needs no git repo |
| `mode` | `bus` or `terminal` | `bus` | in the background through messages, or at your terminal; once set it is fixed, and `--terminal` cannot change it |
| `context` | `kept` or `fresh` | `kept` | bus only: one conversation for every delivery, or a new conversation for each task delivery under the same rules |
| `repo_settings` | `true` or `false` | `false` | load the repo's own Claude Code or Codex settings, hooks and MCP servers, once the checkout is trusted |
| `tools` | `bus`, `default` or `full` | `bus` | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool. Commits made under `default` or `full` reach you through `dockingbird sync` |
| `egress` | `allowlist`, `models`, `none` or `full` | `full`, or what `dockingbird egress` set | what the agent may reach on the network |
| `allow` | list of hosts and presets | the list `dockingbird egress` set, else nothing beyond the tool's own hosts | with `allowlist`, the presets `registries` and `github`, or hosts such as `docs.python.org` and `*.corp.example` |
| `harness_args` | list of words | none | fixed arguments for the tool: Claude takes `--model`, `--fallback-model`, `--max-turns` and `--effort` (`low`, `medium`, `high`, `xhigh` or `max`); Codex takes `--model`, `-m` and `-c model_reasoning_effort=LEVEL`; anything else is refused |
| `mise_env` | text | none | mise's environments for the agent's toolchain, comma separated; `ci` makes mise read `mise.ci.toml` over `mise.toml` |
| `[env]` | table of text | none | variables the agent's tool sees; settings, never secrets, because the agent can read and send them |

## Keys of `[skills]`

| Key | Values | Default | What it does |
|---|---|---|---|
| `path` | a folder, or a list of folders | none | one skills folder, each of whose folders holding a `SKILL.md` is one skill (`".agents/skills"`), or a list of folders, each one skill or a skills folder (`[".agents/skills/review", "tools/skills"]`); a repo's own config names paths from the checkout's top, an added config's are relative to its file's folder, and `config add` copies them with it |
| `into` | `both`, `claude` or `agents` | `both` | where they go in the agent's home: `both` writes each skill to `~/.claude/skills`, where Claude Code finds personal skills, and to `~/.agents/skills`, where Codex finds a user's; `claude` or `agents` writes only that one |

## Keys of `[limits]`

| Key | Values | Default | What it does |
|---|---|---|---|
| `turn_minutes` | whole number, at least 1 | none, so no turn deadline | a turn that runs longer is interrupted and reported |
| `session_hours` | whole number from 1 to the installation's maximum, 168 | 12 | the agent stops itself after this many hours |
| `cpus` | text such as `"2"` | none | the agent container's CPU limit |
| `memory` | text such as `"4g"` | none | the agent container's memory limit |
| any key named here | as above | as above | fixed for the config's agents: `--session-hours`, `--cpus` and `--memory` with another value are refused, the same value is not |

## Keys of an added config only, refused in a repo's own config

| Key | Values | What it does |
|---|---|---|
| `connections` | list of connection names | connections you recorded with `dockingbird connect`, granted to each agent of the command for at most its `session_hours`; never a credential as a value |
| `browser` | `chrome` | a Google Chrome of Dockingbird's own in a container beside the agent, which `dockingbird watch` shows; the browser tools come with it whatever `tools` says |
| `browser_extensions` | list | with a browser: each entry a Chrome Web Store link, a 32-letter extension id, or an absolute folder (`/` or `~/` first) that holds a `manifest.json` |
| `[browser_policy]` | table | with a browser: Chrome policies by Google's names; policies that would cut Dockingbird's control of the browser are refused |
| `local_model` | model tag | a tag as `docker model ls` lists it, run on this Mac by Docker Desktop's Model Runner; used with `egress = "models"` |
| `version` | a tool version such as `"2.1.285"` | pins this config's tool version, at the top level or in one command |

## What a checkout you marked untrusted turns off

| Key | Effect while the checkout is untrusted |
|---|---|
| `harness_args` | not applied until `dockingbird trust` marks the checkout trusted |
| `[env]` | not applied until `dockingbird trust` marks the checkout trusted |
| `[skills]` | not applied until `dockingbird trust` marks the checkout trusted; `dockingbird -h` and `config list` say `.dockingbird/app.toml: skills applies after dockingbird trust`; an added config's `[skills]` apply everywhere |
| `repo_settings = true` | the repo's own settings, hooks and MCP servers do not load |
| an added config's `harness_args` and `[env]` | still apply everywhere, because you chose to add the config |

## Smallest useful files

```toml
# .dockingbird/app.toml
command = "review"
summary = "Review this branch and list what to fix"
skill = "skills/review.md"
```

```toml
# an added config: dockingbird config add agents/triage.toml
command = "triage"
harness = "codex"
connections = ["github-issues"]
```

## Related

| Page | What it holds |
|---|---|
| [your-own-commands.md](../../guides/your-own-commands.md) | the guide to adding a command, step by step |
| [templates/.dockingbird/app.toml](../../../templates/.dockingbird/app.toml) | a template with a comment on every key |
| [commands.md](../commands.md) | `config add`, `config list`, `config remove` and `start --command` |
| [limits.md](../limits.md) | the session and turn bounds in one table |
| [roles-and-connections.md](roles-and-connections.md) | the files a swarm's roles and a service connection use |
