---
title: The GUI
summary: What the Dockingbird GUI is, that its install is not yet available to customers, and what dockingbird ui prints today.
audience: daily
commands:
  - ui
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# The GUI

The Dockingbird GUI is a terminal program that shows every agent of this computer in one window, one tab per agent, with your inbox in a sidebar. Its install is not yet available to customers, so no customer can open it today. This page says what the GUI does, and what `dockingbird ui` prints when no GUI is installed, which is the case on your computer.

## What the GUI is

Run `dockingbird ui` and the program `dockingbird-gui` opens in your terminal. You drive it with the mouse. Each agent that runs at a terminal gets its own tab, named after the agent. A sidebar on the left lists your inbox and your agents, and a bar under the panes shows the selected agent with its buttons. Every action prints the `dockingbird` command it runs, so you can learn the commands by using it. Press `ctrl+b`, then `q`, to leave; the agents keep working. The GUI has no key for changing an agent's settings or for sending a message. `dockingbird set` and `dockingbird send` do those, as [delegating tasks](delegating-tasks.md) shows.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- You can do all of the daily work without the GUI. `dockingbird claude --as NAME` shows any agent's screen, and `dockingbird status` lists them all.

## What `ui` prints today

```bash
dockingbird ui
```

With no GUI installed, `ui` stops and exits 1.

```text
The Dockingbird GUI isn't installed.
Install it: dockingbird ui --install
```

Message id `GUI_MISSING`. The install step the second line names is not yet available to customers. Until it is, use `dockingbird status`, `dockingbird claude --as NAME` and the other commands in [the daily loop](daily-loop.md). `dockingbird ui` also needs a terminal: in a pipe or a script it prints `dockingbird ui needs a terminal: run it in Terminal, not in a pipe or a script.` and exits 1.

## When it fails

Only one message belongs to this page. [`GUI_MISSING`](../troubleshooting.md#gui_missing) appears whenever no GUI is installed on this computer, which today is every customer's computer.
