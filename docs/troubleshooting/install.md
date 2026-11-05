---
title: "Troubleshooting index: install, Docker, licensing and the command line"
summary: "The 63 message ids about installing, Docker, the license and typing a command, each with when it appears."
audience: first-day
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: install, Docker, licensing and the command line

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 63 ids about installing, Docker, the license and typing a command.

| Id | When it appears |
|---|---|
| [`UNKNOWN_COMMAND`](../troubleshooting.md#unknown_command) | You typed a word where a command goes, and it isn't one of Dockingbird's commands. |
| [`SETTING_REFUSED`](../troubleshooting.md#setting_refused) | A setting in your shell (a variable with Dockingbird's prefix) can't be given to Dockingbird's containers as it stands, so the command stops before it runs rather than ignore it: its value isn't a whole number within the setting's range, two or more values break a rule between settings, its name is spelled in another case than upper case, or it is a setting of Dockingbird outside Docker (the database's address and roles, the developer's role switch and the host git's path), which Docker mode never uses. |
| [`UNKNOWN_OPTION`](../troubleshooting.md#unknown_option) | You gave an option the command doesn't have. |
| [`MISSING_VALUE`](../troubleshooting.md#missing_value) | You gave an option without the value it needs. |
| [`MISSING_ARGUMENT`](../troubleshooting.md#missing_argument) | You ran a command without the choice it needs, such as `dockingbird login` with no tool. |
| [`UNKNOWN_CHOICE`](../troubleshooting.md#unknown_choice) | You gave a choice the command doesn't have. |
| [`UNEXPECTED_ARGUMENT`](../troubleshooting.md#unexpected_argument) | You gave the command a word it has no place for. |
| [`OPTION_NEEDS_OPTION`](../troubleshooting.md#option_needs_option) | You gave an option that only works together with another one. |
| [`OPTIONS_NOT_BOTH`](../troubleshooting.md#options_not_both) | You gave two options that don't go together, such as a start's `--bus` with `--terminal`, or `dockingbird inbox --clear` with another inbox option. |
| [`OPTION_GIVEN_TWICE`](../troubleshooting.md#option_given_twice) | You gave `--agent-md` or `--claude-md` twice on one command. |
| [`NOT_BUILT_YET`](../troubleshooting.md#not_built_yet) | You ran a command this version doesn't have yet, or the MCP server was asked to start an agent at a terminal: it starts agents without one. |
| [`INTERNAL_ERROR`](../troubleshooting.md#internal_error) | Something went wrong that Dockingbird has no words for. |
| [`DOCKER_NOT_RUNNING`](../troubleshooting.md#docker_not_running) | Docker isn't running, and didn't start in time. |
| [`DOCKER_ANSWERING_SLOWLY`](../troubleshooting.md#docker_answering_slowly) | Docker is running but answers too slowly, as on a Mac too busy for it or a Docker Desktop in trouble. |
| [`DOCKER_STARTING`](../troubleshooting.md#docker_starting) | Docker Desktop wasn't running, so Dockingbird started it. |
| [`DOCKER_WAKING`](../troubleshooting.md#docker_waking) | Docker Desktop was asleep (its Resource Saver stops it when idle) or still starting, so Dockingbird waits for it to answer. |
| [`DOCKER_NOT_ANSWERING`](../troubleshooting.md#docker_not_answering) | Docker took a request and never answered: it is stuck, not off. |
| [`DOCKER_NOT_INSTALLED`](../troubleshooting.md#docker_not_installed) | There is no `docker` command on this computer. |
| [`DOCKER_UNSTARTED`](../troubleshooting.md#docker_unstarted) | There is a `docker` command on this computer, but it couldn't be run: the file is being replaced (Docker Desktop updating itself), it was removed, or the computer has no process or open file left for it. |
| [`DOCKER_BUILDX_MISSING`](../troubleshooting.md#docker_buildx_missing) | Dockingbird was about to build itself (during the set-up, or the rebuild that finishes an update), and Docker has no buildx plugin, which runs that build. |
| [`NOT_APPLE_SILICON`](../troubleshooting.md#not_apple_silicon) | This computer is neither an Apple silicon Mac nor arm64 Linux, the two Dockingbird runs on for now. |
| [`SETTING_UP`](../troubleshooting.md#setting_up) | The first command that needs Dockingbird to be set up, usually `dockingbird claude` or `dockingbird login`, sets it up, once. |
| [`BUILD_QUIET`](../troubleshooting.md#build_quiet) | The set-up (or an update's rebuild) has printed nothing for a while. |
| [`BUILD_QUIET_CHECK`](../troubleshooting.md#build_quiet_check) | The set-up has been quiet for several minutes, so a slow network or a stuck Docker is likely. |
| [`SETUP_INTERRUPTED`](../troubleshooting.md#setup_interrupted) | You pressed Ctrl-C during the set-up. |
| [`IMAGE_BUILD_FAILED`](../troubleshooting.md#image_build_failed) | Setting up Dockingbird failed. |
| [`DOCKER_STOPPED_ANSWERING`](../troubleshooting.md#docker_stopped_answering) | Docker took the build but never started it, twice: Docker Desktop may be paused or still starting, or the base system couldn't be downloaded. |
| [`IMAGE_SOURCE_UNAVAILABLE`](../troubleshooting.md#image_source_unavailable) | This install of Dockingbird is missing the files it sets up from. |
| [`DOCKINGBIRD_STARTING`](../troubleshooting.md#dockingbird_starting) | Dockingbird had stopped (it stops when idle, or after a restart) and is starting again. |
| [`COORDINATOR_UNHEALTHY`](../troubleshooting.md#coordinator_unhealthy) | Dockingbird's container started but didn't report ready. |
| [`LOGS_NOT_VISIBLE`](../troubleshooting.md#logs_not_visible) | Docker Desktop can't see Dockingbird's log folder, though it is there. |
| [`COORDINATOR_ROLLED_BACK`](../troubleshooting.md#coordinator_rolled_back) | An update's new version didn't start, so the version you had is running again. |
| [`SETTINGS_CHANGED`](../troubleshooting.md#settings_changed) | Dockingbird was started with other settings (the variables with its prefix in that shell) than this terminal gives now, and a running Dockingbird keeps the settings it started with. |
| [`DOCKER_ARGV_REFUSED`](../troubleshooting.md#docker_argv_refused) | Dockingbird stopped one of its own Docker commands because it broke a safety rule. |
| [`NOT_A_GIT_REPO`](../troubleshooting.md#not_a_git_repo) | You ran a command that works on a repo, in a folder that isn't in a git repo. |
| [`COORDINATOR_RESHAPING`](../troubleshooting.md#coordinator_reshaping) | A connection that uses your Mac's ssh-agent was added, or the last one was disconnected, while no agent ran, so Dockingbird restarted to take Docker Desktop's forwarded ssh-agent, or to give it back. |
| [`COORDINATOR_RESHAPE_LATER`](../troubleshooting.md#coordinator_reshape_later) | A connection that uses your Mac's ssh-agent was added, or the last one was disconnected, while agents run. |
| [`COORDINATOR_AGENT_SOCKET_MISSING`](../troubleshooting.md#coordinator_agent_socket_missing) | Dockingbird started, and Docker had no ssh-agent socket for it, so it started without your Mac's ssh-agent: this Docker is not Docker Desktop, or Docker Desktop lost its socket. |
| [`HELP_CONFIG_COMMAND`](../troubleshooting.md#help_config_command) | You ran `dockingbird -h` in a repo whose `.dockingbird/` folder, or a config you added with `dockingbird config add`, gives agents a command of its own. |
| [`LICENSE_SHOWN`](../troubleshooting.md#license_shown) | You ran `dockingbird license status`. |
| [`LICENSE_ACTIVATED`](../troubleshooting.md#license_activated) | You ran `dockingbird license activate` and pasted or piped your key: this computer is now linked to that license, and the line under it says how many computers are linked (with an older license program, how many seats are in use). |
| [`LICENSE_TRIAL_STARTED`](../troubleshooting.md#license_trial_started) | You ran `dockingbird license trial`: this computer's trial started, and the line says until when. |
| [`LICENSE_RELEASED`](../troubleshooting.md#license_released) | You ran `dockingbird license deactivate`: this computer's seat is free for another computer, and its license is gone from it. |
| [`LICENSE_ACTIVATIONS`](../troubleshooting.md#license_activations) | You ran `dockingbird license activations` with your key: one line for each computer linked to the license, with the day it was activated and the day it was last seen, and how to free one with `--release`. |
| [`LICENSE_ACTIVATION_RELEASED`](../troubleshooting.md#license_activation_released) | You ran `dockingbird license activations --release` with an activation's id: that computer no longer uses a seat, and the list that follows is without it. |
| [`LICENSE_NOTE`](../troubleshooting.md#license_note) | You started an agent, and the license has something to say: its term ends soon, the license server hasn't answered lately, it ended and its grace time runs, or it can't be used while licensing isn't enforced. |
| [`LICENSE_REFUSED`](../troubleshooting.md#license_refused) | You started an agent, and the license doesn't allow new agents: this computer has none, its term ended, the license server hasn't answered for too long, the license authority ended it, its seat was freed elsewhere, the license file belongs to another computer or can't be read, or it needs a newer Dockingbird. |
| [`LICENSE_CLIENT_DAMAGED`](../troubleshooting.md#license_client_damaged) | Dockingbird's license program is missing, took too long, or answered something Dockingbird can't read. |
| [`LICENSE_CLIENT_UNAVAILABLE`](../troubleshooting.md#license_client_unavailable) | You started an agent, and Dockingbird couldn't download its license program from the license authority; the line says why (no network, the server's answer, a timeout). |
| [`LICENSE_CLIENT_DIGEST_MISMATCH`](../troubleshooting.md#license_client_digest_mismatch) | Dockingbird downloaded its license program, and the file isn't the one this version of Dockingbird expects, so it wasn't kept. |
| [`LICENSE_CLIENT_PATH_INVALID`](../troubleshooting.md#license_client_path_invalid) | The variable that names a license program of your own is set in your shell, and it isn't the full path of an existing program. |
| [`LICENSE_PLATFORM_UNSUPPORTED`](../troubleshooting.md#license_platform_unsupported) | Dockingbird's license program is made for Apple silicon Macs and arm64 Linux, and this computer is neither. |
| [`LICENSE_AUTHORITY_UNAVAILABLE`](../troubleshooting.md#license_authority_unavailable) | Dockingbird couldn't reach the license server, to download its license program or for a `dockingbird license` action. |
| [`LICENSE_AUTHORITY_REFUSED`](../troubleshooting.md#license_authority_refused) | A `dockingbird license` action didn't work for a reason Dockingbird has no words of its own for, so the line shows what the license program said. |
| [`LICENSE_SEATS_FULL`](../troubleshooting.md#license_seats_full) | You ran `dockingbird license activate`, and the license's seats already link every computer they admit: its seats times the computers each seat may link. |
| [`LICENSE_KEY_INVALID`](../troubleshooting.md#license_key_invalid) | The key you pasted or piped isn't one the license authority knows, or isn't a key at all: `ZF-` then five groups of five letters or digits. |
| [`LICENSE_TRIAL_USED`](../troubleshooting.md#license_trial_used) | You ran `dockingbird license trial`, and this computer has had its trial. |
| [`LICENSE_KEY_IN_ARGV`](../troubleshooting.md#license_key_in_argv) | You typed a license key on the command line, where other programs and your shell history can read it. |
| [`LICENSE_SEAT_STILL_HELD`](../troubleshooting.md#license_seat_still_held) | You ran `dockingbird clean --all`, and the license server didn't answer, so this computer still uses a seat. |
| [`LICENSE_UPDATE_NEEDS_LICENSE`](../troubleshooting.md#license_update_needs_license) | `dockingbird update` (or `--check`) on an install from the release index found no activation on this computer: the index serves new versions only to an activated computer, with the download token its activation came with. |
| [`LICENSE_TERMS`](../troubleshooting.md#license_terms) | You activated this computer or started a trial: the line says where the terms you use Dockingbird under are. |
| [`LICENSE_OPTION_INVALID`](../troubleshooting.md#license_option_invalid) | You gave `dockingbird license` a `--label`, `--accept-terms` or `--release` value the license program doesn't take: a label is letters, digits, `-` and `.`, a terms version the same and `_`, an activation's id letters, digits, `-` and `_`. |
| [`LICENSE_KEY_PROMPT`](../troubleshooting.md#license_key_prompt) | You ran `dockingbird license activate` or `activations` in a terminal: paste your license key; it isn't shown as you paste it. |
