---
title: Backup and restore
summary: What a Dockingbird home and its Docker volumes hold, what to save before you replace a computer, and how to start fresh on the new one.
audience: daily
commands:
  - results --to
  - config list
  - homes
  - license deactivate
  - license activate
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Backup and restore

This page says what Dockingbird keeps on your computer and in Docker, which of it you should save before replacing a computer, and how to start fresh on the new one. A restore of a copied home is not documented yet: a procedure is written here only after a run proves it.

## What a home holds

A home is the folder `DOCKINGBIRD_HOME`, `~/.local/share/dockingbird` by default. Other homes live in `homes/NAME` below it. The folder holds the files below, and Docker holds the rest in five volumes. See [the home layout](../reference/files/home-layout.md) for every file.

| Where | What it holds | Who writes it |
|---|---|---|
| `config.toml` | The image tag, the last build's duration and your `trust` line | You and Dockingbird |
| `hosts.toml`, `fleet.toml` | The other computers you reach, and the fleet database and your role | You, or `fleet hosts` |
| `versions.toml`, `egress.toml` | Tool pins, and what new agents may reach | `pin`, `egress` |
| `instructions/` | Your rules for every agent: `claude.md`, `codex.md` | You |
| `configs/` | A copy of each config you added with `config add`, and `configs/index.json` | `config add` |
| `results/<agent>/` | Files `dockingbird results` saved, one folder per agent | `results` |
| `connections/`, `vaults/` | The catalogs of your connections; the stores of vault connections | `connect` |
| `logs/` | Each agent's log, copied when it ends, and Dockingbird's own log | Dockingbird |
| `bin/`, `license.json` | The license client, the license file and the GUI link | `license`, `ui --install` |
| Docker volume `dockingbird-state` | Every agent's copy and history, and the protected copy of each linked branch | Dockingbird |
| Docker volumes `dockingbird-home-claude`, `dockingbird-home-codex` | The sign-ins and the saved API keys | `login` |
| Docker volume `dockingbird-tools` and the toolchain store | Downloaded versions of Claude Code and Codex, and the language versions agents get | Dockingbird |

The sign-ins live in the volumes, so a copy of the folder carries none. Sign in again on the new computer, as [sign-in and API keys](sign-in-and-api-keys.md) says. Dockingbird refuses to run in a folder that holds files but no marker, apart from the files it lists as yours: `logs/`, `instructions/`, `vaults/`, `versions.toml`, `config.toml`, `hosts.toml` and `fleet.toml`.

## Before you start

- The old computer still runs Dockingbird. `dockingbird --version` prints a version.
- You have a folder outside `DOCKINGBIRD_HOME` for what you save. `dockingbird results --to` refuses a folder inside it (`RESULTS_TO_INVALID`).

## 1. Take the agents' work

In each repo, take the commits the agents shared, and stop what runs.

```bash
dockingbird sync
dockingbird stop
```

Done when `sync` prints `myapp (main): up to date.` or the `Updated your main to ...` line, and `stop` prints `Stopped claude-1. Dockingbird is off until you next use it.` See [the daily loop](daily-loop.md). An agent's copy is in the state volume, not on your computer, so work not shared is lost with the volume. `dockingbird status` lists every kept copy under "Needs your attention".

## 2. Save the results

```bash
dockingbird results claude-1 --to ../save/claude-1
```

Run it once per agent. Done when each file prints its type and path, then this line.

```text
The copy in {where} is yours, outside dockingbird clean.
```

Message id `RESULTS_COPY_OWN`. `{where}` is the folder you gave. An agent with no files says `claude-1's task thread has no artifacts yet.` (`RESULTS_NONE`).

## 3. Save your configs

```bash
dockingbird config list
```

`config list` prints one row for each config: where it comes from, its commands, how it runs, the connections it may use and the start of its fingerprint.

```text
  {name}  {scope}  {commands}  {workspace}  {mode}  {connections}  {digest}
```

Message id `CONFIG_LIST_ROW`. Each field is one cell of the row. Keep the TOML files you added from. `config add` copied them into the home, and you can add them again on the new computer. A repo's own `.dockingbird/` folder is in the repo, so git carries it.

## 4. Save your own files

Copy `hosts.toml`, `fleet.toml`, `versions.toml`, `config.toml`, the `instructions/` folder and any `vaults/` you want to keep into the save folder. `dockingbird homes` lists every home on this computer, one line each, so you can do the same for each named home.

```bash
dockingbird homes
```

```text
default (default): Dockingbird stopped, version 0.11.1, this home
```

Message id `HOMES_ROW`. A connection's catalog in `connections/` names each key's path. The key's copy lives in a Docker volume, not in that folder, so the folder alone does not carry it.

## 5. Give the seat back

```bash
dockingbird license deactivate
```

Done when the line prints.

```text
This computer no longer uses a seat of the license.
```

Message id `LICENSE_RELEASED`. `dockingbird clean --all` gives the seat back first too. If you wiped the old computer without doing either, free it from another computer with `dockingbird license activations --release ID`. The cookbook [move your seat to a new laptop](../../examples/move-your-seat/README.md) shows both.

## 6. Start fresh on the new computer

Install Dockingbird as [install](../getting-started/install.md) says. Then take a seat.

```bash
dockingbird license activate
```

Done when the line prints.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
```

Message id `LICENSE_ACTIVATED`. Create the home folder if it does not exist, and copy your saved `hosts.toml`, `fleet.toml`, `versions.toml`, `config.toml` and `instructions/` into it before the first start. A folder holding only those files is Dockingbird's to use. Then add your configs again with `dockingbird config add`. The first start in a repo sets up the rest and signs in. The cookbook [before you replace a computer](../../examples/before-you-replace-a-computer/README.md) runs steps 1 to 6 in order.

Agents' copies and histories do not move. Restoring a whole copied home, folder and volumes together, is not documented yet.

## When it fails

- A `--to` folder inside the Dockingbird home, or one that does not exist, gives [`RESULTS_TO_INVALID`](../troubleshooting.md#results_to_invalid).
- A file name in the save folder that already holds something else gives [`RESULTS_TAKEN`](../troubleshooting.md#results_taken). Save into a new folder.
- A license server that does not answer at `license deactivate` or `clean --all` leaves the seat held, and [`LICENSE_SEAT_STILL_HELD`](../troubleshooting.md#license_seat_still_held) says so. Free it from the new computer.
- A license with every computer linked refuses the new one with [`LICENSE_SEATS_FULL`](../troubleshooting.md#license_seats_full). `dockingbird license activations --release ID` frees one.
- A home folder that holds other files and no marker gives [`HOME_NOT_EMPTY`](../troubleshooting.md#home_not_empty). Point `DOCKINGBIRD_HOME` at an empty folder.
