---
title: "Troubleshooting index: the GUI, the MCP server and shell completion"
summary: "The 27 message ids about the GUI, the MCP server and shell completion, each with when it appears."
audience: integrator
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: the GUI, the MCP server and shell completion

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 27 ids about the GUI, the MCP server and shell completion.

Install the Dockingbird GUI with `dockingbird ui --install`; [the GUI guide](../guides/gui.md) has the steps.

| Id | When it appears |
|---|---|
| [`MCP_CONNECTED`](../troubleshooting.md#mcp_connected) | You ran `dockingbird mcp install` and it connected Dockingbird's tools to Claude Code or Codex with the tool's own `mcp add`, and recorded it; the line shows how to undo it. |
| [`MCP_ALREADY_CONNECTED`](../troubleshooting.md#mcp_already_connected) | You ran `dockingbird mcp install` (or its `--check`) and the tool already has Dockingbird's tools, or you gave `--connected` a name already recorded. |
| [`MCP_CONNECT_FAILED`](../troubleshooting.md#mcp_connect_failed) | You ran `dockingbird mcp install` and the tool's own `mcp add` failed or didn't answer, so nothing was recorded. |
| [`MCP_NOT_FOUND`](../troubleshooting.md#mcp_not_found) | You ran `dockingbird mcp install` and no `claude` or `codex` program it can run is on your `PATH`. |
| [`MCP_SHOW`](../troubleshooting.md#mcp_show) | You ran `dockingbird mcp install --show`: the server definition, `{"command": "dockingbird", "args": ["mcp"]}` (stdio), to add to a tool's MCP settings yourself; with a `DOCKINGBIRD_HOME` that isn't the default, it adds `"env": {"DOCKINGBIRD_HOME": ...}`. |
| [`MCP_CHECKED`](../troubleshooting.md#mcp_checked) | You ran `dockingbird mcp install --check`: a connection it recorded is gone from the tool, no `claude` or `codex` program on your `PATH` could be used now, or it was made by hand for another tool, which can't be checked; or nothing is recorded yet. |
| [`MCP_DISCONNECTED`](../troubleshooting.md#mcp_disconnected) | You ran `dockingbird clean --all` and it disconnected a harness `dockingbird mcp install` had connected, with the harness's own remove command. |
| [`MCP_CONNECTED_BY_HAND`](../troubleshooting.md#mcp_connected_by_hand) | You ran `dockingbird clean --all` with a harness you had connected yourself (`dockingbird mcp install --connected`). |
| [`MCP_DISCONNECT_FAILED`](../troubleshooting.md#mcp_disconnect_failed) | You ran `dockingbird clean --all` and a harness's remove command failed, or the program is gone. |
| [`UI_NOT_A_TERMINAL`](../troubleshooting.md#ui_not_a_terminal) | You ran `dockingbird ui` where it has no terminal to draw on: in a pipe, from a script, or with `--json`. |
| [`UI_STOP_WITH_INSTALL`](../troubleshooting.md#ui_stop_with_install) | You ran `dockingbird ui stop` with `--install`. |
| [`GUI_MISSING`](../troubleshooting.md#gui_missing) | You ran `dockingbird ui`, and the Dockingbird GUI it opens isn't on this computer: there's no `dockingbird-gui` in the `bin` folder in Dockingbird's folder, where `dockingbird ui --install` puts it, nor in a folder of your `PATH`. |
| [`GUI_SESSION_EMPTY`](../troubleshooting.md#gui_session_empty) | You ran `dockingbird ui` or `dockingbird ui stop` with the variable that names where the GUI runs set, but empty. |
| [`GUI_PREVIOUS_OPENED`](../troubleshooting.md#gui_previous_opened) | You ran `dockingbird ui`, and two GUIs run on this computer: the one you had before Dockingbird 0.4.4, and the one 0.4.4 started beside it under a name of its own. |
| [`GUI_NOT_EXECUTABLE`](../troubleshooting.md#gui_not_executable) | You ran `dockingbird ui`, and the file it found for the Dockingbird GUI can't be run: it isn't a program file you may run, or it didn't start, as a program built for another kind of computer doesn't. |
| [`GUI_WRONG_VERSION`](../troubleshooting.md#gui_wrong_version) | You ran `dockingbird ui`, and the Dockingbird GUI it found is another version than the one this Dockingbird works with, or didn't say its version when asked. |
| [`GUI_INSTALLING`](../troubleshooting.md#gui_installing) | You ran `dockingbird ui --install`, or `dockingbird update` found no dockingbird-gui installed, or one at another version than the one this Dockingbird expects. |
| [`GUI_INSTALLED`](../troubleshooting.md#gui_installed) | The dockingbird-gui Dockingbird got matched the checksum it expects, and it is now installed in the `bin` folder of your Dockingbird home, in place of the one before, with a link to it beside `dockingbird` on your `PATH`, so `dockingbird-gui` is a command too (run bare, it opens its own default view, not this home's: use `dockingbird ui`). |
| [`GUI_LINK_IN_THE_WAY`](../troubleshooting.md#gui_link_in_the_way) | You ran `dockingbird ui --install`, and where Dockingbird links dockingbird-gui beside `dockingbird` there is already a file that isn't its link, such as a build of your own. |
| [`GUI_LINK_REFUSED`](../troubleshooting.md#gui_link_refused) | You ran `dockingbird ui --install` or `dockingbird update`, and the folder `dockingbird` is in refused the link to dockingbird-gui. |
| [`GUI_CHECKSUM_MISMATCH`](../troubleshooting.md#gui_checksum_mismatch) | The dockingbird-gui file Dockingbird got doesn't have the SHA-256 checksum this Dockingbird expects for that version: the release was replaced by another build, or the file is damaged. |
| [`GUI_PLATFORM_UNSUPPORTED`](../troubleshooting.md#gui_platform_unsupported) | You ran `dockingbird ui --install` on a computer dockingbird-gui has no build for: it is built for Macs with Apple silicon and for Linux on arm64. |
| [`GUI_FETCH_FAILED`](../troubleshooting.md#gui_fetch_failed) | Getting dockingbird-gui failed, so nothing was installed and the one you had stays. |
| [`COMPLETION_INSTALLED`](../troubleshooting.md#completion_installed) | You ran `dockingbird completion --install`: Dockingbird wrote the completion script for your shell into its own folder and added the line that loads it to your shell's startup file (`~/.zshrc`, `~/.bashrc`, or fish's `~/.config/fish/conf.d/dockingbird.fish`). |
| [`COMPLETION_ALREADY`](../troubleshooting.md#completion_already) | You ran `dockingbird completion --install` again: your startup file already loads the script, so nothing was added to it, and the script was written again for this version. |
| [`COMPLETION_SHELL_UNKNOWN`](../troubleshooting.md#completion_shell_unknown) | You ran `dockingbird completion --install` without naming a shell, and the `SHELL` variable names a shell Dockingbird has no completion for, or isn't set. |
| [`COMPLETION_RC_REFUSED`](../troubleshooting.md#completion_rc_refused) | You ran `dockingbird completion --install`, and Dockingbird couldn't read or write your shell's startup file: the system refused it, it isn't a regular file, or it is very large; run the command with `--verbose` to see why. |
