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
  - dockingbird license activations
  - dockingbird license deactivate
  - dockingbird init
  - dockingbird claude
  - dockingbird codex
  - dockingbird status
  - dockingbird status --json
  - dockingbird sync
  - dockingbird stop
  - dockingbird clean
  - dockingbird login
  - dockingbird logout
  - dockingbird update
  - dockingbird pin
  - dockingbird egress
  - dockingbird trust
  - dockingbird env
  - dockingbird homes
  - dockingbird start
  - dockingbird send
  - dockingbird expect
  - dockingbird inbox
  - dockingbird read
  - dockingbird questions
  - dockingbird answer
  - dockingbird wait
  - dockingbird results
  - dockingbird search
  - dockingbird set
  - dockingbird config
  - dockingbird connect
  - dockingbird connections
  - dockingbird revoke
  - dockingbird disconnect
  - dockingbird serve
  - dockingbird watch
  - dockingbird mcp install
  - dockingbird ui
  - dockingbird ui --install
  - dockingbird ui stop
  - dockingbird cp
  - dockingbird node
  - dockingbird org
  - dockingbird fleet
  - dockingbird swarm
  - dockingbird work
  - dockingbird harbor
  - dockingbird inspect
  - dockingbird repo release
  - dockingbird completion
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](llms.txt).

# Dockingbird

Dockingbird runs Claude Code and Codex side by side on your git repo, each in its own container.
Agents never overwrite each other and never touch your Mac.
Each agent works on its own copy of your branch, and its work comes back to you as commits through `dockingbird sync`.
Zeusfyi makes it, and it runs on an Apple silicon Mac or on arm64 Linux.

## Prerequisites

Dockingbird needs four tools and a license key. [Prerequisites](docs/getting-started/prerequisites.md) gives the check for each.

- An Apple silicon Mac or arm64 Linux. Intel Macs, and Windows are not guaranteed to work.
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

These ten commands cover a first day.

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

Every command explains itself with `dockingbird -h`, and `-h` after a command shows that command's help.
`dockingbird COMMAND -h` prints the arguments of the release you installed.
The tables below group the rest by task. [Commands](docs/reference/commands.md) lists every argument, exit status and guide.

### Messages and tasks

An agent started with `start` works on the bus without a terminal. You hear from it through your inbox.
[Delegate tasks](docs/guides/delegating-tasks.md) walks through the loop.

| Command | What it does | Guide |
|---|---|---|
| `dockingbird start "fix the flaky test"` | Hands an agent a task; it works without a terminal | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird start --wait 30m "task"` | Waits up to 30 minutes for room when the host is busy | [Host load protection](docs/guides/host-load-protection.md) |
| `dockingbird send claude-1 "yes"` | Answers a question, or sends a new task | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird send --swarm NAME "pause and report"` | Sends one message to every live agent of a swarm; `--all` and `--role` pick other groups | [Reliable messages](docs/guides/reliable-messages.md) |
| `dockingbird send --reply-required claude-1 "task"` | Demands a reply to a task; `--requires-ack` keeps a message open until it is acknowledged | [Reliable messages](docs/guides/reliable-messages.md) |
| `dockingbird expect status --from test-1 --prefix tested --within 1800` | Alerts you when that message has not arrived in 1800 seconds; `expect --list` shows the open ones | [Reliable messages](docs/guides/reliable-messages.md) |
| `dockingbird inbox` | Lists what waits for you, numbered | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird read 1` | Shows one message and the files it names | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird questions` | Lists the questions your agents ask, one row each | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird answer 1 --option 2` | Answers a question by its option number, or in words | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird wait claude-1` | Shows the agent's next message as it comes | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird results claude-1` | Saves the files the agent attached | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird search "flaky test"` | Finds the newest messages that hold every word | [Delegate tasks](docs/guides/delegating-tasks.md) |

[Message persistence](docs/concepts/message-persistence.md) says where messages are stored and when old bodies expire.

### Agents and sessions

| Command | What it does | Guide |
|---|---|---|
| `dockingbird claude --as claude-1` | Reconnects to that agent from any branch; `--new` always starts a fresh one, and `--as NAME` names it | [Daily loop](docs/guides/daily-loop.md) |
| `dockingbird set claude-1 --effort high` | Changes a running agent's model, effort or compact point from its next turn | [Delegate tasks](docs/guides/delegating-tasks.md) |
| `dockingbird login claude` | Signs in again, or as someone else | [Sign in and API keys](docs/guides/sign-in-and-api-keys.md) |
| `dockingbird logout claude` | Signs the tool out and removes its saved API key | [Sign in and API keys](docs/guides/sign-in-and-api-keys.md) |
| `dockingbird env` | Shows the toolchain this repo's agents get; `env install`, `env lock` and `env use node 22` change it | [Toolchains](docs/guides/toolchains.md) |
| `dockingbird homes` | Lists every Dockingbird home on this computer | [Updates](docs/guides/updates.md) |
| `dockingbird --home NAME status` | Runs one command in the home named NAME | [Commands](docs/reference/commands.md) |
| `dockingbird mcp install` | Lets your own Claude Code or Codex start agents and talk to them | [MCP server](docs/guides/mcp-server.md) |

