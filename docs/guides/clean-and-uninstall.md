---
title: Clean and uninstall
summary: Free disk, delete stopped agents, remove everything Dockingbird made, give the seat back and uninstall the tool.
audience: daily
commands:
  - clean
  - clean NAME
  - clean --all
  - docker system df
  - docker builder prune
  - uv tool uninstall
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Clean and uninstall

This page shows how to get disk back from Dockingbird, from a light clean up to removing the tool. `clean` never touches your code, `~/.claude`, `~/.codex` or any object that does not carry this installation's labels. The order matters at the end: run `dockingbird clean --all` before `uv tool uninstall dockingbird`.

## Before you start

- Docker Desktop is running. `docker version` answers.
- Work you want is taken. Run `dockingbird sync` in each repo first, and `dockingbird results NAME --to DIR` for files you want to keep ([delegating tasks](delegating-tasks.md)). Copies made with `--to` are yours and `clean` never removes them.
- You can read the list of kept copies. `dockingbird status` shows each under "Needs your attention".

## What takes the disk

Each agent's copy holds the repo's history. Dockingbird keeps five Docker volumes: the state volume with every agent's copy and history, one volume each for the Claude and Codex sign-ins, the program store with each downloaded tool version, and the toolchain store. An agent also has a dependency cache, the volume `dockingbird-cache-<agent>`. Docker keeps the build cache of Dockingbird's image, shared with every other project's. A first run downloads about 1 GB. How much a week of use takes is not documented yet. Docker's own summary shows what is used now.

```bash
docker system df
```

`clean` prints the size it freed. That figure does not count Docker's build cache.

## 1. Free disk

```bash
dockingbird clean
```

`clean` removes old images of this installation, versions of toolchains that no running agent and no repo names, and the copies agents left behind. It removes a copy that is provably empty at once and asks about every other one. The default answer is no.

```text
claude-1 left 2 commits not shared yet. Remove its copy anyway? [y/N]
```

Message ids `CLEAN_ASK_UNSHARED`, `CLEAN_ASK_CHANGED` for files not committed, and `CLEAN_ASK_CRASHED` for a crash. A copy's results go with the copy and the question covers both (`CLEAN_RESULTS_QUESTION`). `--yes` removes without asking. Without a terminal, or with `--json`, `clean` without `--yes` keeps each copy it would ask about and exits 1. Ctrl-C at a question is a no for it and every question after it, and the command exits 130. Done when it names what it freed.

```text
Removed 2 copies (reviewer: 1 commit not shared; rev2: empty) and temporary files: 300 MB freed.
```

Message id `CLEAN_DONE`. A copy you said no to is named: `Kept claude-1's copy. Nothing else to clean.` (`CLEAN_KEPT`). Below a megabyte it says `under 1 MB freed`.

## 2. Delete a stopped agent by name

```bash
dockingbird clean codex-1
dockingbird clean codex-1 claude-2
```

This deletes the agent whole: its kept copy, its results folder and its history. `status` no longer lists it and its name is free for a new agent. It asks first about a copy or results that may hold work. It deletes an agent whole or not at all, so a no, or a copy it could not remove, keeps everything of that agent. Done when the line prints.

```text
Deleted codex-1: its copy (1 commit not shared), its results and its history; 300 MB freed.
```

Message id `CLEAN_NAME_DELETED`. A working agent is refused: `codex-1 is running. To delete it, stop it first: dockingbird stop codex-1` (`CLEAN_NAME_RUNNING`). An agent with nothing left says `Nothing to delete: codex-1 has no kept copy, results or history.` (`CLEAN_NAME_NOTHING`). Names and `--all` do not go together (`CLEAN_NAMES_WITH_ALL`).

## 3. Remove everything Dockingbird made

```bash
dockingbird clean --all
```

This removes this installation's containers, its five volumes, every agent's dependency cache, its images, every link in your checkouts' `.git/config`, the refs `refs/remotes/dockingbird/*` in each linked checkout and its files in `DOCKINGBIRD_HOME`. Harbor's install and jobs go with them. It gives this computer's seat back first. It lists what is lost, every item named, before it asks.

```text
claude-1 is working now: it will be stopped and its copy removed.
keep8 stopped with 1 file not committed: its copy will be removed.
myapp (main): 2 commits the agents shared that you haven't synced.
To keep them: git switch main, then dockingbird sync
This removes everything Dockingbird made: every agent and its copy, their
history, and the settings and logs in DOCKINGBIRD_HOME.
Your code is untouched. Type delete to go on:
```

