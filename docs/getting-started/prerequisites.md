---
title: Prerequisites
summary: What a computer needs before Dockingbird installs, with one check for each item.
audience: first-day
commands:
  - docker version
  - docker buildx version
  - uv --version
  - git --version
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Prerequisites

This page lists what a computer needs before Dockingbird installs, and the command that checks each item.
When all four checks pass, go on to [install](install.md).

## Before you start

You need a terminal on the computer that will run Dockingbird, and a license key or a decision to use a trial.
The key arrives in your purchase email. [Activate](activate.md) covers the trial.

## Supported computers

Dockingbird runs on an Apple silicon Mac or on arm64 Linux.
Intel Macs, x86 Linux and Windows are not supported.
The first start checks the platform before it builds anything.

## 1. Docker

Dockingbird runs every agent in a container and builds its own image, so Docker must answer.

- On a Mac, install Docker Desktop. It shares your home folder by default, which Dockingbird needs, and it includes the buildx plugin.
- On Linux, install Docker Engine and Docker's `docker-buildx-plugin` package.

```bash
docker version
docker buildx version
```

Done when `docker version` answers without an error and `docker buildx version` prints the plugin's version.
Dockingbird starts Docker Desktop itself when it is stopped, so a stopped Docker Desktop is not a failure on a Mac.

## 2. uv

uv installs the `dockingbird` command from Zeusfyi's release index.
On a Mac, `brew install uv` installs it. Other platforms follow the [uv documentation](https://docs.astral.sh/uv/).

```bash
uv --version
```

Done when uv prints its version.

## 3. git

Dockingbird looks for git at `/usr/bin/git`.
It works on a git repository and copies your branch for the agents, so the repo needs a commit on a branch.

```bash
git --version
```

Done when git prints its version.

## 4. Disk space and network

The first start builds the image on your computer, with no image to pull from a registry.
It takes about 5 minutes and downloads about 1 GB, once.
The build also fills a folder of Ubuntu packages, `apt-pool`, inside the Dockingbird home, 441 MB once per pinned snapshot.
The home is `~/.local/share/dockingbird` unless `DOCKINGBIRD_HOME` names another folder.
Docker keeps the build cache of Dockingbird's image, shared with every other project's, and `docker builder prune` frees all of it.

The first start of each tool, Claude Code and Codex, then fetches that tool's latest release.
Both downloads need a working network.

## 5. A way to sign in the agents

Claude Code and Codex each need a sign-in or an API key.
Dockingbird reads the login Claude Code or Codex already uses on this computer, and keeps a copy.
Without one, the tool shows a sign-in link once at the first start, or you use an API key.
[First run](first-run.md) shows both routes.

## When it fails

- If there is no `docker` command, Dockingbird prints [`DOCKER_NOT_INSTALLED`](../troubleshooting.md#docker_not_installed). Install Docker Desktop on a Mac, or Docker on Linux.
- Docker that has not started in time ends in [`DOCKER_NOT_RUNNING`](../troubleshooting.md#docker_not_running). On Linux, start the service yourself and run the command again.
- The image build needs the buildx plugin, and its absence gives [`DOCKER_BUILDX_MISSING`](../troubleshooting.md#docker_buildx_missing). Update Docker Desktop, or add the `docker-buildx-plugin` package on Linux.
- A home folder with files Dockingbird did not make gives [`HOME_NOT_EMPTY`](../troubleshooting.md#home_not_empty). Point `DOCKINGBIRD_HOME` at an empty or new folder, then retry.