[Agent tools](docs/reference/agent-tools.md) lists every tool an agent gets from Dockingbird.

### Configs, trust and egress

| Command | What it does | Guide |
|---|---|---|
| `dockingbird config add agents/triage.toml` | Adds a command of your own, usable in every repo | [Your own commands](docs/guides/your-own-commands.md) |
| `dockingbird config list` | Lists your configs and this repo's | [Your own commands](docs/guides/your-own-commands.md) |
| `dockingbird config remove triage` | Removes an added config's copy | [Your own commands](docs/guides/your-own-commands.md) |
| `dockingbird trust --off` | Keeps this repo's own settings, hooks and MCP servers off | [Trust and repo settings](docs/guides/trust-and-repo-settings.md) |
| `dockingbird egress models` | Lets new agents reach only their tool's own hosts; `allowlist`, `none` and `full` are the other modes | [Egress and network](docs/guides/egress-and-network.md) |

### Connections and secrets

A connection lets agents use a resource while the secret stays with Dockingbird. [Connections](docs/guides/connections.md) covers each kind.

| Command | What it does | Guide |
|---|---|---|
| `dockingbird connect github --github your-org/myapp` | Lets agents fetch and push a GitHub repo without seeing your key | [Connections](docs/guides/connections.md) |
| `dockingbird connect NAME --folder PATH` | Gives agents a folder of this computer, read-only | [Connections](docs/guides/connections.md) |
| `dockingbird connect db --database postgres://reader@pg.local/app --password` | Gives agents a read-only database; they never see its password | [Connections](docs/guides/connections.md) |
| `dockingbird connect NAME --service FILE` | Registers a program of this computer for `serve` to run | [Connections](docs/guides/connections.md) |
| `dockingbird connect NAME --browser chrome` | Lends your Chrome, Firefox or Safari while `serve` runs | [Connections](docs/guides/connections.md) |
| `dockingbird connect logins --vault gopass --login alice https://site.example alice@site.example` | Connects a gopass vault whose logins and one-time codes are typed into an agent's browser | [Password vault](docs/guides/secrets-vault.md) |
| `dockingbird connect NAME --config FILE --to AGENT --until ISO` | Grants a connection to an agent until a time | [Connections](docs/guides/connections.md) |
| `dockingbird connections` | Lists connections and the agents that may use them | [Connections](docs/guides/connections.md) |
| `dockingbird revoke NAME` | Takes a connection away from one agent | [Connections](docs/guides/connections.md) |
| `dockingbird disconnect NAME` | Removes a connection and the key copy Dockingbird kept | [Connections](docs/guides/connections.md) |
| `dockingbird serve NAME` | Runs a service, browser or vault connection here, as you | [Connections](docs/guides/connections.md) |

### The agent's browser

| Command | What it does | Guide |
|---|---|---|
| `dockingbird watch claude-1` | Shows the agent's browser, when its config asks for one, and lets you take over its screen | [An agent's own browser](docs/guides/agent-browser.md) |

### The GUI

| Command | What it does | Guide |
|---|---|---|
| `dockingbird ui --install` | Gets the GUI this Dockingbird pins and installs it; needs no terminal | [The GUI](docs/guides/gui.md) |
| `dockingbird ui` | Opens the GUI over your inbox and every agent, one tab for each terminal agent | [The GUI](docs/guides/gui.md) |
| `dockingbird ui stop` | Stops the GUI's server; needs no terminal | [The GUI](docs/guides/gui.md) |

### Teams and the control plane

You run your own control plane. [Run your own control plane](docs/guides/control-plane-setup.md) covers the hub, the members and the upgrade, and [Install a team fleet](docs/guides/team-fleet.md) covers the rest of the team set-up.

