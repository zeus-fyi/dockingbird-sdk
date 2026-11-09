---
title: Frequently asked questions
summary: Fourteen first-week questions, each answered in three lines with one link to the page that holds the detail.
audience: first-day
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../llms.txt).

# Frequently asked questions

Fourteen questions, three lines each. The questions cover the prerequisites and the key, what the agent sees, sync, two agents on one branch, a shared key, the slow first start, a closed lid, Claude Code against Codex, support, a new laptop, a trial, offline use and the GUI. The last line of each answer is a link.

## What do I need: Mac or Linux, Docker, uv, git, disk?
You need an Apple silicon Mac or arm64 Linux, Docker Desktop (Docker Engine with buildx on Linux), uv, and git at `/usr/bin/git`.
Intel Macs, x86 Linux and Windows are not supported. The first run downloads about 1 GB once and takes about 5 minutes.
See [prerequisites](getting-started/prerequisites.md).

## Where does the key go, and how do I know the install worked?
The key goes to uv through the environment variable `UV_INDEX_ZEUSFYI_PASSWORD`, then to `dockingbird license activate`, which asks for it hidden.
The install worked when `dockingbird --version` prints a version and activation prints `This computer is activated:`.
See [install](getting-started/install.md).

## What does the agent see of my computer and my repo?
Each agent runs in its own container, on its own copy of your last commit. It never sees your uncommitted edits.
A connection you name is the only way a folder, a database or a secret reaches it.
See [the security model](concepts/security-model.md).

## Where are the agent's changes, and what if we both committed?
The agents' work reaches you only as commits, when you run `dockingbird sync`.
`sync` never rewrites history and keeps your uncommitted edits. When both sides have new commits, it offers a merge.
See [the sync model](concepts/sync-model.md).

## Can two agents work on one branch at once?
Yes. Each agent has its own copy of your branch, so two agents never overwrite each other's files.
Start each with `dockingbird claude` or `dockingbird codex` in its own terminal, or with `dockingbird start` for a task on the bus.
See [the sync model](concepts/sync-model.md).

## Can my colleague use my key?
No. A seat is one person, who may link up to three computers, so a colleague needs a seat of their own.
A fourth computer on a one-seat license stops at activation with `LICENSE_SEATS_FULL`, and the key is never shown or printed.
See [what a seat is](guides/licensing.md#what-a-seat-is).

## Why is the first start slow, and how much disk does it take?
The first start builds Dockingbird's image on your computer, about 1 GB of downloads and about 5 minutes, once.
Each agent's copy holds your repo's history, and `dockingbird clean` frees the copies you no longer need.
See [first run](getting-started/first-run.md).

## What happens when I close the lid or lose the network?
Closing the terminal leaves the agent working, and a bare `dockingbird claude` in that repo reconnects to it.
When Docker Desktop was asleep, the screen shows `Waking Docker ...` and the command goes on once Docker answers.
See [the daily loop](guides/daily-loop.md).

## Claude Code or Codex, and how do I pick the model?
Run `dockingbird claude` for Claude Code or `dockingbird codex` for Codex. Each signs in once, inside its container.
`dockingbird set NAME --model MODEL --effort LEVEL` changes the model and effort of a running agent.
See [Claude Code and Codex](concepts/claude-code-and-codex.md).

## Something failed: where do I ask, and what do I send?
Every message says what to do next, and the [catalogue](troubleshooting.md) lists them all by id.
To ask for help, send `dockingbird --version`, the output of `dockingbird status --json` and the message id.
See [SUPPORT.md](../SUPPORT.md).

## How do I move to a new laptop?
Free the old computer's seat with `dockingbird license deactivate`, or with `dockingbird license activations --release ID` if it is lost.
Then install Dockingbird on the new laptop and run `dockingbird license activate`.
See [move your seat](../examples/move-your-seat/README.md).

## Can I try it without a key?
Yes. `dockingbird license trial` starts a trial on this computer with no key, once per computer.
A trial cannot install from the release index and cannot update, so an install needs a key.
See [start a trial](guides/licensing.md#start-a-trial).

## What happens when the computer is offline or the term ends?
`dockingbird license status` reads a file on the computer and needs no network, and without a check-in the license keeps working for its lease.
After a term ends the installed version keeps working, and new releases need a renewed license.
See [offline behavior](guides/licensing.md#offline-behavior-and-day-counts).

## Is there a GUI?
Yes. `dockingbird ui --install` installs it, and `dockingbird ui` opens one window with a tab for each agent and your inbox beside them.
It runs on Apple silicon Macs and arm64 Linux, and the install needs your git to read the GUI's private repository over SSH.
See [the GUI](guides/gui.md).
