---
title: Updates
summary: Check for a new release, update with or without agents running, know which changes cannot be undone, pin a tool version, read homes on other versions, and move a fleet to a release.
audience: daily
commands:
  - update --check
  - update
  - fleet update
  - status
  - serve
  - clean
  - homes
  - inspect swarm
  - pin
  - init --check
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Updates

A Dockingbird home takes a new release in one of a few ways, and this page walks through each. `dockingbird update` fetches the latest Dockingbird, Claude Code and Codex. When agents are running, the home switches in place. Each agent picks up the new code at its next stopping point and keeps its conversation. Later sections cover the changes an update cannot undo, version pins, homes on other versions, a repo's own files and a whole fleet.

## Before you start

- Dockingbird is installed from Zeusfyi's release index and this computer is activated. `dockingbird license status` shows the license. Without an activation, `update` stops with `LICENSE_UPDATE_NEEDS_LICENSE` and says `Activate it: dockingbird license activate`.
- Dockingbird is set up. Before the first run, `update` upgrades only the command and prints `Dockingbird isn't set up yet; the first dockingbird claude will set it up.`
- No other `update` runs on this computer. A second one stops with `Another dockingbird update is under way here.` (`UPDATE_IN_PROGRESS`).

## 1. Check for a newer release

```bash
dockingbird update --check
```

`--check` changes nothing. Done when the line says a newer one is out.

```text
A newer Dockingbird is out. Get it: dockingbird update
```

Message id `UPDATE_AVAILABLE`. If the network is down, the check names the source it could not read and exits 1 (`UPDATE_CHECK_FAILED`).

## 2. Update with no agent running

```bash
dockingbird update
```

`update` upgrades the command, puts the release's code in the home's code store, and rebuilds the image only when the image's base changed: its operating system, its toolchains, its locked Python packages or its launcher. Then it fetches the latest of each tool you have used. A tool you never used is not fetched. The lines run in this order.

```text
Getting the latest Dockingbird ... done (0.15.2 -> 0.15.3)
Rebuilding Dockingbird (about 5 min) ... done (4 min)
Claude Code 2.1.296 is the latest.
Dockingbird 0.15.3 is installed and takes over now. Your repos, history and your saved Claude API key are kept.
```

Done when the last line prints, or `Up to date.` when nothing changed (`UPDATE_DONE`). Message ids `UPDATE_GETTING`, `UPDATE_REBUILDING`, `UPDATE_TOOLS` and `UPDATE_ROLLING`. The rebuild line appears only when the image's base changed. A tool that `update` had to fetch says `Got Claude Code 2.1.296.` instead. When the new release changes Dockingbird's records, `update` first says so, because there is no way back.

```text
This update changes Dockingbird's records.
Once it takes over, it can't go back to 0.15.2.
```

On a Mac, `update` then installs the Dockingbird GUI that this release pins, version 0.1.20 in 0.15.28, when none is installed or another version is, and links `dockingbird-gui` beside `dockingbird` on your `PATH`. It fetches the GUI with git over SSH, so git must reach the GUI's repository with your GitHub SSH key. When the fetch fails, Dockingbird itself is already updated: `update` says so, ends with the GUI message and exits 1. Run `dockingbird ui --install` again once git can reach the repository. On any other computer, such as a cloud VM, `update` downloads no GUI and leaves one already there as it is. A `dockingbird-gui` link that already opens a GUI of this release from another home stays where it is. See [the GUI](gui.md).

### Where the release is installed

`update` installs each release with uv into a folder of its own, `~/.local/share/dockingbird/programs/VERSION/`, and points your `dockingbird` command at it with one rename. A command you start during an update runs whole, on the old release or on the new one. A folder is never changed once installed, and an install that follows `main` names its folder by the first 12 characters of its commit. [The home folder layout](../reference/files/home-layout.md) lists `programs/VERSION/`, its `programs/VERSION.lock` and the `programs/current` link.

