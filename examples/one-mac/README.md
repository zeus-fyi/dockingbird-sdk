# One Mac, day one

Everything here runs on one Apple silicon Mac with Docker Desktop and uv, in a git repo of yours (`~/code/myapp`
below); nothing is written by hand. Each step ends with the line it gives when it is done, as
`docs/troubleshooting.md` lists that line under its message's id.

## 1. Install

Copy your license key from your purchase email, then:

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeusfyi.com/simple/
dockingbird license activate
dockingbird completion --install
```

`dockingbird license activate` asks for the key and gives this Mac its seat; from then on `dockingbird update` needs no
key, and `dockingbird license status` names your plan, its seats and the day it ends. Open a new terminal for the tab
completion. If `dockingbird` is not found, run `uv tool update-shell` and open a new terminal.

## 2. `dockingbird status`

```bash
cd ~/code/myapp
dockingbird status
```

Before the first run it sets nothing up and says so:

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

and when there is nothing new either way:

```text
myapp (main): up to date.
```

## 5. `dockingbird ui`

`dockingbird ui` opens the Dockingbird GUI in this terminal: a tab for each agent at a terminal, a sidebar row for each
agent and one for your inbox. It is installed once with `dockingbird ui --install`, which gets it from the
zeus-fyi/dockingbird-gui repository with your own git and SSH key, so it needs your access to that repository, and
ends with:

```text
Installed dockingbird-gui <version>:
  <its path>
Open it: dockingbird ui
```

With no GUI installed, `dockingbird ui` says `The Dockingbird GUI isn't installed.` and names the install command.

The operator guide (`docs/operator-guide.md`) has the rest: sign-ins and API keys, update and clean, and what lives
where. `dockingbird stop` turns it all off, and nothing is lost.
