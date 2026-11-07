---
title: "Troubleshooting index: updates"
summary: "The 49 message ids about checking for and installing updates, pins and the switch to a new version, each with when it appears."
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: updates

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 49 ids about checking for and installing updates, pins and the switch to a new version.

| Id | When it appears |
|---|---|
| [`VERSION`](../troubleshooting.md#version) | You ran `dockingbird --version` (or `-v`): Dockingbird's version, the commit it was installed from (or that it came from a local checkout, when you installed it from a folder), and the versions of Claude Code and Codex it runs. |
| [`VERSION_MISMATCH`](../troubleshooting.md#version_mismatch) | The `dockingbird` command you ran is older than the Dockingbird that is running, so it won't talk to it. |
| [`VERSION_UNREADABLE`](../troubleshooting.md#version_unreadable) | You ran a `dockingbird` command, and the Dockingbird running in this home doesn't say which version it is, or says something that isn't a version (a container made or changed outside Dockingbird), so the command can't use it. |
| [`STATE_NEWER`](../troubleshooting.md#state_newer) | A newer Dockingbird last wrote the files Dockingbird keeps for you (`state.json` in its folder), and the `dockingbird` command you ran is older, so it reads them but won't change them. |
| [`STATE_FILE_REFUSED`](../troubleshooting.md#state_file_refused) | Dockingbird keeps its records of your agents, sign-ins and kept copies in `state.json` in its folder, and reads that file only when it is a plain file within its size limit. |
| [`STATE_FILE_NOT_UPDATED`](../troubleshooting.md#state_file_not_updated) | A command did what you asked, but the record of it couldn't go into `state.json`: the file is over its size limit, a link, a folder or a file Dockingbird can't open, or this record would have taken it past the limit. |
| [`UPDATE_GETTING`](../troubleshooting.md#update_getting) | You ran `dockingbird update`: the first step gets the latest Dockingbird, and its line ends with the versions before and after. |
| [`UPDATE_REBUILDING`](../troubleshooting.md#update_rebuilding) | `dockingbird update` rebuilds Dockingbird, with an estimate from the last build when a build runs, and none when the new version is already built; then it gets the tools' latest releases, one line each. |
| [`UPDATE_DONE`](../troubleshooting.md#update_done) | You ran `dockingbird update`, and there was nothing to change: no newer Dockingbird to install and nothing to rebuild. |
| [`UPDATE_TOOLS`](../troubleshooting.md#update_tools) | After its rebuild, `dockingbird update` got each tool you have used once at its latest version, or found the one you have is the latest, and says which; when the channel names an older version than the one you have, the one you have stays. |
| [`PIN_DONE`](../troubleshooting.md#pin_done) | You ran `dockingbird pin` with a tool and a version, and it wrote that version into `versions.toml` in your Dockingbird folder. |
| [`PIN_FOLLOWS`](../troubleshooting.md#pin_follows) | You ran `dockingbird pin --clear`, or `pin` with `latest` or (Claude Code only) `stable`. |
| [`PIN_INVALID_VERSION`](../troubleshooting.md#pin_invalid_version) | The version you gave `dockingbird pin` isn't a release number like `2.1.285`, `latest`, or (Claude Code only) `stable`. |
| [`PIN_ARGUMENTS_REQUIRED`](../troubleshooting.md#pin_arguments_required) | You ran `dockingbird pin` without a tool and a version, or gave `--clear` a version too. |
| [`UPDATE_LOCAL_INSTALL`](../troubleshooting.md#update_local_install) | You installed Dockingbird from a folder on this computer, so `update` doesn't change its version; it still rebuilds Dockingbird. |
| [`UPDATE_COMMIT_INSTALL`](../troubleshooting.md#update_commit_install) | You installed Dockingbird pinned to one commit (`uv tool install git+...@<commit>`), or from a tag that is no release tag, which never moves, so `update` doesn't change its version; it still rebuilds Dockingbird. |
| [`UPDATE_BRANCH_GONE`](../troubleshooting.md#update_branch_gone) | You installed Dockingbird from a branch (`uv tool install git+...@<branch>`), and the source no longer has that branch, so `update` doesn't change its version; it still rebuilds Dockingbird. |
| [`UPDATE_NOT_SET_UP`](../troubleshooting.md#update_not_set_up) | You ran `dockingbird update` before the first set-up. |
| [`UPDATE_LATEST`](../troubleshooting.md#update_latest) | `dockingbird update` (or `update --check`) found nothing newer: for an install from a release tag, no release tag above the one you installed; `update --check` names that tag. |
| [`UPDATE_AVAILABLE`](../troubleshooting.md#update_available) | `dockingbird update --check` found a newer version. |
| [`UPDATE_RELEASE_AVAILABLE`](../troubleshooting.md#update_release_available) | You installed Dockingbird from a release tag (`uv tool install git+...@v0.1.0`), and `dockingbird update --check` found a newer release tag; `dockingbird update` moves to it. |
| [`UPDATE_FINISHING`](../troubleshooting.md#update_finishing) | You upgraded the command yourself (with uv), so the next command finishes the update by rebuilding Dockingbird. |
| [`UPDATE_UV_FAILED`](../troubleshooting.md#update_uv_failed) | Installing the new Dockingbird with uv failed. |
| [`UPDATE_CHECK_FAILED`](../troubleshooting.md#update_check_failed) | `dockingbird update --check` (or, for an install from a release tag, `dockingbird update`, which reads the source's release tags first) couldn't read the source's versions from the source repository: the network is down, or git on this Mac can't read that private repository over https (the operator guide's Install section gives the one-time git line for it); or the source lists no release tag at all. |
| [`UPDATE_SCRIPT_FAILED`](../troubleshooting.md#update_script_failed) | `dockingbird update` got the new version, but the new version couldn't start its rebuild. |
| [`UPDATE_PROGRAM_IN_USE`](../troubleshooting.md#update_program_in_use) | You ran `dockingbird update` while an earlier update still uses the folder the new version goes into (it is installing or removing it), so nothing changed. |
| [`UPDATE_POINTER_FAILED`](../troubleshooting.md#update_pointer_failed) | `dockingbird update` installed the new version in a folder of its own but couldn't point your `dockingbird` command at it: a file or a folder stands where the link goes, uv named no folder for its commands, or a rename failed. |
| [`UPDATE_PROGRAM_BROKEN`](../troubleshooting.md#update_program_broken) | The folder your `dockingbird` command points at is no longer the whole release: part of it was changed or removed by hand, since Dockingbird never writes a folder after it installs it. |
| [`UPDATE_PLACE_FAILED`](../troubleshooting.md#update_place_failed) | `dockingbird update` placed Dockingbird in a folder of its own and ran itself again from there, but that run didn't find itself in the folder (the command's link was moved in between), so it changed nothing. |
| [`UPDATE_MOVING_PYTHON`](../troubleshooting.md#update_moving_python) | `dockingbird update` found Dockingbird's own tool on a Python other than 3.12, as an install made before this change is, and moves it with `uv tool upgrade --python 3.12 dockingbird` before it rebuilds. |
| [`UPDATE_PYTHON_MOVE_FAILED`](../troubleshooting.md#update_python_move_failed) | `dockingbird update` ran `uv tool upgrade --python 3.12 dockingbird` to move Dockingbird's own tool to Python 3.12, and uv failed, or Dockingbird found no uv. |
| [`UPDATE_PYTHON_NOT_MOVED`](../troubleshooting.md#update_python_not_moved) | `dockingbird update` moved Dockingbird's tool to Python 3.12, but the moved program still ran on another Python, so it stopped instead of moving it again. |
| [`UPDATE_PLACING`](../troubleshooting.md#update_placing) | You ran `dockingbird update` on a Dockingbird installed the earlier way, straight into uv's own folder: before it updates, it places the version you have in a folder of its own, points your `dockingbird` command at it and runs the update again from there. |
| [`UPDATE_MIGRATES`](../troubleshooting.md#update_migrates) | You ran `dockingbird update`, and the new version changes the records Dockingbird keeps. |
| [`UPDATE_ROLLING`](../troubleshooting.md#update_rolling) | You ran `dockingbird update`: the new version takes over now, and each agent the line names takes it at its next stopping point, between its turns, keeping its conversation; agents at a terminal keep theirs until their terminal closes. |
| [`UPDATE_NO_ROLL_FLOOR`](../troubleshooting.md#update_no_roll_floor) | You ran `dockingbird update` while agents are working, and the Dockingbird that runs is too old to give its agents a new version in place. |
| [`UPDATE_VERSION_UNKNOWN`](../troubleshooting.md#update_version_unknown) | You ran `dockingbird update`, and the Dockingbird running in this home doesn't say which version it is, or says something that isn't a version, so `update` can't tell whether the new version is newer or older. |
| [`UPDATE_DOWNGRADE_RUNS`](../troubleshooting.md#update_downgrade_runs) | You ran `dockingbird update` from a program older than the Dockingbird running in this home while agents are working, each named with the version it runs: an older version can't take over from a newer one while agents work. |
| [`UPDATE_IN_PROGRESS`](../troubleshooting.md#update_in_progress) | You ran `dockingbird update` while another `update` on this computer is installing a version or switching to one. |
| [`UPDATE_SWITCHING`](../troubleshooting.md#update_switching) | Dockingbird is switching to the version `dockingbird update` installed, and your command waits until the switch is done, then goes on. |
| [`UPDATE_SWITCH_UNDER_WAY`](../troubleshooting.md#update_switch_under_way) | Your command met a newer Dockingbird in the middle of its work, where it can't wait for the switch, so it started the switch and stopped. |
| [`UPDATE_SWITCH_FAILED`](../troubleshooting.md#update_switch_failed) | The switch to the version `dockingbird update` installed didn't work, so the older version still runs, and your commands with it. |
| [`UPDATE_SWITCHED_UNDER`](../troubleshooting.md#update_switched_under) | Dockingbird switched to the version `dockingbird update` installed while your command ran, so the command stopped; run it again. |
| [`UPDATE_TWO_PROGRAMS`](../troubleshooting.md#update_two_programs) | Two `dockingbird` programs with different code use this home, such as the one on your path and a checkout's, or the GUI's. |
| [`UPDATE_STAGE_UNREADABLE`](../troubleshooting.md#update_stage_unreadable) | You ran `dockingbird update`, and the record of an update staged in this home (`update/stage.json`) can't be read: it was changed, or a newer Dockingbird wrote it. |
| [`UPDATE_SWITCH_OLDER_ENDED`](../troubleshooting.md#update_switch_older_ended) | Dockingbird's log, `dockingbird.log` in its `logs` folder, has this line when an update is staged here while the older Dockingbird's process that finishes an update once the agents end was still running: that process can't read the new update, so Dockingbird ended it and started its own, which finishes the update. |
| [`SWITCH_CODE_UNKNOWN`](../troubleshooting.md#switch_code_unknown) | You ran `dockingbird set NAME --switch-code KEY`, and this home has no Dockingbird code by that key, so nothing was asked of the agent. |
| [`SWITCH_NO_SPEC`](../troubleshooting.md#switch_no_spec) | You ran `dockingbird set NAME --switch-code KEY` with a key that changes Dockingbird's engine. |
| [`STATE_FILE_UNREADABLE`](../troubleshooting.md#state_file_unreadable) | `dockingbird mcp install` can't read Dockingbird's `state.json`: it is damaged, too large or not a plain file. |