- `dockingbird clean` removes the program folders of earlier releases that no home names and no running Dockingbird uses. It keeps a folder still in use for a later `clean`, and `clean --all` never touches the folders.
- Your first `dockingbird update` after the install line moves your command into its program folder.
- A `uv tool upgrade dockingbird` that fetches anything new, or the install line run again, puts your command back on uv's own folder until your next `dockingbird update`.

### Changes an update cannot undo

Some updates change what Dockingbird keeps on disk, and the old release cannot run on the result. Two kinds exist: a records change and a PostgreSQL major upgrade.

A release that changes Dockingbird's records applies a kernel migration to each home it updates. A home updated to it cannot run an older coordinator image again. The migration runner refuses with `SCHEMA_AHEAD`. `update` says so first with `UPDATE_MIGRATES`, as shown above. Releases 0.15.0 to 0.15.24 applied migrations 0030 to 0034.

| Release | Migration | What it adds |
|---|---|---|
| 0.15.0 | `0030_swarm_roles` | the tables the bus and the broker read for a swarm role's send rule and its connection grants |
| 0.15.3 | `0031_live_claim_groups_by_claim_key` | a rebuilt view of live claims, so `status` answers in a few milliseconds on a home whose PostgreSQL has no statistics for its small tables |
| 0.15.6 | `0032_repository_release` | the nullable column `bus.repositories.released_at`, which `dockingbird repo release` fills |
| 0.15.11 | `0033_harness_fallback` | the nullable column `bus.sessions.fallback_of`, which every earlier session reads as null |
| 0.15.24 | `0034_delivery_guarantee` | the column `messages.reply_required` and the table `bus.expectations`, which every earlier message reads as no reply demanded |

Each home's PostgreSQL moved from 17 to 18.6 in 0.15.4, and a new home starts on 18 with data checksums on. The first start of each home after that update upgrades its database in place, which takes a few seconds. The old database stays beside the new one as `pg.old-17-TIME` in the `dockingbird-state` volume until a later release removes it. The upgrade cannot go back once done. When the new Dockingbird then does not come up, `status` says so with `UPDATE_SWITCH_FAILED` and this line: `Dockingbird 0.15.4 changed the records but didn't come up, and 0.15.3 can't run on them.` Fix the cause and run `dockingbird update` again.

### A stopped home stays stopped, and agents that stopped by themselves end

`update` in a home whose Dockingbird was stopped, by `dockingbird stop` or by its idle stop, stops the new coordinator again once the update is done. Updating several idle homes therefore does not start each one for 30 minutes.

`update` also ends the home's agents whose containers stopped by themselves, as `start` does: it saves their logs under `logs/agents/`, ends their sessions and removes their containers. It does this for an update to the release the home already runs and for a rolling update's first step. While an agent's hand-over to a new release is open, `update` leaves such agents to the next `update` or `start`.

## 3. Update with agents running

Run the same command.

```bash
dockingbird update
```

The new code takes over at once and Dockingbird's coordinator is replaced in the background. Your agents keep working through it. Done when the line names them.

```text
Dockingbird 0.15.3 is installed and takes over now.
claude-1 and codex-1 take it at their next stopping point.
```

Message id `UPDATE_ROLLING`. An agent switches in place: the same container, session and conversation, with its deliveries and open questions kept. Before its next prompt, at no cost of a turn, its tool is told `Dockingbird updated from 0.15.2 to 0.15.3 and resumed your conversation. Continue where you were.` A command you run meanwhile waits for the switch, minutes at most, and prints `Switching Dockingbird to 0.15.3 ...` (`UPDATE_SWITCHING`).

### When an agent switches

| Agent | Switches |
|---|---|
| On the bus | Between two turns, never inside a turn or a tool call |
| With a screen of its own on the bus | At its open gate, once your turn has ended |
| At a terminal | Never: it keeps its code until its terminal closes, and `update` never asks it |
| A Claude agent with background work | After the work ends, up to 30 minutes; past that the work is ended and the agent is told |
| An agent asked to stop after its turn | Ends as asked and never switches |

`dockingbird status` says how far the roll got and what holds each agent back.

```text
Dockingbird 0.15.3 is taking over: claude-1 and codex-1 take it at their next stopping point.
claude-1 takes 0.15.3 at the end of its turn (asked 2 min ago).
claude-2 on 0.15.2 keeps its own until its terminal closes.
```

