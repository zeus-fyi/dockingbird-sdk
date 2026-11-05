---
title: Dockingbird
summary: Dockingbird runs Claude Code and Codex side by side on your git repo, each agent in its own container.
audience: first-day
commands:
  - uv tool install
  - dockingbird --version
  - dockingbird license activate
  - dockingbird license trial
  - dockingbird license status
  - dockingbird init
  - dockingbird claude
  - dockingbird codex
  - dockingbird status
  - dockingbird sync
  - dockingbird stop
  - dockingbird clean
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](llms.txt).

# Dockingbird

Dockingbird runs Claude Code and Codex side by side on your git repo, each in its own container.
Agents never overwrite each other and never touch your Mac.
Each agent works on its own copy of your branch, and its work comes back to you as commits through `dockingbird sync`.
Zeusfyi makes it, and it runs on an Apple silicon Mac or on arm64 Linux.

## Prerequisites

Dockingbird needs four tools and a license key. [Prerequisites](docs/getting-started/prerequisites.md) gives the check for each.

- An Apple silicon Mac or arm64 Linux. Intel Macs, x86 Linux and Windows are not supported.
- Docker Desktop, which includes the buildx plugin. Docker Engine on Linux needs Docker's `docker-buildx-plugin` package.
- [uv](https://docs.astral.sh/uv/). On a Mac, `brew install uv` installs it.
- git at `/usr/bin/git`.
- A license key from your purchase email, or no key and a trial.

## Install

On a Mac, copy the key from your purchase email, then run this line.
It hands the key to uv as the index's password, so the key never reaches your shell history or a command line.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
```

On Linux, read the key with `read -rs`, which does not echo it, and clear it afterwards.

```bash
read -rs UV_INDEX_ZEUSFYI_PASSWORD
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$UV_INDEX_ZEUSFYI_PASSWORD" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
unset UV_INDEX_ZEUSFYI_PASSWORD
```

Check the install with `dockingbird --version`, then run `dockingbird license activate` to give this computer its seat.
Never run a bare `uv tool install dockingbird`. That name on PyPI is not this product.
The index serves an active license only, so a trial cannot install from it.
[Install](docs/getting-started/install.md) has the details and the failures.

## Use it

| Command | What it does |
|---|---|
| `cd your-repo` then `dockingbird init` | Makes the repo ready: project file, rules, example swarm, skills |
| `dockingbird claude` | Starts Claude Code on the repo you are in, in its own container |
| `dockingbird codex` | Starts Codex on the same repo, in another terminal |
| `dockingbird status` | Shows who is working on what, and what needs you |
| `dockingbird sync` | Takes the agents' commits and sends them yours |
| `dockingbird login claude` | Signs in again; `dockingbird login claude --api-key` uses an API key instead |
| `dockingbird update` | Gets the latest Dockingbird, Claude Code and Codex |
| `dockingbird clean` | Frees disk space |
| `dockingbird stop` | Turns everything off; nothing is lost |
| `dockingbird egress` | Shows or sets what agents can reach |
| `dockingbird start "fix the flaky test"` | Hands an agent a task; it works without a terminal |
| `dockingbird wait claude-1` | Shows the agent's next message as it comes |
| `dockingbird inbox` | Lists what waits for you, numbered |
| `dockingbird read 1` | Shows one message and the files it names |
| `dockingbird send claude-1 "yes"` | Answers a question, or sends a new task |
| `dockingbird results claude-1` | Saves the files the agent attached |
| `dockingbird watch claude-1` | Shows the agent's browser, when its config asks for one |
| `dockingbird config add agents/triage.toml` | Adds a command of your own, usable in every repo |
| `dockingbird config list` | Lists your configs and this repo's |
| `dockingbird trust --off` | Keeps this repo's own settings, hooks and MCP servers off |
| `dockingbird license activate` | Asks for your key, hidden, and takes a seat for this computer |
| `dockingbird license trial` | Starts this computer's trial instead |
| `dockingbird license status` | Shows the plan, its seats and the day the term ends |
| `dockingbird clean --all` | Removes everything Dockingbird made |
| `uv tool uninstall dockingbird` | Removes the command; run it after `clean --all` |

Every command explains itself with `dockingbird -h`, and `-h` after a command shows that command's help.

## How the first start works

There is nothing to configure.
The first `dockingbird claude` checks your branch, builds the image, starts Dockingbird and copies the branch for the agents.
A branch holding files the agents do not take is refused in seconds, with each file named and nothing set up.
Such files are a symlink leaving the repo, a submodule or a Git LFS file.
The build takes about 5 minutes and downloads about 1 GB, once.
Each tool then uses the login already on your Mac, or shows a sign-in link once, inside Docker.
Every agent works in its own container. Nothing on your Mac is mounted into an agent unless you connect a folder by name.
To leave an agent working, close its window.
Dockingbird turns itself off after 30 minutes with no agent, and the next command turns it back on.

## Exit codes

Exit codes are 0 for done, 1 for a problem with its next step printed, and 2 for a usage error.
`dockingbird claude` and `dockingbird codex` exit with the tool's own status.
[Exit codes](docs/reference/integration/exit-codes.md) lists every code.

## Where to go next

- [Quickstart](docs/quickstart.md) is the one-page path from install to a first commit.
- [Prerequisites](docs/getting-started/prerequisites.md), [install](docs/getting-started/install.md), [activate](docs/getting-started/activate.md), [first run](docs/getting-started/first-run.md) and [choose a topology](docs/getting-started/choose-a-topology.md): one page for each step of the set-up.
- [Troubleshooting](docs/troubleshooting.md) lists every message Dockingbird prints, by its id, with the next step.
- [Operator guide](docs/operator-guide.md) is the long form, with sign-ins, update, clean, licensing and what lives where.
- [llms.txt](llms.txt) indexes every page, one line each, for a coding agent.
