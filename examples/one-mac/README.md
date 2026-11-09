---
title: One Mac, day one
summary: Install, activate, start a first agent, hand a second one a task and take their commits with sync, on one Apple silicon Mac.
audience: first-day
commands:
  - uv tool install
  - dockingbird license activate
  - dockingbird completion --install
  - dockingbird license status
  - dockingbird status
  - dockingbird claude
  - dockingbird start
  - dockingbird wait
  - dockingbird inbox
  - dockingbird read
  - dockingbird send
  - dockingbird results
  - dockingbird sync
  - dockingbird stop
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# One Mac, day one

This cookbook takes one Apple silicon Mac from the install to an agent's commit on your branch. It needs Docker
Desktop, uv and a git repo of yours, `~/code/myapp` below, and you edit no file by hand. Each step shows the line
Dockingbird prints when the step is done. The [troubleshooting](../../docs/troubleshooting.md) catalogue holds every
such line under its message id.

## Before you start

- An Apple silicon Mac. `uname -m` prints `arm64`.
- Docker Desktop, running. `docker info` prints the server section without an error.
- uv. `uv --version` prints a version.
- A git repo of yours with a branch checked out. `git -C ~/code/myapp status` prints the branch name.
- The license key from your purchase email, copied to the clipboard.

## 1. Install

Copy the license key from your purchase email. The first line passes it to uv in two environment variables, so the
key shows up neither on screen nor in your shell history.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
dockingbird license activate
dockingbird completion --install
```

`dockingbird license activate` asks for the key again at a hidden prompt and links this Mac to your seat. It is done
when it prints the plan, the seats and the term.

```text
This computer is activated: {plan}, {seats}, {term}.
You use Dockingbird under its terms: {link}
```

The activation saves a download token, so `dockingbird update` needs no key after this. `dockingbird license status`
prints the same plan, seats and term on its first line. Tab completion starts working in the next terminal you open.
A shell that answers `command not found: dockingbird` needs `uv tool update-shell` and a new terminal.

## 2. `dockingbird status`

```bash
cd ~/code/myapp
dockingbird status
```

Before the first run it sets nothing up and says so.

```text
Dockingbird isn't set up yet. Start here: dockingbird claude
```

The first run, `dockingbird claude`, sets it up: it checks your branch, builds the image (about 5 minutes, once),
starts Dockingbird, copies the branch for the agents and starts Claude Code in its own container, in this terminal. It
uses the Claude Code login already on this Mac, or shows a sign-in link once. To leave the agent working, close the
window.

## 3. `dockingbird start`

`dockingbird start` hands an agent a task with no terminal:

```bash
dockingbird start "Fix the flaky test"
```

It copies your branch for the agent, starts it, and ends with (agents are numbered across the installation, so the
first run's agent is `claude-1` and this one `claude-2`):

```text
claude-2 started on myapp (main).
Thread <id>. Watch: dockingbird wait claude-2
```

`dockingbird wait claude-2` gives its next message as it comes, `dockingbird inbox` lists what waits for you,
`dockingbird read 1` reads one, `dockingbird send claude-2 "yes"` answers it, and `dockingbird results claude-2` saves
the files it attached. `dockingbird status` now shows who is working on what.

## 4. `dockingbird sync`

The agents' work reaches your branch only as commits, through sync:

```bash
dockingbird sync
```

When an agent shared commits, it takes them and names each, with the command to review them:

```text
myapp (main): 1 new commit from the agents
...
Updated your main to <commit>. Review it: git log -p <commit>..<commit>
```

With nothing new either way, it prints this.

```text
myapp (main): up to date.
```

## 5. `dockingbird ui`

`dockingbird ui` opens the Dockingbird GUI in this terminal: one tab per agent, with your inbox beside them. The first
time, install it with `dockingbird ui --install`; `dockingbird update` keeps it current on a Mac. [The GUI](../../docs/guides/gui.md)
covers the install, its keys and what each message means.

The [operator guide](../../docs/operator-guide.md) has the rest: sign-ins and API keys, update and clean, and what
lives where. `dockingbird stop` turns it all off, and nothing is lost.

## When it fails

| Message id | What it means | Entry |
|---|---|---|
| `SIGNIN_NEEDED` | The tool is not signed in. Run `dockingbird login` for it, as the message says, or use an API key. | [catalogue](../../docs/troubleshooting.md#signin_needed) |
| `HOME_NOT_EMPTY` | The folder for Dockingbird's files holds files it did not make. Unset `DOCKINGBIRD_HOME` or point it at an empty or new folder. | [catalogue](../../docs/troubleshooting.md#home_not_empty) |
| `GUI_MISSING` | `dockingbird ui` found no GUI on this computer. Install it with `dockingbird ui --install`. | [catalogue](../../docs/troubleshooting.md#gui_missing) |
