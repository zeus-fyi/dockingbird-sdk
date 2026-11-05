---
title: First start stops
summary: Each place the first dockingbird claude can stop, in the order you meet it, with what the screen shows and the fix.
audience: first-day
commands:
  - claude
  - init
  - login claude
  - login claude --api-key
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# First start stops

This page follows `cd your-repo && dockingbird claude` from its first check to the running agent. Each step names the message id, what the screen shows and the fix. Ids link to the [catalogue](../troubleshooting.md).

## Before you start

- Dockingbird is installed and `dockingbird --version` prints a version.
- You are in a git checkout of your project. Check with `git status`.
- Docker answers. Check with `docker version`.
- The first run builds the image once. Expect about 5 minutes and about 1 GB of downloads.

The start is done when the screen prints these two lines, with your repo and branch.

```text
Starting claude-1 on myapp (main).
To leave it working, close this window.
```

## Step 1. A file in the home

Dockingbird keeps its files in `~/.local/share/dockingbird`, or in the folder `DOCKINGBIRD_HOME` names. It refuses a folder that holds files it did not make. This is [HOME_NOT_EMPTY](../troubleshooting.md#home_not_empty), exit 1, and nothing is set up.

```text
{folder} already has files Dockingbird didn't make, so it won't use it.
In it: {names:and}.
Move those files out of it (your own rules can stay in instructions/),
or set DOCKINGBIRD_HOME to an empty or new folder, then run this again.
```

Some names do not count: `instructions`, `vaults`, `versions.toml`, `config.toml`, `browser-solver.json`, `hosts.toml`, `fleet.toml`, Finder's `.DS_Store` file and an empty `logs` folder. Move the listed files out, or point `DOCKINGBIRD_HOME` at an absolute path that does not exist yet. Avoid a space or any of `%$"'\` in that path.

A variant says the folder is your home folder or one above it. Dockingbird never uses those, so choose another path.

## Step 2. A folder that is not a checkout

The command works on a repo. In any other folder it stops with [NOT_A_GIT_REPO](../troubleshooting.md#not_a_git_repo) and exit 1.

```text
Not a git repo: {path}.
cd into your project, then run this again.
```

Two relatives stop the same way. [SUBMODULE_NOT_YET](../troubleshooting.md#submodule_not_yet) appears inside a submodule, and [WORKTREE_NOT_YET](../troubleshooting.md#worktree_not_yet) appears in a git worktree. Both ask you to `cd` into the repository's main checkout and run the command again.

The command `dockingbird init` has its own pair. [INIT_NOT_A_CHECKOUT](../troubleshooting.md#init_not_a_checkout) says `{path} is not in a git repo, so there is nothing to set up.` and [INIT_INSIDE_HOME](../troubleshooting.md#init_inside_home) says the same for a folder inside the Dockingbird home. Run `dockingbird init` in your repo.

## Step 3. Files the agents do not take

Before it sets anything up, Dockingbird checks the branch. A symlink that leaves the repo, a submodule or a Git LFS file is refused within seconds. This is [LINK_TREE_POLICY](../troubleshooting.md#link_tree_policy), exit 1.

```text
{repo} ({branch}) can't be linked yet: it has {count} files the agents don't take:
{entries}
Fix them, commit, then run this again.
```

Each entry names its kind, and a symlink shows where it points. A relative symlink that stays inside the repo is fine. Remove or replace each listed file, commit, and run the command again.

## Step 4. Docker is not ready

Dockingbird starts Docker Desktop when it is off. [DOCKER_STARTING](../troubleshooting.md#docker_starting) and [DOCKER_WAKING](../troubleshooting.md#docker_waking) only inform and exit 0. They end with the seconds it took.

```text
Waking Docker ... ready ({elapsed})
```

When Docker does not come up, one of these stops the start, each with exit 1.

| Message id | What it means and the fix |
|---|---|
| [DOCKER_NOT_RUNNING](../troubleshooting.md#docker_not_running) | Start Docker Desktop, then run the command again. |
| [DOCKER_NOT_ANSWERING](../troubleshooting.md#docker_not_answering) | Docker took a request and never answered. Restart Docker Desktop. |
| [DOCKER_ANSWERING_SLOWLY](../troubleshooting.md#docker_answering_slowly) | Docker answers too late, as on a busy Mac. Check Docker Desktop. |
| [HOME_NOT_SHARED](../troubleshooting.md#home_not_shared) | Docker Desktop does not share the folder. Add it under Settings, Resources, File sharing. |
| [DOCKER_BUILDX_MISSING](../troubleshooting.md#docker_buildx_missing) | Update Docker Desktop, or install `docker-buildx-plugin` on Linux. |

## Step 5. The build

The build takes about 5 minutes and shows a progress line. Ctrl-C ends it with [SETUP_INTERRUPTED](../troubleshooting.md#setup_interrupted), exit 1.

```text
Set-up didn't finish. Nothing changed. Run this again.
```

Run the command again. A failed step stops with [IMAGE_BUILD_FAILED](../troubleshooting.md#image_build_failed) and exit 1. It names the step.

```bash
dockingbird --verbose claude
```

The `--verbose` flag shows Docker's own output for that step. [HOME_SETUP_TOOK_TOO_LONG](../troubleshooting.md#home_setup_took_too_long) means a tool's home took longer than Dockingbird waits, usually because the computer was busy. Run the command again when the load drops.

## Step 6. The copy of your branch

The start copies your branch for the agents. It is done when the line ends with the size and the time.

```text
Copying myapp (main) for the agents ({size}) ... done ({elapsed})
```

[REPO_LINKING](../troubleshooting.md#repo_linking) is that line and only informs. [REPO_DISK_FULL](../troubleshooting.md#repo_disk_full) exits 1 when Docker's virtual disk has too little room for the history. Free space in Docker Desktop, under Settings and Resources, or run `docker system prune`, then run the command again.

## Step 7. A sign-in that never finishes

The first start of a tool signs in once, inside the container. The start line says what will happen.

```text
Starting claude-1 on myapp (main). Claude will show a sign-in link:
open it on this Mac, sign in, then paste the code here. Only this once.
```

Open the link on the Mac, sign in, and paste the code back. That line is [SIGNIN_FIRST_TIME](../troubleshooting.md#signin_first_time). Codex shows a code and a link instead, and you enter the code on the page. If its device sign-in is off, turn it on in ChatGPT's security settings.

When you quit the sign-in, or never use the link, the agent ends with [SIGNIN_NEEDED](../troubleshooting.md#signin_needed) and exit 1. Its empty copy is removed.

```text
Claude isn't signed in yet. Run dockingbird claude again to sign in.
Or use an API key: dockingbird login claude --api-key
```

Run `dockingbird claude` again, or sign in on its own.

```bash
dockingbird login claude
```

The sign-in worked when the product prints [SIGNIN_DONE](../troubleshooting.md#signin_done).

```text
Claude is signed in.
```

[SIGNIN_FAILED](../troubleshooting.md#signin_failed) exits 1 when the screen did not finish, and nothing changed. [SIGNIN_NOT_SAVED](../troubleshooting.md#signin_not_saved) exits 1 when it finished but could not be kept. Run `dockingbird login claude` again for either. With no Claude or ChatGPT account, use an API key with `dockingbird login claude --api-key` or `dockingbird login codex --api-key`.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [HOME_NOT_EMPTY](../troubleshooting.md#home_not_empty) | Move the files out or set `DOCKINGBIRD_HOME`. |
| [NOT_A_GIT_REPO](../troubleshooting.md#not_a_git_repo) | `cd` into your project. |
| [INIT_NOT_A_CHECKOUT](../troubleshooting.md#init_not_a_checkout) | Run `dockingbird init` in your repo. |
| [LINK_TREE_POLICY](../troubleshooting.md#link_tree_policy) | Fix the listed files and commit. |
| [DOCKER_NOT_RUNNING](../troubleshooting.md#docker_not_running) | Start Docker. |
| [SETUP_INTERRUPTED](../troubleshooting.md#setup_interrupted) | Run the command again. |
| [IMAGE_BUILD_FAILED](../troubleshooting.md#image_build_failed) | Run again with `--verbose`. |
| [REPO_DISK_FULL](../troubleshooting.md#repo_disk_full) | Free Docker's disk. |
| [SIGNIN_NEEDED](../troubleshooting.md#signin_needed) | Sign in, or use an API key. |
| [SIGNIN_FAILED](../troubleshooting.md#signin_failed) | Run `dockingbird login claude` again. |

The page before this one is [a license refused](licence-refused.md). The first-run guide is [first run](../getting-started/first-run.md).
