---
title: The home folder layout
summary: What lives where under a Dockingbird home, which files you may edit, and how a second home by name works.
audience: daily
commands:
  - dockingbird homes
  - dockingbird --home NAME
  - dockingbird egress
  - dockingbird pin
  - dockingbird clean --all
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# The home folder layout

A Dockingbird home is one folder on your computer, `~/.local/share/dockingbird` by default, plus five Docker volumes that never appear in Finder or in your file listings.
Dockingbird never writes into a folder that lacks the marker file, and `dockingbird clean --all` removes nothing from such a folder.
The folder itself has mode 0700.

## The home folder and DOCKINGBIRD_HOME

| Path | What it holds | Mode |
|---|---|---|
| `.dockingbird-home` | the marker: a small JSON file Dockingbird writes first into a new home; never a link | 0600 |
| `config.toml` | the image tag, the last build's duration (`last_build_seconds`, the next build's estimate) and, yours, a `trust =` line | |
| `egress.toml` | optional; what new agents may reach, written by `dockingbird egress` | 0600 |
| `browser.toml` | optional, yours, in the default home's folder and read for every home of the computer; its one key is `local_network_access`, a list of up to 32 Chrome URL patterns of at most 512 characters, such as `["[*.]example.com"]`, whose pages may reach the local network without Chrome's question; every agent with a browser started afterwards gets them as Chrome's managed policy `LocalNetworkAccessAllowedForUrls`; Dockingbird never writes it, and a file it cannot read or that holds anything else refuses every start of an agent with a browser (`BROWSER_SETTINGS_INVALID`) | |
| `versions.toml` | optional; which version each tool runs, written by `dockingbird pin` or by you | |
| `instructions/claude.md`, `instructions/codex.md` | optional, yours; rules for every agent of that tool in this home | |
| `repos.toml` | each checkout: its display name, path, repo name, branches and their root commits | |
| `hosts.toml` | the other computers you reach; see [hosts-file.md](hosts-file.md) | 0600 when Dockingbird writes it |
| `fleet.toml` | optional, yours; the older form of the fleet database login, see [org-file.md](org-file.md) | 0600 |
| `trust/`, `untrusted/` | the marks `dockingbird trust` and `trust --off` leave for a checkout | |
| `homes/NAME/` | another home on this computer, made by `--home NAME` | |
| `clones/` | a fleet worker's clones of the repositories its swarms work on | |
| `installs/RELEASE/` | a release installed for a home's program file to name | |
| `installs/current` | a link to the release this computer's fleet worker and admitter run; `dockingbird fleet update` moves it | |
| `programs/VERSION/` | one release of your `dockingbird` command in a folder of its own, never changed once installed; an install that follows `main` names it by its commit's first 12 characters; `dockingbird update` installs each release here, and `dockingbird clean` removes the folders that no home names and no running Dockingbird uses | |
| `programs/VERSION.lock` | the lock file beside each program folder | |
| `programs/current` | a link to the release your `dockingbird` command runs, which the `dockingbird` that uv put on your `PATH` links to; `dockingbird update` moves it with one rename | |
| `cache/`, `org-db/` | reserved; `clean --all` of this home keeps these folders and says so | |
| `state.json` | a cache no container can write; its absence means "not set up" | |
| `program` | one line: the path of the `dockingbird` script a start or update ran; `fleet scrape` and `fleet read-home` run it for this home | 0600 |
| `locks/`, `attach/` | the setup lock, the link locks and `hosts.lock`; one attach lock per agent shown in a terminal | |
| `docker-config/config.json` | the docker configuration every docker call of Dockingbird runs with; it holds no logins | 0600 |
| `results/AGENT/` | the files `dockingbird results` saved, one folder per agent | 0700, files 0600 |
| `connections/ID.json` | the catalogue `dockingbird connect` saved for one connection: each repo, branch and key path; a key's copy lives in a Docker volume, never here | 0700 |
| `configs/NAME/` | a config you added: its copy, `config.toml` and the files it names | 0700, files 0600 |
| `configs/index.json` | the list of the configs you added | 0600 |
| `vaults/` | the password stores a vault connection reads | 0700 |
| `logs/coordinator.log` | the log of the coordinator, the background process that Dockingbird turns off after 30 idle minutes | |
| `logs/agents/NAME-STAMP.log` | each agent's log, copied when it ends, with control characters escaped; an agent's `supervisor.log` moves to `supervisor.log.1` at half its bound, and this copy keeps the last part of both, so the lines that say how the agent ended survive; the supervisor log also holds `SETTLE_INHERITED` and `SETTLED` for each delivery a successor settles after an update, and `TASK_PACKET` for each task packet written | |
| `logs/dockingbird.log` | an unexpected error's details, redacted, and one line for each start of the home's coordinator: the command that started it, the start's form (run or start), the container, and the process and its parent, so the wake of an idle home traces to a command; rotated to `.1` | |
| `tmp/` | sync bundles in flight; empty between commands | |
| `bin/dockingbird-gui` | the GUI that `dockingbird ui` runs, version 0.1.20 in this release; `dockingbird ui --install` and, on a Mac, `dockingbird update` put it here and link it beside `dockingbird` on your `PATH`; the file is missing until one of them has run, and `dockingbird ui` then prints `GUI_MISSING`; see [the GUI](../../guides/gui.md) | |
| `bin/zeusfyi-license`, `bin/zeusfyi-license.fetch-failed` | the license client, downloaded once, and the time of its last failed download | 0700 |
| `license.json` | the license client's file: the license, this computer's id and label, the last check-in, the terms accepted; `clean --all` gives the seat back, then removes it | 0600 |
| `completion/dockingbird.SHELL` | the tab completion script `completion --install` wrote; `dockingbird update` keeps it current | 0700, files 0600 |
| `update/previous/`, `update/stage.json`, `update/last-switch.json` | a staged update: the copy of the version your agents run, what is staged, and the last switch; `clean --all` removes all three | 0700 |
| `toolchain/store.json` | the toolchain store's last listing, which `dockingbird env` and `clean` read | 0700, files 0600 |
| `toolchain/resolved/KEY.toml` | each checkout's last look at the versions its agents get; KEY is the SHA-256 of its real path | 0700, files 0600 |
| `fleet/container/` | the credential of a computer that joined a control plane; never in an agent's container, a log or a command line | |
| `apt-pool/` in `~/.local/share/dockingbird/` | the copy of the pinned Ubuntu package files the image installs, shared by every home of your user on that computer | |

