---
title: Trust and repo settings
summary: Decide which checkouts load their own settings, hooks, MCP servers, rules and dependency installs inside an agent, and add rules of your own for every agent.
audience: daily
commands:
  - trust
  - trust --off
  - trust --forget
  - claude --no-toolchain
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Trust and repo settings

This page explains which checkouts are trusted and what that changes inside an agent. A trusted checkout lets the repo's own settings, hooks and MCP servers load, as Claude Code and Codex load them outside Dockingbird. An untrusted one gets none of them, because a cloned repo can use them to run code before an agent does anything. The marks live on your Mac, so no agent can change them.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- You know the repo's folder. Trust is per checkout, and `dockingbird trust` with no path acts on the repo you stand in.

## What trust changes

Every checkout is trusted unless you mark it untrusted, or make untrusted the default. The table shows what each state gives an agent.

| Item | Trusted checkout | Untrusted checkout |
|---|---|---|
| The repo's Claude Code and Codex settings, hooks and MCP servers | Load | Stay off |
| The repo's rules file, `.dockingbird/rules.md` by default | Read at each start | Not read |
| Claude's project `CLAUDE.md` and skills | Load with the settings | Stay off |
| Codex's `AGENTS.md` | Read | Read, through Codex's global instructions file; its `.codex/config.toml`, hooks and exec policies stay off |
| The repo's mise `[env]` and `[settings]` | Load | A config that needs them stops the start |
| Dependency installs from lock files | Run | Skipped: the agent gets its toolchain alone |
| Claude's question whether to trust `/work/<repo-name>` | Dockingbird answers it | Claude may ask once per repo; Dockingbird never answers |
| Codex's folder-access notice | Not shown | Shown at each screen; one Enter opens its copy restricted |

A plain version in `mise.toml`, a `.tool-versions` file and the version files need no trust. See [toolchains](toolchains.md).

## 1. Mark a checkout untrusted

```bash
dockingbird trust --off
```

`--off` and `--forget` are the same. Name another folder to mark it: `dockingbird trust --off ../cloned-app`. Done when the line prints.

```text
Not trusted: {path}. Its own settings, hooks and MCP servers stay off
in agents started here.
```

Message id `TRUST_FORGOTTEN`. `{path}` is the checkout's path on your Mac. Agents already running keep what they started with.

## 2. Trust a checkout again

```bash
dockingbird trust
```

This removes the mark `--off` left and marks the checkout trusted, whatever the default says. Done when the line prints.

```text
Trusted {path}. This checkout's own settings, hooks and MCP servers
load in agents started here.
```

Message id `TRUSTED`. A tool loads them only once Dockingbird has proven they cannot redirect its sign-in, and today that holds for both Claude Code and Codex. For a tool where it does not yet hold, the command adds `Claude Code keeps them off for now: Dockingbird has not yet proven they can't redirect its sign-in.` (`TRUST_PIN_UNPROVEN`).

## 3. Make untrusted the default

Open `config.toml` in `DOCKINGBIRD_HOME` and put one line at the top.

```toml
trust = "untrusted"
```

`trust = "trusted"`, or no line, is the default. A checkout you marked with `dockingbird trust` or `dockingbird trust --off` keeps its mark whatever the line says. The marks are files under `trust/` and `untrusted/` in `DOCKINGBIRD_HOME`. You edit the line by hand: there is no command or flag for it. Dockingbird changes nothing else in that file except its own `last_build_seconds` line, and a `config.toml` holding anything of yours stays through `dockingbird clean --all`. You can write the line before the first start, because a fresh home holding only your `config.toml` is Dockingbird's to use.

The command prints no done line. Check the line by starting a Codex agent in a repo you never marked: it shows the untrusted note before Codex opens.

```text
Codex may ask for folder access to /work/myapp: that is its copy of this repo.
```

Message id `TRUST_NOTE`. Any other `trust` value, or a `config.toml` that is not TOML, is refused by every command that reads trust (`TRUST_CONFIG_INVALID`). A start stops before anything runs.

## 4. What an untrusted checkout looks like at a start

Claude may ask once per repo whether to trust its copy. Codex shows its folder-access notice each time it opens its screen. Dockingbird answers neither, and whatever you answer turns nothing on. At a terminal, Dockingbird prints its note before each such Codex start and waits for Enter.