Message ids `STATUS_UPDATE_ROLLING` and `STATUS_UPDATE_STRAGGLERS`. An idle agent that does not answer its ask in 10 minutes is left on its code. The roll waits for such agents, its stragglers, up to 24 hours, then ends, and `status` names the ones still running. A later `dockingbird update` asks the bus and screen stragglers again. To move an agent at a terminal, stop it and start it again.

```bash
dockingbird stop claude-2
dockingbird claude --as claude-2
```

Done when `update`, run again for the same version, prints this line.

```text
Dockingbird 0.15.3 is in place, and no agent is waiting to take it.
```

An update that changes Dockingbird's engine, the image's base, also rolls. Each bus or screen agent moves to a new container at its next stopping point, keeping its name, session and conversation, and `update` names those agents apart. An update to the same version that changes the image's base replaces Dockingbird on the new base the same way. Agents left on the old engine keep their code. Once they stop, run `dockingbird update` again: it finishes the update and moves Dockingbird's code store to the new version. The cookbook [update with agents running](../../examples/update-with-agents-running/README.md) runs this end to end.

### What a screen agent's switch waits for

A screen agent's switch waits behind text you typed and left unsent in its screen, as a held message does. After 300 seconds (`TUI_HOLD_REPORT_S`) the agent is told, and text left unsent is cleared once no key has come for as long again. `status` names the cause and how long it has lasted.

```text
notes-1's update waits until you finish typing in its screen.
```

`dockingbird --json status` gives the cause as `switch_hold`, one of `typing`, `working`, `drawing` or `starting`, and when it began as `switch_held_since`. A screen turn that the agent did not begin, that draws nothing and takes no key for 600 seconds (`TUI_TURN_STILL_MAX_S`), counts as ended, and a tool that has not reached its prompt after 300 seconds (`TUI_START_MAX_S`) is ended. After a switch, a screen agent's Claude Code resumes its conversation only when its transcript holds one. With none, it starts fresh.

### Your conversation across a switch

An agent's conversation is saved at the end of each turn, so a host crash or a killed container no longer loses the turns since its last save at a stop, an exit or a switch. A switch resumes the conversation even when Dockingbird could not confirm the transcript. Only a transcript that is not there starts a new one, and `status` then no longer says the agent picked up where it left off.

### `serve` through an update

`dockingbird serve NAME` and `serve --all` keep serving while an update replaces the coordinator. After a failed wait, `serve` looks at the home's update lock. While an update holds it, `serve` prints this line, looks again every 2 seconds and serves again once the update lets go.

```text
Dockingbird is updating, so notes-1 waits for it to finish.
```