| Command | What it does | Guide |
|---|---|---|
| `dockingbird cp init --hub-address 100.64.0.1` | Makes this home the control plane, its hub reached at that address on your tailnet | [Run your own control plane](docs/guides/control-plane-setup.md) |
| `dockingbird cp token --host laptop --platform macos` | Adds a computer and prints its join bundle once | [Run your own control plane](docs/guides/control-plane-setup.md) |
| `dockingbird cp status` | Lists the computers, their versions and when each was last heard from | [Run your own control plane](docs/guides/control-plane-setup.md) |
| `dockingbird cp remove laptop` | Takes a computer out at once | [Run your own control plane](docs/guides/control-plane-setup.md) |
| `dockingbird cp off` | Makes the home a plain home again | [Run your own control plane](docs/guides/control-plane-setup.md) |
| `dockingbird node join` | Joins this computer to the fleet with the bundle read from standard input | [Install a team fleet](docs/guides/team-fleet.md) |
| `dockingbird node leave` | Leaves the fleet; the agents keep running | [Install a team fleet](docs/guides/team-fleet.md) |
| `dockingbird org login HOST --as user --role ROLE` | Signs this computer in to your organisation's store | [Install a team fleet](docs/guides/team-fleet.md) |
| `dockingbird org status` | Shows the login and connects once | [Install a team fleet](docs/guides/team-fleet.md) |
| `dockingbird org projects` | Lists or changes the store's projects; `org roles`, `org people` and `org members` keep the rest, admin only | [Install a team fleet](docs/guides/team-fleet.md) |

### The fleet and swarms

A swarm is a named group of agents with roles. [Swarms](docs/guides/swarms.md) shows how to write one, and [Fleet scheduler](docs/guides/fleet-scheduler.md) shows how the pool places it.

| Command | What it does | Guide |
|---|---|---|
| `dockingbird swarm list` | Lists each swarm of this home and how many agents it has | [Swarms](docs/guides/swarms.md) |
| `dockingbird swarm add review-1 --swarm hi --role reviewer` | Puts an agent in a swarm with a role; `swarm remove`, `swarm role` and `swarm assign` change it | [Swarms](docs/guides/swarms.md) |
| `dockingbird fleet agents` | Lists every agent on every host; `fleet hosts` lists the hosts, `fleet probe` reads this computer | [Hosts](docs/guides/hosts.md) |
| `dockingbird fleet hosts add NAME --os mac --cores N --memory SIZE --line FIGURE=BOUND,CLEAR` | Adds a host to the pool; `fleet hosts policy`, `drain`, `undrain` and `remove` manage it | [Fleet scheduler](docs/guides/fleet-scheduler.md) |
| `dockingbird fleet describe NAME` | Prints a swarm definition's parameters and settable fields as JSON | [Swarm parameters](docs/guides/swarm-parameters.md) |
| `dockingbird fleet submit NAME --set KEY=VALUE` | Checks a swarm definition and queues it; `--set` fills a parameter | [Swarms](docs/guides/swarms.md) |
| `dockingbird fleet queue` | Shows each host and workload; `fleet why ID` says why one waits | [Fleet scheduler](docs/guides/fleet-scheduler.md) |
| `dockingbird fleet pause ID` | Pauses a workload; `resume`, `cancel`, `done`, `hold` and `set` change it | [Fleet scheduler](docs/guides/fleet-scheduler.md) |
| `dockingbird fleet add ID ROLE --count N` | Adds agents of a role to a running swarm; `fleet retire`, `replace`, `assign` and `prune` change the rest | [Swarms](docs/guides/swarms.md) |
| `dockingbird fleet host-history NAME` | Prints a pool host's samples, including load Dockingbird did not start | [Host load protection](docs/guides/host-load-protection.md) |
| `dockingbird fleet run --cores N --memory SIZE --bound TIME -- CMD` | Leases capacity and runs a command under the lease | [Fleet scheduler](docs/guides/fleet-scheduler.md) |
| `dockingbird fleet worker --host NAME` | Runs a host's worker service; `fleet admitter` runs the admitter | [Install a team fleet](docs/guides/team-fleet.md) |
| `dockingbird fleet update --release V` | Moves the pool's hosts to a release, one after another | [Updates](docs/guides/updates.md) |
| `dockingbird work status` | Prints the items in work by priority; `work show ID`, `work search TEXT` and `work needs-you` read more | [The work queue](docs/guides/work-queue.md) |
| `dockingbird work new ID --title TEXT --area AREA --priority P --owner OWNER` | Makes an item; `work log`, `work set`, `work eta`, `work agent` and `work request` record the rest | [The work queue](docs/guides/work-queue.md) |

### Benchmarks

| Command | What it does | Guide |
|---|---|---|
| `dockingbird harbor run -a claude-code` | Runs a Harbor benchmark task of this folder on this computer | [Harbor](docs/guides/harbor.md) |
| `dockingbird harbor baseline` | Runs the task with `-a oracle`, which must score 1, then `-a nop`, which must score 0 | [Harbor](docs/guides/harbor.md) |
| `dockingbird harbor jobs` | Lists the jobs that ran; `harbor results JOB` shows one | [Harbor](docs/guides/harbor.md) |
| `dockingbird harbor clean` | Removes the jobs; `--all` removes Harbor itself too | [Harbor](docs/guides/harbor.md) |

