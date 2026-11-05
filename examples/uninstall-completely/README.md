---
title: Uninstall completely
summary: Stop every agent, clean everything Dockingbird made, give the seat back, remove the tool and prune Docker's build cache.
audience: daily
commands:
  - stop
  - clean --all
  - uv tool uninstall
  - docker builder prune
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Uninstall completely

This cookbook removes Dockingbird from a computer: every agent, copy, volume and image it made, the license seat, the command itself and Docker's cached build layers. Your code is never touched. The order matters: remove what Dockingbird made first, then the command. Each step ends with the line it prints when it worked.

## Before you start

- Dockingbird still runs. `dockingbird --version` prints a version.
- Docker Desktop is running. `docker version` answers.
- Work you want is saved. Run `dockingbird sync` in each repo and `dockingbird results NAME --to DIR` for each agent. [Clean and uninstall](../../docs/guides/clean-and-uninstall.md) says what each removal takes with it.

## 1. Stop every agent

```bash
dockingbird stop
```

`stop` asks before stopping working agents. `--yes` skips the question. The step is done when the product prints this line.

```text
Stopped claude-1. Dockingbird is off until you next use it.
```

Message id `STOPPED`. With nothing running, the line is `Nothing is running. Dockingbird is off.` (`NOTHING_RUNNING`).

## 2. Clean everything

```bash
dockingbird clean --all
```

`clean --all` lists what is lost: each agent still working, each stopped agent with its copy kept, and commits the agents shared that you have not synced, each with the step that keeps them. Take those commits before you go on. It then says `Your code is untouched.` and asks you to type `delete`.

```text
claude-1 is working now: it will be stopped and its copy removed.
myapp (main): 2 commits the agents shared that you haven't synced.
To keep them: git switch main, then dockingbird sync
Your code is untouched. Type delete to go on:
```

Type `delete`. Any other answer prints `Nothing removed.` and exits 1. `--yes` accepts the loss, and without a terminal it is required. The step is done when the product prints these lines.

```text
Removed everything Dockingbird made ({freed}). Your code is untouched.
To remove the command too: uv tool uninstall dockingbird
```

Message id `CLEAN_ALL_DONE`. `{freed}` is the size. `clean --all` removes this installation's containers, its five volumes, every agent's dependency cache, its images, the links in your checkouts' `.git/config` and its files in the home. It keeps your code, your `config.toml` when it holds anything of yours, your `vaults/` folder when anything is in it, and one empty `logs/` folder so a later start works while Docker Desktop still shares it.

## 3. Check that the seat is back

`clean --all` gives this computer's seat back before it removes anything. When the license server does not answer, it says so.

```text
Dockingbird couldn't reach the license server, so this computer
still uses a seat.
Free it from another computer: dockingbird license activations
```

Message id `LICENSE_SEAT_STILL_HELD`. The step is done when `clean --all` did not print it. If you saw it, run `dockingbird license activations --release ID` from another computer, as [move your seat to a new laptop](../move-your-seat/README.md) shows.

## 4. Remove the command

```bash
uv tool uninstall dockingbird
```

uv prints its own confirmation. Check that the command is gone.

```bash
command -v dockingbird
```

The step is done when that command prints nothing. Uninstalling before step 2 would leave Dockingbird's containers, volumes and image behind.

## 5. Prune the build cache

```bash
docker builder prune
```

Docker keeps the build cache of Dockingbird's image. Every project's builds share it, and it carries no labels, so `clean --all` leaves it alone and its freed figure does not count it. `docker builder prune` removes the unused build cache of every project on this Docker, not only Dockingbird's. Run it only if that is what you want. The step is done when Docker prints its own total reclaimed.

## 6. Leftovers you may remove by hand

- The empty `logs/` folder in the home. Delete it once Docker Desktop has restarted.
- Two lines in your shell's startup file that `dockingbird completion --install` added. `clean --all` removes the completion script but not those lines.
- Your `vaults/` folder, if it kept the stores of your vault connections (`CLEAN_ALL_VAULTS_KEPT`).

## When it fails

- `dockingbird stop` with no terminal while agents work prints [`STOP_REFUSED_NO_TTY`](../../docs/troubleshooting.md#stop_refused_no_tty). Add `--yes`.
- `dockingbird clean --all` with no terminal prints [`CLEAN_ALL_NEEDS_TERMINAL`](../../docs/troubleshooting.md#clean_all_needs_terminal). Add `--yes`.
- Any answer except `delete` ends with [`CLEAN_ALL_DECLINED`](../../docs/troubleshooting.md#clean_all_declined), and nothing is removed.
- A removal that could not finish prints [`CLEAN_ALL_INCOMPLETE`](../../docs/troubleshooting.md#clean_all_incomplete). Run `dockingbird clean --all` again.
- An image that something else in Docker uses stays: [`CLEAN_ALL_IMAGE_LEFT`](../../docs/troubleshooting.md#clean_all_image_left). Remove that first, then run the command again.
- A license server that does not answer leaves the seat held: [`LICENSE_SEAT_STILL_HELD`](../../docs/troubleshooting.md#license_seat_still_held). Free it from another computer.