Message id [`SERVE_UPDATE_WAITING`](../troubleshooting.md#serve_update_waiting). An update that runs longer than 600 seconds (`SERVE_UPDATE_WAIT_MAX_S`) stops `serve` with exit 1 ([`SERVE_UPDATE_TOO_LONG`](../troubleshooting.md#serve_update_too_long)). Run `serve` again then. `serve` never starts the coordinator itself, and `dockingbird stop` still ends it. From 0.15.25, a running `serve` moves to the release its home runs once the update has replaced Dockingbird, between two requests, with no browser session or job cut and no exit.

### Programs left on an older release

`status` names a `serve`, a login courier or a solve watcher that runs an older release than its home, with its process id ([`STATUS_HOST_PROCESS_BEHIND`](../troubleshooting.md#status_host_process_behind)). A browser or a proxy that runs an older release than its agent is named too ([`STATUS_SIDECAR_BEHIND`](../troubleshooting.md#status_sidecar_behind)). They take the new release when their agent starts again. To take it now, stop the agent and start it again.

```bash
dockingbird stop NAME
dockingbird claude --as NAME
```


### A roll that fails

`status` shows it under "Needs your attention" with the fix.

```text
Dockingbird didn't switch to 0.15.3, so 0.15.2 still runs.
See why and try again: dockingbird update
```

Message id `UPDATE_SWITCH_FAILED`. Run `dockingbird update` again. A roll stops if Dockingbird here or its code cannot be read for 30 minutes, and the next command here resumes it. When the switch at idle failed for a cause Dockingbird could name, `status` and the next command's refusal end the first line with it.

```text
Dockingbird didn't switch to 0.15.3, so 0.15.2 still runs: DOCKER_NOT_ANSWERING.
See why and try again: dockingbird update
```

### A home too old to roll

A home whose running Dockingbird predates rolling updates waits once, for its first update to a release that rolls. The agents keep their code until they end.

```text
Dockingbird here is too old to take 0.15.3 while agents run,
so claude-1 on 0.15.2 keeps its own until it ends.
```

Message id `UPDATE_NO_ROLL_FLOOR`. `status` says what waits (`STATUS_UPDATE_STAGED`). Once the last agent ends, Dockingbird switches by itself, with no command typed. After that, updates reach working agents at their stopping points.

### A home whose version cannot be read

A Dockingbird container made or changed outside Dockingbird may not say which version it is. Every command that uses Docker, except `stop` and `clean --all`, is then refused before anything starts.

```text
Dockingbird is running here, but its version can't be read,
so this dockingbird (0.15.3) can't use it.
Replace it: dockingbird stop, then dockingbird update
```

Message id [`VERSION_UNREADABLE`](../troubleshooting.md#version_unreadable). `dockingbird update` refuses the same way with [`UPDATE_VERSION_UNKNOWN`](../troubleshooting.md#update_version_unknown), and `status` names the same way out. Run `dockingbird stop`, then `dockingbird update`. Done when `dockingbird status` lists the home as usual.

## 4. Pin a tool version

```bash
dockingbird pin claude 2.1.285
dockingbird pin --clear claude
```

`pin` writes the version into `versions.toml` in the home. The next start downloads it if it is missing. Agents already running keep their version. Done when the line prints.

```text
Claude Code will run 2.1.285 from its next start; agents already running keep theirs.
Claude Code follows the latest release from its next start.
```

Message ids `PIN_DONE` and `PIN_FOLLOWS`. `dockingbird --version` shows a pin as `Claude Code 2.1.285 (pinned)`. A start or an update never changes a pinned version. `latest` and `--clear` follow the latest release. `stable` is Claude Code's slower channel and Codex has none. See [lock the tools your agents run](../../examples/lock-tool-versions/README.md).

## 5. Read homes on other versions

A home runs the Dockingbird it was last started or updated with, which may not be the one on your path.

```bash
dockingbird homes
dockingbird inspect swarm
```

`homes` prints one line per home on this computer.

```text
default (default): Dockingbird running, version 0.15.3, this home
```

Message id `HOMES_ROW`. `inspect swarm` reads one home's agents and who may message whom, without starting, updating or locking anything.

| Home | `homes` says | A command from here |
|---|---|---|
| Runs the image this Dockingbird would run | Its line, readable | Runs as usual |
| Runs 0.6.2 or later, an older image | `readable for inspection; a command from here would update it` | Updates its coordinator; its running agents follow |
| Runs a newer Dockingbird | `readable for inspection; commands from here are refused: it is newer, update this computer's Dockingbird` | Refused |
| Runs older than 0.6.2 | `not readable from here` | Updates it; with agents running, it switches once they end |
| Its coordinator is stopped | `not readable from here: a command from here would start it` | Starts it |

Three refusals name both sides. `INSPECT_NOT_SUPPORTED` is fixed by updating that home: `dockingbird --home lab update` for the home named `lab`. `STATE_NEWER` and `INSPECT_SCHEMA_NEWER` are fixed by updating this computer with `dockingbird update`.

## 6. Check a repo after an update

```bash
dockingbird init --check
```

`init --check` writes nothing and exits 1 when an installed file is not the running release's.

```text
myapp is not set up for Dockingbird 0.15.3: init would change it.
To change it: dockingbird init
```

Message id `INIT_OUT_OF_DATE`. Run `dockingbird init`: a file you edited is kept and named, and `--force` replaces it. Done when the check prints `myapp is set up for Dockingbird 0.15.3: nothing to change.` (`INIT_CURRENT`).

## 7. Move a fleet to a release

For a team whose computers form a pool, an admin moves every host with one command.

```bash
dockingbird fleet update --release 0.15.3
```

Only a member of `fleet_admin` may run it; any other login ends 77. Each host needs a live worker and a `repoint` line in its `[[host]]` table of `hosts.toml`: your own command that restarts that host's Dockingbird services and returns without waiting. See [the hosts file](../reference/files/hosts-file.md). The command installs the release host by host, updates each home, moves the services and waits for the worker to report the release. Done when the last line prints.

```text
Dockingbird 0.15.3 runs on lab and local.
```

Message id `FLEET_UPDATE_DONE`. A step that fails stops the command with the host and its words, exit 1, and leaves later hosts as they are. Fix it and run the same command again: hosts done are skipped. `--host NAME` moves one host. Before a release that needs a newer store, an admin runs `dockingbird org create`; a worker or admitter of the new release refuses to start against an older store (`FLEET_STORE_BEHIND`) until then.

## When it fails

- Never activated? On an index install, `update` stops at [`LICENSE_UPDATE_NEEDS_LICENSE`](../troubleshooting.md#license_update_needs_license) and tells you to run `dockingbird license activate`.
- A dead network turns `update --check` into [`UPDATE_CHECK_FAILED`](../troubleshooting.md#update_check_failed).
- If uv cannot fetch the release, [`UPDATE_UV_FAILED`](../troubleshooting.md#update_uv_failed) prints the exact command that failed. Run it yourself to read uv's reason.
- A second `update` started during the first prints [`UPDATE_IN_PROGRESS`](../troubleshooting.md#update_in_progress). Wait for the first to end.
- The new coordinator may not come up. [`UPDATE_SWITCH_FAILED`](../troubleshooting.md#update_switch_failed) then says the old version still runs, and `dockingbird update` shows why.
- On a Dockingbird from before rolling updates, [`UPDATE_NO_ROLL_FLOOR`](../troubleshooting.md#update_no_roll_floor) says the agents keep their code until they end.
- A coordinator whose version cannot be read ends every Docker command but `stop` and `clean --all` with [`VERSION_UNREADABLE`](../troubleshooting.md#version_unreadable), and `update` with [`UPDATE_VERSION_UNKNOWN`](../troubleshooting.md#update_version_unknown). Run `dockingbird stop`, then `dockingbird update`.
- A `serve` that waits for an update past 600 seconds ends with [`SERVE_UPDATE_TOO_LONG`](../troubleshooting.md#serve_update_too_long). Run it again.
- Before a release that changes the records takes over, you read [`UPDATE_MIGRATES`](../troubleshooting.md#update_migrates). The old version cannot run on those records. The table in "Changes an update cannot undo" lists them.
- Reading a home that predates inspection yields [`INSPECT_NOT_SUPPORTED`](../troubleshooting.md#inspect_not_supported); a home that a newer Dockingbird wrote yields [`STATE_NEWER`](../troubleshooting.md#state_newer). Update that home in the first case and this computer in the second.
- After an update, `init --check` exits 1 with [`INIT_OUT_OF_DATE`](../troubleshooting.md#init_out_of_date) if a repo's installed files are older. `dockingbird init` brings them up.
- `pin claude 2.1` is refused with [`PIN_INVALID_VERSION`](../troubleshooting.md#pin_invalid_version), and a well formed number the vendor never published gives [`TOOL_PIN_NOT_FOUND`](../troubleshooting.md#tool_pin_not_found).
- For a fleet, a host lacking its `repoint` line stops `fleet update` before it touches anything ([`FLEET_UPDATE_NO_REPOINT`](../troubleshooting.md#fleet_update_no_repoint)). A step that breaks on one host prints [`FLEET_UPDATE_HOST_FAILED`](../troubleshooting.md#fleet_update_host_failed), and the same command, run again, resumes.
- A worker that meets an org store without the newest change is refused with [`FLEET_STORE_BEHIND`](../troubleshooting.md#fleet_store_behind), until an admin runs `dockingbird org create`.
