---
title: "Troubleshooting index: homes, checkouts and toolchains"
summary: "The 113 message ids about Dockingbird homes, your checkout and its branches, init, toolchains, project rules and trust, each with when it appears."
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: homes, checkouts and toolchains

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 113 ids about Dockingbird homes, your checkout and its branches, init, toolchains, project rules and trust.

| Id | When it appears |
|---|---|
| [`ENV_NAME_UNKNOWN`](../troubleshooting.md#env_name_unknown) | A variable in your shell starts with Dockingbird's prefix but isn't a setting any Dockingbird command reads: a retired or misspelled name, or one spelled with a character outside plain ASCII. |
| [`HOME_TWICE`](../troubleshooting.md#home_twice) | You gave `--home NAME` before the command while `DOCKINGBIRD_HOME` was set, or gave `--home` twice. |
| [`HOME_NAME_INVALID`](../troubleshooting.md#home_name_invalid) | You gave `--home` a word that isn't a home's name: a name is lowercase letters, digits and `-`, starting with a letter or a digit, such as `lab`. |
| [`HOME_SETUP_TOOK_TOO_LONG`](../troubleshooting.md#home_setup_took_too_long) | Dockingbird sets up each tool's home the first time it starts, and this took longer than Dockingbird waits, usually because the computer was busy. |
| [`HOME_NOT_SHARED`](../troubleshooting.md#home_not_shared) | Docker Desktop doesn't share the folder Dockingbird keeps its files in, so its container can't use it. |
| [`HOME_IS_NATIVE`](../troubleshooting.md#home_is_native) | `DOCKINGBIRD_HOME` points at a folder a native-mode Dockingbird uses, which Docker mode can't share. |
| [`HOME_UNSAFE`](../troubleshooting.md#home_unsafe) | `DOCKINGBIRD_HOME` isn't a full path, points through a link or at someone else's folder, or has a character Docker can't take in a path. |
| [`HOME_NOT_EMPTY`](../troubleshooting.md#home_not_empty) | The folder Dockingbird would keep its files in already has files it didn't make, so it leaves it alone. |
| [`TOOL_GETTING`](../troubleshooting.md#tool_getting) | The tool isn't downloaded yet, or you pinned a version that isn't, so Dockingbird fetches it before the command goes on; or a newer release is out, and a start waits a short while for it (the line shows the download's progress) before it runs the version you have instead. |
| [`TOOL_FETCH_FAILED`](../troubleshooting.md#tool_fetch_failed) | A newer version couldn't be downloaded this time (offline, a slow connection, the download store busy or Docker's disk full), so the version you have runs. |
| [`TOOL_VERIFY_FAILED`](../troubleshooting.md#tool_verify_failed) | A download's signature, digest or size didn't match the vendor's, so it wasn't installed and that version is set aside until `dockingbird update`. |
| [`TOOL_BROKEN`](../troubleshooting.md#tool_broken) | The new version was downloaded and verified but didn't print its version when Dockingbird ran it, so Dockingbird keeps the version you have and sets the new one aside until `dockingbird update`. |
| [`TOOL_CHECK_FAILED`](../troubleshooting.md#tool_check_failed) | Dockingbird couldn't run the new version's check (Docker didn't answer in time), so the version you have runs, the download is kept and nothing is set aside; the next start checks it again without downloading it. |
| [`TOOL_NOT_AVAILABLE`](../troubleshooting.md#tool_not_available) | This is the tool's first run on this Mac and it couldn't be downloaded (no network, or the download host didn't answer). |
| [`TOOL_PIN_NOT_FOUND`](../troubleshooting.md#tool_pin_not_found) | Your `versions.toml` pins the tool to a version the vendor doesn't have and that isn't downloaded. |
| [`TOOL_PIN_INVALID`](../troubleshooting.md#tool_pin_invalid) | Your `versions.toml` (in your Dockingbird folder) couldn't be read: one line per tool, `claude` or `codex`, then a quoted version like "2.1.285", or "latest", or (Claude Code only) "stable"; nothing else, and the file must be a plain file of yours. |
| [`TOOL_CHECK_SKIPPED`](../troubleshooting.md#tool_check_skipped) | `--verbose` only: the version you have is the latest, or the one you pinned, so there was nothing to fetch; or the quick check for a newer release gave no answer (offline, or the answer couldn't be read), or named an older version than the one you have, which stays. |
| [`TOOL_FETCHING`](../troubleshooting.md#tool_fetching) | An agent started over MCP (by your own harness, through `dockingbird mcp`) found the tool still downloading and no version of it to run yet: a start over MCP doesn't wait for a download. |
| [`TOOL_STILL_DOWNLOADING`](../troubleshooting.md#tool_still_downloading) | A newer version is downloading and didn't arrive within the time a start waits, so this start runs the version you have; when another command (an `update`, or a start in another terminal) is doing the download, the line says so and the next start checks again. |
| [`TOOL_PRUNE_FAILED`](../troubleshooting.md#tool_prune_failed) | `--verbose` only: removing a tool's unused versions from the download store didn't work this time. |
| [`TOOL_STORE_BUSY`](../troubleshooting.md#tool_store_busy) | `clean`, `update` or another start is removing that tool's unused versions; run the command again in a minute. |
| [`DETACHED_HEAD`](../troubleshooting.md#detached_head) | Your checkout is on no branch (a detached HEAD), and Dockingbird works on branches. |
| [`EMPTY_REPO`](../troubleshooting.md#empty_repo) | The repo has no commits yet, so there is nothing to copy. |
| [`WORKTREE_NOT_YET`](../troubleshooting.md#worktree_not_yet) | You ran Dockingbird in a git worktree, which it doesn't support yet. |
| [`SUBMODULE_NOT_YET`](../troubleshooting.md#submodule_not_yet) | You ran Dockingbird inside a submodule, which it doesn't support yet. |
| [`REPO_LINKING`](../troubleshooting.md#repo_linking) | The first start on a branch copies its history for the agents. |
| [`REPO_NAME_TAKEN`](../troubleshooting.md#repo_name_taken) | Another checkout already has this folder's name, so this one gets a numbered name, which its lines and `status` use. |
| [`REPO_LINK_TOOK_TOO_LONG`](../troubleshooting.md#repo_link_took_too_long) | Copying the branch for the agents took too long, so it stopped. |
| [`REPO_DISK_FULL`](../troubleshooting.md#repo_disk_full) | The first start on a branch copies its history to the agents' disk (Docker's virtual disk), and that disk ran out of room for it: the message shows the free space. |
| [`LINK_TREE_POLICY`](../troubleshooting.md#link_tree_policy) | The branch has files the agents don't take: a symlink that points outside the repo, by an absolute path, into `.git`, in a loop or to nothing usable, or one in place of a git file such as `.gitignore`; a submodule; or a Git LFS file. |
| [`REPO_RELINKED`](../troubleshooting.md#repo_relinked) | You cloned a repo again at the same place, made a branch again from the agents' copy after deleting it (`git switch -c feature/x dockingbird/feature/x`), or said yes when Dockingbird asked about a new branch with a deleted branch's name, and Dockingbird linked it back to the agents' copy it had. |
| [`BRANCH_NAME_REUSED`](../troubleshooting.md#branch_name_reused) | You started an agent or ran `dockingbird sync` on a branch you made under the name of a branch you deleted, and that branch's agents' copy has commits the new one doesn't. |
| [`NOTHING_LINKED`](../troubleshooting.md#nothing_linked) | You said no (or pressed Ctrl-C) when Dockingbird asked whether a branch with a deleted branch's name should carry on from that branch's agents' commits, or there was no terminal to ask on. |
| [`BRANCH_NAME_UNSUPPORTED`](../troubleshooting.md#branch_name_unsupported) | The branch's name has characters the agents' copy can't hold. |
| [`REPO_HISTORY_REFUSED`](../troubleshooting.md#repo_history_refused) | The branch's history has an object git's strict checks refuse, often from an old tool. |
| [`REPO_LINK_REFUSED`](../troubleshooting.md#repo_link_refused) | Dockingbird refused to copy the branch for the agents, for a reason no other message covers: the message names the reason and, when there is one, the field it refused. |
| [`REPO_RELEASED`](../troubleshooting.md#repo_released) | You ran `dockingbird repo release --repository R` and Dockingbird released that repository: it no longer lists it, and the next start in its folder copies the branch again. |
| [`REPO_RELEASE_NO_ANSWER`](../troubleshooting.md#repo_release_no_answer) | You ran `dockingbird repo release`, and its call inside Dockingbird could not start, ran out of time, or gave a reply Dockingbird could not read; the message names which. |
| [`LINK_NO_ANSWER`](../troubleshooting.md#link_no_answer) | Dockingbird didn't answer while it linked the branch. |
| [`REPOS_FILE_UNREADABLE`](../troubleshooting.md#repos_file_unreadable) | Dockingbird's list of linked repos can't be read: it is a link, not yours, too large, or not in its format. |
| [`LINK_INVALID`](../troubleshooting.md#link_invalid) | The branch's Dockingbird link in `.git/config` has something that isn't a link Dockingbird made. |
| [`TREE_ROW`](../troubleshooting.md#tree_row) | One file in a list of files the agents don't take, with its kind: a submodule or a Git LFS file. |
| [`TREE_LINK_ROW`](../troubleshooting.md#tree_link_row) | One symlink in a list of files the agents don't take: its path, where it points, and why it isn't taken. |
| [`TRUST_NOTE`](../troubleshooting.md#trust_note) | The first attached start of a tool on a repo (`dockingbird claude` or `codex`, or `start --terminal`) where the repo's own settings are off: a repo that isn't trusted on this Mac (one you marked with `dockingbird trust --off`, or one with no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`), a command whose config leaves them off, or a tool whose sign-in isn't yet proven safe from them. |
| [`LINK_ROW`](../troubleshooting.md#link_row) | One symlink the agents added or changed, and where it points. |
| [`NOTHING_NEEDS_YOU`](../troubleshooting.md#nothing_needs_you) | The last line of `status` when nothing needs you. |
| [`NOTHING_RUNNING`](../troubleshooting.md#nothing_running) | You ran `dockingbird stop`, and nothing was running. |
| [`NOTHING_TO_CLEAN`](../troubleshooting.md#nothing_to_clean) | `dockingbird clean` found nothing to remove. |
| [`TRUSTED`](../troubleshooting.md#trusted) | You ran `dockingbird trust` in a repo: Dockingbird marks the repo trusted on your Mac, whatever `config.toml`'s `trust` line says, removing the mark `dockingbird trust --off` left, if any, and the repo's own settings, hooks and MCP servers load in agents started there. |
| [`TRUST_PIN_UNPROVEN`](../troubleshooting.md#trust_pin_unproven) | After `dockingbird trust`, for each tool whose sign-in Dockingbird has not yet proven safe from a repo's own settings: that tool keeps them off for now, trusted or not. |
| [`TRUST_FORGOTTEN`](../troubleshooting.md#trust_forgotten) | You ran `dockingbird trust --off` (or `--forget`, the same): Dockingbird marks the repo untrusted, on your Mac only, and its own settings, hooks and MCP servers stay off in agents started there until you run `dockingbird trust` in it. |
| [`TRUST_NOT_A_CHECKOUT`](../troubleshooting.md#trust_not_a_checkout) | You ran `dockingbird trust` outside a git repo, or named a folder that is not in one, so nothing was recorded. |
| [`TRUST_CONFIG_INVALID`](../troubleshooting.md#trust_config_invalid) | You started an agent, or ran `dockingbird -h` or `dockingbird config list` in a repo, and `config.toml` in Dockingbird's folder can't be read as written: its `trust` line, which sets whether a repo you haven't marked is trusted, is something other than `"trusted"` or `"untrusted"`, or the file isn't TOML, or it isn't a plain file of yours Dockingbird can read (a link, which Dockingbird never follows there, a folder, a file too large or not UTF-8). |
| [`REPO_SETTINGS_OFF`](../troubleshooting.md#repo_settings_off) | You started an agent in a repo that isn't trusted on this Mac (one you marked with `dockingbird trust --off`, or one with no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`; every other repo is trusted), or a command whose config leaves `repo_settings` off: the repo's own settings, hooks and MCP servers don't load in it. |
| [`INIT_NOT_A_CHECKOUT`](../troubleshooting.md#init_not_a_checkout) | You ran `dockingbird init` in a folder that is not in a git repo, so nothing was written. |
| [`INIT_INSIDE_HOME`](../troubleshooting.md#init_inside_home) | You ran `dockingbird init` inside a Dockingbird home, the folder Dockingbird keeps its own files in, so nothing was written. |
| [`INIT_SLUG_INVALID`](../troubleshooting.md#init_slug_invalid) | You ran `dockingbird init` with a `--project` name, or in a repo whose own name, that is not a project name: lowercase letters, digits and `-`. |
| [`INIT_PROJECT_FILE_INVALID`](../troubleshooting.md#init_project_file_invalid) | You ran `dockingbird init` in a repo whose `.dockingbird/project.toml` has a key or a value Dockingbird doesn't read, or is not a file it can read. |
| [`INIT_SKILLS_LINK_FOREIGN`](../troubleshooting.md#init_skills_link_foreign) | You ran `dockingbird init` in a repo whose `.claude/skills` is a link to another folder than `.agents/skills`, so nothing was written. |
| [`INIT_LOCK_INVALID`](../troubleshooting.md#init_lock_invalid) | You ran `dockingbird init` in a repo whose `.dockingbird/skills.lock` is not one Dockingbird can read. |
| [`INIT_ROLE_INDEX_INVALID`](../troubleshooting.md#init_role_index_invalid) | You ran `dockingbird init` in a repo whose `.dockingbird/roles/index.toml` is not one Dockingbird can read. |
| [`INIT_WRITE_FAILED`](../troubleshooting.md#init_write_failed) | `dockingbird init` could not write a file into the repo, for the reason shown, a full disk or a folder you can't write for example. |
| [`INIT_PATH_IS_LINK`](../troubleshooting.md#init_path_is_link) | You ran `dockingbird init` in a repo where a folder it writes into, such as `.claude` or `.agents`, or one of its files, is a link, is someone else's, or is a file where a folder belongs (or the other way round). |
| [`INIT_SKILLS_TWICE`](../troubleshooting.md#init_skills_twice) | Your repo has a `.claude/skills` folder of its own, so `dockingbird init` put the skills both there and in `.agents/skills`. |
| [`INIT_NO_REMOTE`](../troubleshooting.md#init_no_remote) | Your repo has no remote named `origin`, so `dockingbird init` named the project after the repo's folder. |
| [`INIT_NOT_REGISTERED`](../troubleshooting.md#init_not_registered) | `dockingbird init` made the repo ready without adding the project to your organisation's store: this computer is not logged in with `dockingbird org login`, you gave `--no-register`, your org login is not an admin of the store, the store isn't made yet (an admin runs `dockingbird org create`), or the store didn't answer or refused, in the words the line ends with. |
| [`INIT_REGISTERED`](../troubleshooting.md#init_registered) | `dockingbird init` added the project to your organisation's store, with the repo's address, its default branch and this release. |
| [`INIT_ALREADY_REGISTERED`](../troubleshooting.md#init_already_registered) | `dockingbird init` found the project in your organisation's store already and left it as it is. |
| [`INIT_FILE_EDITED`](../troubleshooting.md#init_file_edited) | `dockingbird init` found files it installed that you changed, and kept them as they are. |
| [`INIT_UPDATED`](../troubleshooting.md#init_updated) | `dockingbird init` replaced the files this release changed, and wrote the ones that were missing; with `--check`, the files it would change. |
| [`INIT_DONE`](../troubleshooting.md#init_done) | `dockingbird init` wrote what your repo needs: the first time, the project file, its rules, an example swarm, the skills and their agents, with the commands that come next. |
| [`INIT_CURRENT`](../troubleshooting.md#init_current) | `dockingbird init` found everything it writes as this release has it, so nothing changed. |
| [`INIT_OUT_OF_DATE`](../troubleshooting.md#init_out_of_date) | You ran `dockingbird init --check`, and `dockingbird init` would change files in the repo: they are not this release's. |
| [`RULES_FILE_MISSING`](../troubleshooting.md#rules_file_missing) | You started an agent in a repo whose `.dockingbird/project.toml` names a rules file in `[rules] file` that is not there, so no agent started. |
| [`RULES_FILE_INVALID`](../troubleshooting.md#rules_file_invalid) | You started an agent in a repo whose rules file Dockingbird can't give agents, for the reason shown, so no agent started. |
| [`RULES_FILE_TOO_LONG`](../troubleshooting.md#rules_file_too_long) | You started an agent in a repo whose rules file, with Dockingbird's own rules, is longer than an agent's rules may be, so no agent started. |
| [`HOMES_ROW`](../troubleshooting.md#homes_row) | You ran `dockingbird homes`: each line is a Dockingbird home on this computer (each `DOCKINGBIRD_HOME`, the default one included), its folder or its name, whether its Dockingbird runs, and its version. |
| [`HOME_PATH_DEPRECATED`](../troubleshooting.md#home_path_deprecated) | You gave `--host` a home by its folder with `--home`. |
| [`PROJECT_FILE_INVALID`](../troubleshooting.md#project_file_invalid) | A Dockingbird command read your checkout's `.dockingbird/project.toml` and found something it can't take: a key that is unknown or of the wrong type, a `slug` that isn't one, or a file that isn't TOML. |
| [`TOOLCHAIN_SUMMARY`](../troubleshooting.md#toolchain_summary) | You started an agent in a repo. |
| [`TOOLCHAIN_INSTALLING`](../troubleshooting.md#toolchain_installing) | A start, or `dockingbird env install`, found a version the repo names that isn't installed yet, so mise installs it before the agent starts: mise's latest line and the time so far, and how long mise has printed nothing when it is quiet for a while. |
| [`TOOLCHAIN_INSTALL_FAILED`](../troubleshooting.md#toolchain_install_failed) | mise couldn't install a version the repo names (a version that doesn't exist, a download that failed, a checksum that didn't match), or the install ended before it finished. |
| [`TOOLCHAIN_LOOK_FAILED`](../troubleshooting.md#toolchain_look_failed) | mise couldn't read the repo's tool versions, such as from a `mise.toml` that isn't valid, and the message shows what mise said. |
| [`TOOLCHAIN_LOOK_UNAVAILABLE`](../troubleshooting.md#toolchain_look_unavailable) | You ran `dockingbird env` while Docker isn't running, so Dockingbird can't read the versions agents get. |
| [`TOOLCHAIN_LOCK_INVALID`](../troubleshooting.md#toolchain_lock_invalid) | The repo's `mise.lock` can't be read: it isn't valid TOML, a version in it isn't text, or it is too large. |
| [`TOOLCHAIN_STORE_BUSY`](../troubleshooting.md#toolchain_store_busy) | Another start is installing tool versions, for this repo or another one, or `dockingbird clean` is removing unused ones: one of them runs at a time, so this command waits for it, with the time so far, then goes on and uses what it installed. |
| [`TOOLCHAIN_INTERRUPTED`](../troubleshooting.md#toolchain_interrupted) | You pressed Ctrl-C while mise installed the repo's tool versions, or while a start waited for another start's install. |
| [`TOOLCHAIN_FETCHING`](../troubleshooting.md#toolchain_fetching) | Only for an agent that starts another through Dockingbird's tools (the host MCP server): the repo's tool versions are still installing, so the start is refused at once, nothing waits, and the agent tries the start again. |
| [`TOOLCHAIN_RUNNING_DIFFERS`](../troubleshooting.md#toolchain_running_differs) | `dockingbird status` found a running agent whose version of a tool is not the one the repo now asks for: the repo's files changed since it started. |
| [`TOOLCHAIN_ENV_FAILED`](../troubleshooting.md#toolchain_env_failed) | An agent's container couldn't set up its tool versions before the agent started, and the agent ended. |
| [`TOOLCHAIN_LINE_UNREADABLE`](../troubleshooting.md#toolchain_line_unreadable) | Under a failure's message: one of the lines Dockingbird reads from mise's run was too long or not in its form, so its first part is shown as it was printed. |
| [`TOOLCHAIN_ITEM`](../troubleshooting.md#toolchain_item) | One tool version in a list, such as `Python 3.12.7 (mise.toml)` or `Node 20.18.1 (locked)`: the file that names it, or `locked` when `mise.lock` does. |
| [`DEPS_INSTALLING`](../troubleshooting.md#deps_installing) | An agent's container installs the repo's dependencies with the repo's own command (such as `uv sync --locked` or `npm ci`) before the agent starts; the command's own output follows. |
| [`DEPS_INSTALLED`](../troubleshooting.md#deps_installed) | The repo's dependencies were installed before the agent started, and how long it took. |
| [`DEPS_SKIPPED_UNTRUSTED`](../troubleshooting.md#deps_skipped_untrusted) | The checkout is marked untrusted (`dockingbird trust --off`), so the agent starts without the repo's dependencies installed. |
| [`DEPS_FAILED`](../troubleshooting.md#deps_failed) | The command that installs the repo's dependencies failed in the agent's container, and the agent ended. |
| [`DEPS_OFFLINE_REFUSED`](../troubleshooting.md#deps_offline_refused) | The agent's network access (its egress, `none` or `models`) doesn't reach the package registries and the packages aren't cached, so its dependencies couldn't be installed and the agent ended. |
| [`ENV_HEADING`](../troubleshooting.md#env_heading) | The first line of `dockingbird env`'s table: the repo and its branch over its two columns, what the repo wants and what agents get. |
| [`ENV_ROW`](../troubleshooting.md#env_row) | One tool of `dockingbird env`'s table: the version the repo's files ask for and the file that asks, then the version agents get, with `(locked)` when `mise.lock` names it, `(not installed yet)` when it isn't installed, or the image's own when nothing names the tool. |
| [`ENV_NOTE`](../troubleshooting.md#env_note) | Only under `dockingbird --json env`: one line for each note under the table, naming the note, with the note's own facts. |
| [`ENV_DEPENDENCIES`](../troubleshooting.md#env_dependencies) | `dockingbird env` names the commands that install the repo's dependencies before an agent starts, each with its lock file, or says none are installed when the repo has no lock file, or when it names no toolchain (its agents then use Dockingbird's own tool versions and install nothing), or that they are unknown when its `package.json` beside a `yarn.lock` isn't readable JSON. |
| [`ENV_STORE`](../troubleshooting.md#env_store) | `dockingbird env` says how many tool versions Dockingbird has downloaded for agents; `dockingbird clean` removes the unused ones. |
| [`ENV_CHANGE_HINT`](../troubleshooting.md#env_change_hint) | The last line of `dockingbird env`: the command that changes a tool's version in the repo's `mise.toml`. |
| [`ENV_NOT_A_REPO`](../troubleshooting.md#env_not_a_repo) | You ran `dockingbird env` outside a git repo; it reads the repo you are in. |
| [`ENV_INSTALL_DONE`](../troubleshooting.md#env_install_done) | `dockingbird env install` installed the repo's tool versions, or found them installed already, and offers `dockingbird env lock` so every machine gets the same versions; or the repo names no tool version, so there was nothing to install. |
| [`ENV_LOCK_DONE`](../troubleshooting.md#env_lock_done) | `dockingbird env lock` wrote each tool version into the repo's `mise.toml` and locked them in `mise.lock`: commit both so every machine gets the same. |
| [`ENV_USE_WROTE`](../troubleshooting.md#env_use_wrote) | `dockingbird env use` wrote the version into the repo's `mise.toml`, creating it when the repo had none, and says which version agents started from now get. |
| [`ENV_USE_RUNNING`](../troubleshooting.md#env_use_running) | After `dockingbird env use`, the agents already running on the repo keep the versions they started with until you restart them. |
| [`ENV_USE_FAILED`](../troubleshooting.md#env_use_failed) | `dockingbird env use` couldn't set the version: mise couldn't install it, such as offline or for a version that doesn't exist. |
| [`ENV_USE_NOT_A_NUMBER`](../troubleshooting.md#env_use_not_a_number) | You gave `dockingbird env use` a version that isn't a number, such as `lts` or `latest`: Dockingbird pins version numbers. |
| [`ENV_USE_UNKNOWN_TOOL`](../troubleshooting.md#env_use_unknown_tool) | You gave `dockingbird env use` a tool it doesn't know; the message lists the tools it takes. |
| [`RULES_TOOLCHAIN_SENTENCE`](../troubleshooting.md#rules_toolchain_sentence) | Never shown to you: the line an agent's rules file gets about its tool versions and where its own installs go. |
| [`RULES_DEPS_SENTENCE`](../troubleshooting.md#rules_deps_sentence) | Never shown to you: the line an agent's rules file gets about whether the repo's dependencies were installed before it started. |
