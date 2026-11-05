---
title: Toolchains and dependencies
summary: See, install, lock and change the language versions agents get from your repo's mise.toml or .tool-versions.
audience: daily
commands:
  - env
  - env install
  - env lock
  - env use
  - claude --no-toolchain
  - claude --no-deps
  - clean
---

# Toolchains and dependencies

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Each agent runs the language versions your repo already names, where production reads them. This page shows which versions agents get, installs them ahead of a start, locks them for every computer, and changes one.

Dockingbird reads none of the version files itself. [mise](https://mise.jdx.dev) reads them in a container of Dockingbird's own and installs each version once per Mac, into a store every agent mounts read-only. The files it reads are `mise.toml`, `.tool-versions`, and the version files that `mise.toml` enables under `[settings]`. For example, `idiomatic_version_file_enable_tools = ["node", "python"]` makes mise read `.nvmrc` and `.python-version`. A `mise.lock` decides over them, as mise decides.

## Before you start

- You stand in a git repo. Outside one, `dockingbird env` says so and exits 1.
- Docker runs. With Docker off, `env` shows the heading and the store's line from its last record, and says the versions need Dockingbird running.
- To change a version, you can commit `mise.toml` and `mise.lock` in the repo.

## Steps

1. Read what agents get. The table lists each tool the repo's files name, with the request and its file, beside the version agents get. A version is marked "(locked)" when `mise.lock` names it, and "(not installed yet)" when no start has installed it. Below come the image's Python, Node and Go, where nothing names them, and the count of toolchains this Mac holds. The command runs in a container with your checkout mounted read-only, so it writes nothing there.

   ```bash
   dockingbird env
   ```

   The step is done when the command prints a table like this one.

   ```text
   myapp (main)   repo wants         agents get
     Python       3.12 (mise.toml)   3.12.7 (locked)
     Node         20 (.nvmrc)        20.18.1
     Go           nothing named      1.27.2 (the image's)
   Dependencies: none preinstalled (no lock file).
   Downloaded: 2 toolchains. Unused ones go with: dockingbird clean
   Change one: dockingbird env use TOOL VERSION
   ```

   With `--json`, each line is one envelope, and a tool's row adds `tool_word`, `locked` and `installed`.

2. Install those versions now, so the next start waits for none. This writes nothing in your checkout.

   ```bash
   dockingbird env install
   ```

   The step is done when the command prints this line, or when the versions were installed already.

   ```text
   Lock them so every machine gets the same: dockingbird env lock
   ```

3. Lock the versions. Each exact version goes into `mise.toml` and is locked in `mise.lock`. Once you commit both, every Mac and every agent gets the same versions.

   ```bash
   dockingbird env lock
   git add mise.toml mise.lock
   ```

   The step is done when the first command prints these lines.

   ```text
   Locked Python and Node in mise.toml and mise.lock. Commit them so every machine
   gets the same: git add mise.toml mise.lock
   ```

4. Change one version. The tool is python, node, go, java, rust, ruby, bun, deno, zig, pnpm, yarn or npm. The version is a number such as 22, 3.12 or 1.82.0. Go also takes prefix:1.20, and Java takes temurin-21, or 21 for mise's default vendor. The words lts and latest are refused. Any other tool that mise knows goes into `mise.toml` by hand.

   ```bash
   dockingbird env use node 22
   ```

   The command writes the version into `mise.toml`, creating the file when the repo has none, and installs it. The step is done when it prints this line. A line for each running agent follows, because those agents keep their old version until you restart them.

   ```text
   Wrote mise.toml: node = "22" (was .nvmrc: 20; mise.toml wins now). Agents started from now get Node 22.11.0.
   ```

5. Start with the image's versions for one start only. Neither flag is remembered. The first skips the repo's versions, and the second keeps the toolchain and skips the dependency install.

   ```bash
   dockingbird claude --no-toolchain
   dockingbird claude --no-deps
   ```

   The first line of a start says what the agent gets. Both flags also work on `codex` and `start`.

   ```text
   Toolchain for myapp: Python 3.12.7 (mise.toml) and Node 20.18.1 (.nvmrc).
   Toolchain for myapp: nothing named; agents get the image's versions.
   ```

## What a start does about versions

A start installs a version that is not in the store yet, with a live line, before anything else starts. A second agent on the same repo prints the first line alone. An install that fails stops the start before anything is made, with mise's last lines. Ctrl-C during an install ends the start with exit 130 and leaves the install going, so the next start uses it. A running agent keeps the versions it started with, and `dockingbird status` says when its repo now asks for others.

```text
Installing Node 20.18.1 ... {elapsed}: <mise's latest line>
Installed Node 20.18.1 ({elapsed}).
```

## Dependencies

Before its tool starts, an agent whose repo names a toolchain installs the repo's dependencies in its own copy, from the lock files at the repo's top, with the toolchain's own package managers. A repo that names no toolchain gets the image's versions and installs nothing.

| Lock file | Command the agent runs |
|---|---|
| `uv.lock` | `uv sync --locked` |
| `package-lock.json` | `npm ci` |
| `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| `yarn.lock` | `yarn install --immutable` (Yarn 2 and later) or `yarn install --frozen-lockfile` (Yarn 1) |
| `go.sum` | `go mod download` |
| `Cargo.lock` | `cargo fetch --locked` |
| `Gemfile.lock` | `BUNDLE_FROZEN=true bundle install` |

A lock file that does not match its manifest fails the install, as it would in production. A Maven or Gradle build, and a `requirements.txt` without a lock file, get nothing. The agent prints `Installing myapp's dependencies: uv sync --locked (uv.lock)`, the command's own lines, then `Dependencies installed ({elapsed}).` On the bus these lines go to its log, and `dockingbird status` shows "preparing: installing dependencies".

npm's, uv's and Go's downloads go to a cache of the agent's own, the Docker volume `dockingbird-cache-<agent>` at `/dockingbird/cache`. A restart of the same agent keeps it. `dockingbird clean` removes an agent's cache with its kept copy, `clean NAME` with the agent, and `clean --all` removes them all. `clean` also removes the versions no running agent and no repo's last look names, and clears mise's download cache.

An agent whose egress is `none` or `models` reaches no registry, so it runs each command's offline form, such as `uv sync --locked --offline`, from what is cached. See [egress-and-network.md](egress-and-network.md).

## Trust

A repo's mise config can do more than name versions. Its `[env]` sets variables and its `[settings]` change how mise installs. Those load only in a checkout you trust, which is every checkout unless you ran `dockingbird trust --off` or made untrusted the default. In an untrusted checkout, a mise config that needs trust stops the start and `env`, with mise's own words. A `mise.toml` of plain versions, a `.tool-versions` and the version files need no trust. An untrusted agent gets its toolchain alone and prints `Dependencies: skipped (untrusted checkout; dockingbird trust allows them).` The page [trust-and-repo-settings.md](trust-and-repo-settings.md) covers trust.

A config's `[env]` arrives through mise before the repo's own, so the repo's `mise.toml` entry of a name wins. A config's `mise_env`, such as `"ci"`, makes mise read `mise.ci.toml` over `mise.toml`, for the install and for the agent's environment. See [your-own-commands.md](your-own-commands.md).

## When it fails

- [`TOOLCHAIN_INSTALL_FAILED`](../troubleshooting.md#toolchain_install_failed) shows mise's last lines when a version does not exist, a download failed or a checksum did not match. No agent started. Fix the file that names the version, or start with `--no-toolchain`.
- [`TOOLCHAIN_LOOK_FAILED`](../troubleshooting.md#toolchain_look_failed) means mise could not read the repo's versions. An invalid `mise.toml` is one cause, and an untrusted checkout whose mise config needs trust is the other.
- [`TOOLCHAIN_LOOK_UNAVAILABLE`](../troubleshooting.md#toolchain_look_unavailable) appears when Docker is off, so `env` cannot read the versions agents get. The exit status is 0.
- [`TOOLCHAIN_LOCK_INVALID`](../troubleshooting.md#toolchain_lock_invalid) says `mise.lock` is unreadable and ignored. `dockingbird env lock` writes it again.
- [`TOOLCHAIN_RUNNING_DIFFERS`](../troubleshooting.md#toolchain_running_differs) appears in `status` for an agent that runs an older version than the repo now asks for. Stop it and start it again under its name.
- [`TOOLCHAIN_INTERRUPTED`](../troubleshooting.md#toolchain_interrupted) follows a Ctrl-C during an install. The install carries on and no agent started.
- [`ENV_NOT_A_REPO`](../troubleshooting.md#env_not_a_repo) means you ran `env` outside a git repo.
- [`ENV_USE_NOT_A_NUMBER`](../troubleshooting.md#env_use_not_a_number) refuses `lts` and `latest` and names an example number for the tool.
- [`ENV_USE_UNKNOWN_TOOL`](../troubleshooting.md#env_use_unknown_tool) lists the twelve tools `env use` takes.
- [`ENV_USE_FAILED`](../troubleshooting.md#env_use_failed) means mise could not install that version, offline or because it does not exist.
- [`DEPS_FAILED`](../troubleshooting.md#deps_failed) ended the agent because the install command failed. Fix what the last lines say, or pick the agent up with `--no-deps`.
- [`DEPS_OFFLINE_REFUSED`](../troubleshooting.md#deps_offline_refused) ended the agent because its egress reaches no registry and the packages are not cached. Pick it up with `--egress full`, or with `--no-deps`.
