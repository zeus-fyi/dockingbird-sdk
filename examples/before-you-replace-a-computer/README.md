---
title: Before you replace a computer
summary: Save results, configs and hosts.toml, give the seat back, and start fresh on the new computer.
audience: daily
commands:
  - results --to
  - config list
  - homes
  - license deactivate
  - license activate
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Before you replace a computer

This cookbook saves what you want from a computer you are about to replace, gives its seat back, and starts fresh on the new one. Agents' copies live in a Docker volume and do not move, so you take their work first. A restore of a copied home waits for a run that proves it, and this cookbook does not do one. Each step ends with the line it prints when it worked.

## Before you start

- The old computer still runs Dockingbird. `dockingbird --version` prints a version.
- You have a folder outside the Dockingbird home to save into. This cookbook uses `../save`. `dockingbird results --to` refuses a folder inside the home.
- The new computer has Docker Desktop, uv and git, and you have the license key from your purchase email. See [install](../../docs/getting-started/install.md).

## 1. Take the agents' work and stop them

```bash
dockingbird sync
dockingbird stop
```

Run `sync` in each repo where an agent worked. A repo is clear when `sync` prints `myapp (main): up to date.` or an `Updated your main` line. `stop` then turns Dockingbird off, and it prints this line when it is done.

```text
Stopped claude-1. Dockingbird is off until you next use it.
```

Agent copies live in a Docker volume, so work they did not share is lost with the volume. `dockingbird status` lists each kept copy under "Needs your attention" with its pick-up command. Run that command, let the agent finish, and sync again.

## 2. Save the results

```bash
dockingbird results claude-1 --to ../save/claude-1
```

Run it once per agent. The step is done when each file prints its type and path, then this line.

```text
The copy in {where} is yours, outside dockingbird clean.
```

Message id `RESULTS_COPY_OWN`. `{where}` is the folder you gave. An agent with no files prints `claude-1's task thread has no artifacts yet.`

## 3. Save your configs

```bash
dockingbird config list
```

The step is done when each config you added has a row.

```text
  {name}  {scope}  {commands}  {workspace}  {mode}  {connections}  {digest}
```

Message id `CONFIG_LIST_ROW`. Keep the TOML files you added each config from, because `config add` copied them into the home. A repo's own `.dockingbird/` folder is in git.

## 4. Save hosts.toml and your own files

```bash
dockingbird homes
```

`homes` lists every Dockingbird home on this computer, so you know which folders to copy.

```text
default (default): Dockingbird stopped, version 0.15.3, this home
```

Message id `HOMES_ROW`. Copy these from each home's folder into `../save`: `hosts.toml`, `fleet.toml`, `versions.toml`, `config.toml`, the `instructions/` folder and any `vaults/`. The step is done when the files are in the save folder. `hosts.toml` names the other computers you reach, so the new computer reads them the same way. Sign-ins live in Docker volumes and are not in these files: you sign in again.

## 5. Give the seat back

```bash
dockingbird license deactivate
```

The step is done when the product prints this line.

```text
This computer no longer uses a seat of the license.
```

Message id `LICENSE_RELEASED`. A seat is one person with up to three computers, so you can skip this step and have both computers linked for a while. `dockingbird clean --all` gives the seat back first too. If you wipe the old computer without doing either, free it from another computer: [move your seat to a new laptop](../move-your-seat/README.md).

## 6. Start fresh on the new computer

Install Dockingbird. Then take a seat.

```bash
dockingbird license activate
```

The step is done when the product prints the activation line.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
```

Message id `LICENSE_ACTIVATED`. Create the home folder, copy the saved `hosts.toml`, `fleet.toml`, `versions.toml`, `config.toml` and `instructions/` into it before the first start, then add each saved config.

```bash
dockingbird config add ./agents/triage.toml
```

Then start in a repo as the first day does. The first start sets up the rest and signs in. See [one Mac, day one](../one-mac/README.md). Restoring a whole copied home, folder and volumes together, is not documented yet.

## When it fails

- A `--to` folder that is missing, or lies inside the Dockingbird home, gives [`RESULTS_TO_INVALID`](../../docs/troubleshooting.md#results_to_invalid).
- A file name in the save folder that holds something else gives [`RESULTS_TAKEN`](../../docs/troubleshooting.md#results_taken). Save into a new folder.
- `license deactivate` or `clean --all` with no answer from the license server leaves the seat held: [`LICENSE_SEAT_STILL_HELD`](../../docs/troubleshooting.md#license_seat_still_held). Free it from the new computer.
- A license whose seats are all linked refuses the new computer with [`LICENSE_SEATS_FULL`](../../docs/troubleshooting.md#license_seats_full). `dockingbird license activations --release ID` frees one.
- A new home folder that holds files other than your own and no marker gives [`HOME_NOT_EMPTY`](../../docs/troubleshooting.md#home_not_empty).
