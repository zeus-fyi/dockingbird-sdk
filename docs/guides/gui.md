---
title: The GUI
summary: Install the Dockingbird GUI with dockingbird ui --install, open and stop it, read its agent tabs, inbox and hosts sidebar, use its keys and mouse, and fix its message ids.
audience: daily
commands:
  - ui
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# The GUI

The Dockingbird GUI is a terminal program, `dockingbird-gui`, that shows every agent of this computer in one window. Each agent that runs at a terminal gets a tab, and your inbox and your hosts sit in a sidebar. The sections below cover the install, `ui` and `ui stop`, the window, the keys and mouse, the message ids and updates.

## What the GUI is

Run `dockingbird ui` and `dockingbird-gui` opens in the terminal you ran it in. It is built from [herdr](https://github.com/herdrdev/herdr) (Apache-2.0), so it keeps herdr's colours, layout and key prefix. It makes no network call of its own: no update check and no announcements.

Closing the window ends nothing. The GUI's server keeps running in the background with every tab and its agent, and the next `dockingbird ui` attaches to it again, with the tabs as you left them. This computer has one GUI server, whichever home and whichever folder you start it from.

Every action prints the `dockingbird` command it runs, in a popup or in the agent's tab, so you can learn the commands by using it. It has no key for changing an agent's settings or for sending a message: `dockingbird set` and `dockingbird send` do those, as [delegating tasks](delegating-tasks.md) shows.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version, and the first run is done.
- This computer is an Apple silicon Mac or arm64 Linux. The GUI has no build for another system, and the install says so with [`GUI_PLATFORM_UNSUPPORTED`](../troubleshooting.md#gui_platform_unsupported).
- A terminal window is open. `dockingbird ui` draws on the terminal and reads its keys and mouse, so it refuses a pipe or a script.

## 1. Install the GUI

```bash
dockingbird ui --install
```

```text
Getting dockingbird-gui 0.1.20 from GUI_REPO ...
Installed dockingbird-gui 0.1.20:
  ~/.local/share/dockingbird/bin/dockingbird-gui
  On your PATH: ~/.local/bin/dockingbird-gui
Open it: dockingbird ui
```

The first line is `GUI_INSTALLING`, with the repository's name in place of `GUI_REPO`. The last four lines are `GUI_INSTALLED`. The install needs no terminal, so it runs in a script too.

Dockingbird compares the file's SHA-256 with the checksum it pins for that version before it writes anything. A different checksum installs nothing ([`GUI_CHECKSUM_MISMATCH`](../troubleshooting.md#gui_checksum_mismatch)), and a build with no pinned checksum is not installed at all.

The file lands in `bin/dockingbird-gui` of your Dockingbird folder. A link to it goes beside `dockingbird` on your `PATH`, so `dockingbird-gui` also works as a command. Run bare, that command opens herdr's default session, not Dockingbird's: use `dockingbird ui`. A file of your own where the link would go is left as it is ([`GUI_LINK_IN_THE_WAY`](../troubleshooting.md#gui_link_in_the_way)), and a folder that refuses the link is named ([`GUI_LINK_REFUSED`](../troubleshooting.md#gui_link_refused)). The GUI is installed either way, and `dockingbird ui` runs it.

`dockingbird update` also installs it, on a Mac. See [how it is updated](#how-it-is-updated).

## 2. Open and stop the GUI

```bash
dockingbird ui
```

`ui` opens the GUI that `dockingbird ui --install` put in Dockingbird's folder, else a `dockingbird-gui` on your `PATH`. It runs only the version this Dockingbird pins, 0.1.20 for Dockingbird 0.15.28. Another version stops with `GUI_WRONG_VERSION` and the install command.

```bash
dockingbird ui stop
```

`ui stop` stops the GUI's one server, and every attached view ends. It needs no terminal, so it runs in a script too. A `dockingbird-gui` run bare from your `PATH` targets herdr's default session, which is why `ui stop` exists. Give `stop` and `--install` one at a time: together they print `UI_STOP_WITH_INSTALL` and exit 2.

Closing a tab leaves its agent working, as closing a terminal window does. `ctrl+b q` leaves the GUI with every agent still working.

## 3. What the window shows

- **A tab for each agent.** Each running agent at a terminal gets a tab named after it, whose pane is the agent's screen. Tabs sit in a workspace for the agent's repo and branch, such as `My App (main)`. The pane runs the same `dockingbird claude --as NAME` (or `codex`) that you would type, so it takes the agent over from any terminal that shows it. A tab you close stays closed until you open it from the agent's row.
- **An agent without a screen.** A click on the row of a running agent that has no screen, such as a Codex bus agent (`screen: none` in `dockingbird --json status`), opens its log as it grows, with a line to send it messages. The log opens when `fleet agents` lists the agent's container. Without that, the row is only selected.
- **The sidebar.** Under the workspaces, the `dockingbird` section lists the inbox and one row for each agent whose container runs, with the agents that ask first. A row shows the agent's name and state, its tool and computer (with `no screen` for an agent without one), and its repo and branch.
- **The inbox.** The first row, such as `Inbox (3)`, opens the inbox tab: the questions first, each with its numbered options, then the messages. The GUI never answers a question for you. A question opens the asking agent's screen, where you answer it.
- **The command bar.** One row under the panes shows the selected agent, its model, effort and context, one note, and the buttons for what you can do next, such as `results`, `stop`, `answer`, `sync` and `start`.
- **The Swarms tab.** It reads any home whose coordinator answers `inspect`, and its roster is the agents that run. See [updates](updates.md#5-read-homes-on-other-versions) for which homes that is.
- **Hosts.** The sidebar runs the host commands of [hosts](hosts.md). `add a host...` on the `DOCKINGBIRD` heading asks for the route, the destination and the name. For a host over ssh it also asks `PATH for docker there (or empty)` and `docker host URL there (or empty)`, the `--path` and `--docker-host` options, each optional. `rename...` on a host's heading asks for the new name, and the popup offers the old name first. `forget...` removes the host once you type `y`. The host `local` has neither. Renaming and forgetting change only the hosts file, as `fleet hosts rename` and `fleet hosts forget` do.

The GUI reads `dockingbird --json status` and `dockingbird --json inbox`, and `dockingbird --json questions` while a question waits. It reads when it starts and again 2 minutes after each read ends. It also reads at once for `r` and when a command's popup ends. A new agent's row can take up to 2 minutes to appear unless you press `r`.

The state of a tab (working, blocked or idle) is Dockingbird's own record of the agent. An agent that asks you something shows as blocked, whatever its screen shows.

Inside tmux, the sidebar and tab bar draw the Claude, Codex and Dockingbird tiles as images when tmux's `allow-passthrough` is on and the terminal speaks Kitty graphics. They draw as text (`✻`, `✿`) otherwise.

## 4. Keys and mouse

The mouse is first. Click a pane, a tab, a workspace or a row to focus it. Drag a border to resize a split, and drag over text to copy it. Right-click an agent's row for a menu of the same actions as the keys: `Stop` (`Delete...` once it ended), `Results`, `Pick up`, `Answer in its screen`, `Start an agent...`, `Sync`, `Inbox` and `Read everything again`. The sidebar's width, the share of the workspaces and the share of the `dockingbird` section move with a drag and are saved when you let go.

`ctrl+b` is the prefix: press it, let go, then press a key. `ctrl+b ?` lists every binding, and `ctrl+b ctrl+b` sends the pane a plain `ctrl+b`. `ctrl+b q` leaves the GUI with its agents working. Dockingbird's keys sit one layer under the prefix: `ctrl+b`, then `d`, then a letter.

| Key after `ctrl+b d` | What it does |
|---|---|
| `n` | Starts an agent: here, in a tab of its own, or in the background on the bus. It asks the tool, the name and, in the background, the task. |
| `x` | Stops a working agent with `dockingbird stop NAME --yes`, or deletes a stopped one after you type `y`. |
| `y` | Runs `dockingbird sync` in the folder you started the GUI in. |
| `a` | Opens the agent's screen, to answer it there. |
| `p` | Picks an ended agent up. |
| `R` | Runs `dockingbird results NAME`. |
| `i` | Opens your inbox in a tab. |
| `r` | Reads everything again. |

`Esc`, or any other key, leaves the layer and runs nothing. A key that needs an agent acts on the agent of the focused pane, else on the only agent, else it asks `which agent?`.

In the inbox tab, the arrows (or `j` and `k`) and the wheel select a row. Enter on a message runs `dockingbird read 3`, with its own number, and shows the output in the tab. `Esc` goes back. Enter on a question opens the asking agent's screen. `r` reads again, and `q` closes the tab.

When the GUI is not connected to its server, the keys and clicks you send a pane are dropped and never sent later. A yellow card at the top right says `Input not sent` once for that spell.

## How it is updated

Dockingbird pins one GUI version. Dockingbird 0.15.28 pins 0.1.20. `dockingbird update` keeps the GUI at the pin on a Mac and does nothing about it elsewhere.

- With no GUI at `bin/dockingbird-gui`, once Dockingbird is set up, `update` installs the pinned one after its own last line.
- With a GUI at another version, one that gives no version or one that cannot start, `update` replaces it with the pin.
- With a GUI at the pin whose `PATH` link is missing or points elsewhere, `update` makes the link again (`GUI_INSTALLED`, the one-line form).
- With agents running, `update` downloads the GUI into its staging folder while it stages the update, and puts it in place when the update takes over.
- On another computer, such as a cloud VM, `update` gets no GUI and leaves one already there as it is. `dockingbird ui --install` still installs it there when you ask.

A GUI that is already open keeps its version until its server stops. Run `dockingbird ui stop`, then `dockingbird ui`, to move to the new one.

When the GUI's step fails after Dockingbird itself updated, for example because git cannot read the GUI's repository, `update` prints the GUI's message and exits 1. The update is done. Fix the access and run `dockingbird ui --install`. `update` and `ui --install` leave the `dockingbird-gui` command on your `PATH` with the home that already has a GUI of this release, and replace a link to an older GUI. [Updates](updates.md) covers the rest of `update`.

## When it fails

Every message below links to its entry in the [catalogue](../troubleshooting.md). Add `--verbose` to a command to see a message's id beside it.

| Id | When it appears | Next step |
|---|---|---|
| [`GUI_MISSING`](../troubleshooting.md#gui_missing) | `dockingbird ui` finds no `dockingbird-gui` in Dockingbird's `bin` folder or on your `PATH`. Its other form says `DOCKINGBIRD_GUI` names a path with no file. Exit 1. | `dockingbird ui --install`, or `unset DOCKINGBIRD_GUI` |
| [`GUI_WRONG_VERSION`](../troubleshooting.md#gui_wrong_version) | The GUI found is another version than the pin, or gave no version. Exit 1. | `dockingbird ui --install` |
| [`GUI_NOT_EXECUTABLE`](../troubleshooting.md#gui_not_executable) | The file found cannot run, for example a build for another kind of computer. Exit 1. | `dockingbird ui --install` |
| [`UI_NOT_A_TERMINAL`](../troubleshooting.md#ui_not_a_terminal) | `ui` ran in a pipe, a script or with `--json`. Exit 1. | Run it in Terminal |
| [`UI_STOP_WITH_INSTALL`](../troubleshooting.md#ui_stop_with_install) | `ui stop` came with `--install`. Exit 2. | Run one at a time |
| [`GUI_PREVIOUS_OPENED`](../troubleshooting.md#gui_previous_opened) | Two GUIs run, the one from before Dockingbird 0.4.4 and a later one under its own name. It informs, exit 0. | Use the line's last command to end the second |
| [`GUI_SESSION_EMPTY`](../troubleshooting.md#gui_session_empty) | `DOCKINGBIRD_GUI_SESSION`, a variable for development, is set but empty. Exit 1. | `unset DOCKINGBIRD_GUI_SESSION` |
| [`GUI_INSTALLING`](../troubleshooting.md#gui_installing) | The install, or `update`, is getting the GUI. It informs, exit 0. | None |
| [`GUI_INSTALLED`](../troubleshooting.md#gui_installed) | The GUI is in place, or its link was made again. Exit 0. | `dockingbird ui` |
| [`GUI_FETCH_FAILED`](../troubleshooting.md#gui_fetch_failed) | the GUI download failed or timed out, or no such version exists. Exit 1. | Run `dockingbird ui --install` again |
| [`GUI_CHECKSUM_MISMATCH`](../troubleshooting.md#gui_checksum_mismatch) | The download is not the build this Dockingbird pins. Nothing was installed. Exit 1. | None |
| [`GUI_PLATFORM_UNSUPPORTED`](../troubleshooting.md#gui_platform_unsupported) | No build for this system, or no checksum yet for its build. Exit 1. | None |
| [`GUI_LINK_IN_THE_WAY`](../troubleshooting.md#gui_link_in_the_way) | A file of your own sits where the `PATH` link goes. It informs, exit 0. | Remove the file and install again |
| [`GUI_LINK_REFUSED`](../troubleshooting.md#gui_link_refused) | The folder of `dockingbird` refused the link. It informs, exit 0. | `ui` runs the GUI anyway |
| [`CLEAN_GUI_LINK_LEFT`](../troubleshooting.md#clean_gui_link_left) | `clean --all` kept a link that is not Dockingbird's own, or could not remove its own. It informs, exit 0. | Delete the link yourself |

`DOCKINGBIRD_GUI` and `DOCKINGBIRD_GUI_SESSION` are for development and tests: the first names another file to run, the second another session for the GUI. Leave both unset.