## The small files you edit

| File | Keys | What it does |
|---|---|---|
| `config.toml` | `trust = "untrusted"` or `trust = "trusted"` | what a checkout with no mark is; no line means `"trusted"`; any other value is refused by every command that reads trust, and Dockingbird changes no byte of the file but its `last_build_seconds` line |
| `egress.toml` | `egress = "MODE"`, `allow = [...]` | `MODE` is `allowlist`, `models`, `none` or `full`; `allow` appears only with `allowlist` |
| `versions.toml` | `claude = "2.1.285"`, `codex = "0.162.1"` | a version Dockingbird downloads if it lacks it; `"latest"` or no line follows the latest release; `"stable"` is Claude Code's slower channel and works for Claude only; any other line, an unknown key or a file that is not plain TOML of yours stops the command and names the line |
| `instructions/claude.md`, `instructions/codex.md` | Markdown | Dockingbird copies a changed file into Docker the way it copies a key, read-only to agents, and never mounts it |

## Docker volumes, kept by Docker and named with a `-ID` suffix in a second installation

| Volume | What it holds |
|---|---|
| `dockingbird-state` | the database, the tokens, the agents' protected copies of each linked branch and every agent's own copy |
| `dockingbird-tools` | the program store: each downloaded version of Claude Code and Codex |
| `dockingbird-home-claude` | Claude's credentials store, its saved API key and your rules' copy |
| `dockingbird-home-codex` | Codex's credentials store, its saved API key and your rules' copy |
| `dockingbird-browser-sock-NAME` | one per agent whose config asks for a browser; removed once the agent's container is gone |

## In your checkout

| Path | What it holds |
|---|---|
| `.git/config`, `branch.BRANCH.dockingbird` | one line per linked branch; `git branch -m` moves it with the branch and `clean --all` removes it |
| `refs/remotes/dockingbird/BRANCH` | the head the agents' copy started from, then their commits as of your last sync; `clean --all` removes it |
| `.dockingbird/`, `.agents/`, `.claude/` | what `dockingbird init` writes; see [project-file.md](project-file.md) |

## A second home on the same computer

`--home NAME` before a command runs it in the home `homes/NAME` of the default home's folder.
The first command that claims it, such as `dockingbird --home lab egress full`, makes the folder, `homes/` above it at 0700, and its marker.

| Rule | Detail |
|---|---|
| NAME | lowercase letters, digits and `-`, a letter or a digit first |
| `--home default` | the default home itself, the same as no `--home` |
| position | before the command; after a command, `--home` belongs to `--host` and names a home of that host |
| refused, exit 2 | when `DOCKINGBIRD_HOME` is also set, when `--home` is given twice, and when NAME is not such a name |
| listing | `dockingbird homes` lists the home by that name from then on |
| seat | a second home on the same computer shares its computer's seat |