```text
Press Enter to open Codex.
```

Press Enter before you type. `n`, `q`, `2` or Esc at Codex's notice close Codex and end the agent. Ctrl-C there ends the start before Codex runs. A start whose input or output is a pipe prints Codex's note on the first start only and never waits. An agent started with `dockingbird start` in an untrusted repo runs without a screen, because its tool would ask about trust (`START_NO_SCREEN_TRUST`).

Dependency installs are skipped, and the agent says so.

```text
Dependencies: skipped (untrusted checkout; dockingbird trust allows them).
```

Message id `DEPS_SKIPPED_UNTRUSTED`. When the repo's mise config needs trust, the start stops. Two ways on: `dockingbird trust`, or a start with the image's versions.

```bash
dockingbird claude --no-toolchain
```

`--no-toolchain` is for that one start and is not remembered. Also on `codex` and `start`.

## 5. A trusted repo's Codex config that sets `developer_instructions`

Dockingbird's rules reach a Codex agent through the `developer_instructions` key. A trusted repo whose `.codex/config.toml` sets that key would replace them, so the start is refused on this Mac before anything runs, exit 2.

```text
.codex/config.toml sets developer_instructions, which replaces the agent's
Dockingbird rules in a trusted checkout, so nothing was started.
Remove the key, or run untrusted: dockingbird trust --off
```

Message id `START_PROJECT_RULES_REPLACED`. The same line shows when the file cannot be read (a link, over its size bound, not TOML). It also answers a bare `dockingbird codex` that would reconnect to a running agent: the agent keeps working, and you reach it again once the key is gone. Claude is not affected, and an untrusted repo's file is never read.

## 6. Rules of your own for every agent

Agents get Dockingbird's built-in rules for the coordination tools. To add your own for every agent in this home, write one file per tool in the home's `instructions/` folder.

```bash
mkdir -p "$DOCKINGBIRD_HOME/instructions"
$EDITOR "$DOCKINGBIRD_HOME/instructions/claude.md"
```

With no `DOCKINGBIRD_HOME` set, the home is `~/.local/share/dockingbird`. The files are `claude.md` and `codex.md`. Dockingbird copies a changed file into Docker the way it copies a key, read-only to agents, and never mounts it. A repo has its own rules too: the file that `[rules] file` names in `.dockingbird/project.toml` is read from the checkout at each start, `.dockingbird/rules.md` when the key is unset. It reaches Claude and Codex after Dockingbird's rules and before a config's own instructions.

A rules file the project names that is missing, a link, not UTF-8 text or holding a Dockingbird credential stops the start. So does a total of rules longer than 64 KB. In an untrusted repo the project's file is not read. These commands print no done line. Start an agent and ask it to quote its rules.

## When it fails

- [`TRUST_FORGOTTEN`](../troubleshooting.md#trust_forgotten): the checkout is marked untrusted.
- [`TRUST_NOTE`](../troubleshooting.md#trust_note): the first attached start in a checkout whose settings are off; the tool may ask about trust, and the answer turns nothing on.
- [`TRUST_CONFIG_INVALID`](../troubleshooting.md#trust_config_invalid): the `trust` line of `config.toml` is not `"trusted"` or `"untrusted"`, or the file is not TOML.
- [`TRUST_NOT_A_CHECKOUT`](../troubleshooting.md#trust_not_a_checkout): the path is not in a git repo; name one with `dockingbird trust PATH`.
- [`TRUST_PIN_UNPROVEN`](../troubleshooting.md#trust_pin_unproven): a tool keeps the repo's settings off for now, trusted or not.
- [`START_NO_SCREEN_TRUST`](../troubleshooting.md#start_no_screen_trust): an agent without a terminal runs without a screen, because its tool would ask about trust.
- [`DEPS_SKIPPED_UNTRUSTED`](../troubleshooting.md#deps_skipped_untrusted): dependencies were not installed in an untrusted checkout.
- [`START_PROJECT_RULES_REPLACED`](../troubleshooting.md#start_project_rules_replaced): a trusted repo's Codex config would replace Dockingbird's rules.