### Inspection and diagnostics

Every command here only reads.

| Command | What it does | Guide |
|---|---|---|
| `dockingbird status --json` | Prints the status as JSON, for scripts; `--host NAME` reads another host | [Commands](docs/reference/commands.md) |
| `dockingbird inspect swarm --json` | Reads this home's agents and whether each pair may message each other | [Commands](docs/reference/commands.md) |
| `dockingbird inspect config --agent NAME` | Shows the settings an agent runs with | [Commands](docs/reference/commands.md) |
| `dockingbird inspect capabilities` | Says what this Dockingbird can answer | [Commands](docs/reference/commands.md) |
| `dockingbird inspect instances` | Lists the Dockingbird homes on this computer, as `homes` does | [Commands](docs/reference/commands.md) |
| `dockingbird fleet scrape` | Reads this home's metrics | [Metrics](docs/guides/metrics.md) |

### Updates and cleanup

| Command | What it does | Guide |
|---|---|---|
| `dockingbird update --check` | Says whether a newer release is out | [Updates](docs/guides/updates.md) |
| `dockingbird update` | Gets the latest release; with agents running, the new one takes over when they end | [Updates](docs/guides/updates.md) |
| `dockingbird pin claude 2.1.285` | Runs one version of Claude Code or Codex; `pin --clear claude` follows the latest again | [Updates](docs/guides/updates.md) |
| `dockingbird clean` | Frees disk space | [Clean and uninstall](docs/guides/clean-and-uninstall.md) |
| `dockingbird clean claude-1` | Deletes that stopped agent, its kept copy, results and history | [Clean and uninstall](docs/guides/clean-and-uninstall.md) |
| `dockingbird clean --all` | Removes everything Dockingbird made | [Clean and uninstall](docs/guides/clean-and-uninstall.md) |
| `dockingbird repo release --repository R` | Drops one repository's registration; the next start in its folder copies the branch again | [Home layout](docs/reference/files/home-layout.md) |
| `uv tool uninstall dockingbird` | Removes the command; run it after `clean --all` | [Clean and uninstall](docs/guides/clean-and-uninstall.md) |
| `dockingbird completion zsh` | Prints the completion script for `zsh`, `bash` or `fish` | [Install](docs/getting-started/install.md) |

### Licensing

| Command | What it does | Guide |
|---|---|---|
| `dockingbird license activate` | Asks for your key, hidden, and takes a seat for this computer | [Licensing](docs/guides/licensing.md) |
| `dockingbird license trial` | Starts this computer's trial instead | [Licensing](docs/guides/licensing.md) |
| `dockingbird license status` | Shows the plan, its seats and the day the term ends | [Licensing](docs/guides/licensing.md) |
| `dockingbird license activations` | Lists the computers that hold a seat; `--release ID` frees one | [Licensing](docs/guides/licensing.md) |
| `dockingbird license deactivate` | Gives this computer's seat back | [Licensing](docs/guides/licensing.md) |

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
- [Commands](docs/reference/commands.md) lists every command with its arguments, exit statuses and guide.
- [The daily loop](docs/guides/daily-loop.md), [delegate tasks](docs/guides/delegating-tasks.md) and [reliable messages](docs/guides/reliable-messages.md) cover working with agents day to day.
- [The GUI](docs/guides/gui.md) installs with `dockingbird ui --install` and shows every agent in one window, with your inbox beside it.
- [An agent's own browser](docs/guides/agent-browser.md), [connections](docs/guides/connections.md) and [the password vault](docs/guides/secrets-vault.md) give agents a browser and logins without showing them a secret.
- [Swarms](docs/guides/swarms.md), [swarm parameters](docs/guides/swarm-parameters.md) and [host load protection](docs/guides/host-load-protection.md) cover groups of agents and the host they run on.
- [Run your own control plane](docs/guides/control-plane-setup.md) and [install a team fleet](docs/guides/team-fleet.md) cover a team's shared hosts.
- [Message persistence](docs/concepts/message-persistence.md) and [agent tools](docs/reference/agent-tools.md) explain where messages live and what tools an agent gets.
- [Changes from v0.7.0 to v0.15.28](docs/release-notes/changes-v0.7.0-to-v0.15.28.md) lists what each release changed.
- [Troubleshooting](docs/troubleshooting.md) lists every message Dockingbird prints, by its id, with the next step.
- [Operator guide](docs/operator-guide.md) is the long form, with sign-ins, update, clean, licensing and what lives where.
- [llms.txt](llms.txt) indexes every page, one line each, for a coding agent.