Message ids `CLEAN_ALL_WORKING`, `CLEAN_ALL_KEPT`, `CLEAN_ALL_UNSYNCED` and `CLEAN_ALL_CONFIRM`. Take the commits the list names before you type `delete`. Any other answer prints `Nothing removed.` and exits 1 (`CLEAN_ALL_DECLINED`). `--yes` accepts the loss and afterwards names the working agents it stopped. Without a terminal and without `--yes` it refuses (`CLEAN_ALL_NEEDS_TERMINAL`). Done when the last lines print.

```text
Removed everything Dockingbird made ({freed}). Your code is untouched.
To remove the command too: uv tool uninstall dockingbird
```

Message id `CLEAN_ALL_DONE`. `{freed}` is the size. If it could not remove everything, it says so and the next run finishes the job (`CLEAN_ALL_INCOMPLETE`). If the license server did not answer, the seat is still held: `Free it from another computer: dockingbird license activations` (`LICENSE_SEAT_STILL_HELD`).

### What stays

| Kept | Why |
|---|---|
| Your code, `~/.claude` and `~/.codex` | Dockingbird never touches them |
| A `config.toml` holding anything you wrote, your `trust` line among it | It is yours |
| Your `instructions/` folder; `versions.toml` under `--yes` | They are yours. Without `--yes`, the list names `versions.toml` and it goes |
| Your `vaults/` folder when anything is in it | Your vault connections' stores (`CLEAN_ALL_VAULTS_KEPT`) |
| The empty `logs/` folder | Docker Desktop can refuse a shared folder deleted and made again, so the next start would fail |
| Other homes, clones, installs and caches in the default home | `CLEAN_KEPT_FOLDERS` names them |
| Docker's build cache | It carries no labels and is shared with other projects |

Delete the empty `logs/` folder after uninstalling, once Docker Desktop has restarted, if you like. A second `dockingbird clean --all` finds nothing to clean.

## 4. Uninstall the tool

```bash
uv tool uninstall dockingbird
command -v dockingbird
```

uv prints its own confirmation. Done when `command -v dockingbird` prints nothing. Uninstalling first would leave Dockingbird's containers, volumes and image behind. `dockingbird completion --install` added two lines to your shell's startup file. `clean --all` removes the completion script but not those lines, so delete them yourself.

## 5. Prune Docker's build cache

```bash
docker builder prune
```

This removes the unused build cache of every project on this Docker, not only Dockingbird's. Run it only if that is what you want. Docker asks before it removes anything and prints its own total. The cookbook [uninstall completely](../../examples/uninstall-completely/README.md) strings these steps together.

## When it fails

- `dockingbird clean` asks before it deletes a copy. [`CLEAN_ASK_UNSHARED`](../troubleshooting.md#clean_ask_unshared) is for commits not shared, [`CLEAN_ASK_CHANGED`](../troubleshooting.md#clean_ask_changed) for files not committed, and [`CLEAN_ASK_CRASHED`](../troubleshooting.md#clean_ask_crashed) for a crashed agent whose work could not be counted. Answer y only when you no longer want that work.
- In a script, `clean` without `--yes` keeps those copies and prints [`CLEAN_KEPT_NO_TERMINAL`](../troubleshooting.md#clean_kept_no_terminal).
- `dockingbird clean codex-1` for a running agent gives [`CLEAN_NAME_RUNNING`](../troubleshooting.md#clean_name_running). Stop the agent, then clean it.
- A name together with `--all` gives [`CLEAN_NAMES_WITH_ALL`](../troubleshooting.md#clean_names_with_all) and exit 2.
- Without a terminal, `clean --all` prints [`CLEAN_ALL_NEEDS_TERMINAL`](../troubleshooting.md#clean_all_needs_terminal). Add `--yes`.
- Any answer except `delete` ends with [`CLEAN_ALL_DECLINED`](../troubleshooting.md#clean_all_declined), and nothing is removed.
- A removal that could not finish prints [`CLEAN_ALL_INCOMPLETE`](../troubleshooting.md#clean_all_incomplete). Run `dockingbird clean --all` again.
- An image that another build uses stays, with [`CLEAN_ALL_IMAGE_LEFT`](../troubleshooting.md#clean_all_image_left).
- A license server that does not answer leaves the seat held: [`LICENSE_SEAT_STILL_HELD`](../troubleshooting.md#license_seat_still_held). Free it from another computer.
