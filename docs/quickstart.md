---
title: Quickstart
summary: The one-page path from a fresh computer to a first agent, a daily loop and a clean uninstall.
audience: first-day
commands:
  - dockingbird --version
  - dockingbird completion --install
  - dockingbird license activate
  - dockingbird init
  - dockingbird claude
  - dockingbird codex
  - dockingbird login claude --api-key
  - dockingbird login codex --api-key
  - dockingbird status
  - dockingbird sync
  - dockingbird stop
  - dockingbird update
  - dockingbird clean
  - dockingbird start
  - dockingbird wait
  - dockingbird inbox
  - dockingbird read
  - dockingbird search
  - dockingbird send
  - dockingbird results
  - dockingbird clean --all
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../llms.txt).

# Dockingbird quickstart

This page takes you from a fresh computer to a running agent, then through the daily loop and a clean uninstall.
Each step ends with the line Dockingbird prints when it worked, and each step links to its own page for detail.

Dockingbird runs Claude Code and Codex side by side on your git repo, each in its own container.
They never overwrite each other or touch your Mac, and their work comes back to you as commits.

## Before you start

You need all five of these. [Prerequisites](getting-started/prerequisites.md) gives the check for each.

- An Apple silicon Mac or arm64 Linux. Intel Macs, x86 Linux and Windows are not supported.
- Docker Desktop, which includes the buildx plugin. Docker Engine on Linux needs the `docker-buildx-plugin` package.
- [uv](https://docs.astral.sh/uv/). On a Mac, `brew install uv` installs it.
- git at `/usr/bin/git`.
- A license key from your purchase email, or no key and a trial.

## 1. Install

Copy the key from your purchase email, then run this line on a Mac.
It hands the key to uv as the index's password, so the key never reaches your shell history or a command line.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
dockingbird --version
dockingbird completion --install
```

On Linux, `read -rs UV_INDEX_ZEUSFYI_PASSWORD` reads the key without echo, and `unset` clears it afterwards.
[Install](getting-started/install.md) shows the whole Linux sequence.

Never run a bare `uv tool install dockingbird`. That name on PyPI is not this product, so the line above must carry `--index`.

Done when `dockingbird --version` prints a line that starts with `dockingbird` and a version.
`dockingbird completion --install` then prints "Open a new terminal." for tab completion.
If `dockingbird` is not found, run `uv tool update-shell` and open a new terminal.

## 2. Activate

```bash
dockingbird license activate
```

Dockingbird asks for the key and does not show it. `pbpaste | dockingbird license activate` also works.
A key typed on the command line is refused with exit 2.
No key? `dockingbird license trial` starts this computer's trial, but a trial cannot install from the index or update.

One seat is one person, who may link up to three computers.
[Activate](getting-started/activate.md) explains seats, the trial and the refusals.

Done when Dockingbird prints these two lines.

```text
This computer is activated: {plan}, {seats}, {term}.
You use Dockingbird under its terms: {link}
```

If every computer of the license is linked, the message is `LICENSE_SEATS_FULL` and it names the command that frees one.

## 3. Make a repository ready

```bash
cd your-repo
dockingbird init
git add .dockingbird .agents .claude && git commit
```

`dockingbird init` writes `.dockingbird/project.toml`, the rules file, an example swarm, and the skills and agent definitions of this release.
Agents start from your last commit, so commit these files before the first start.
Without an org login, `init` says the project is not in an organisation's store and still exits 0.
Add `--no-register` to skip that line.

Done when the first line reads "Set up {project} for Dockingbird {release}: the project file, its rules,". The next lines tell you to keep the files in git.
Run in a folder that is no git repo, it stops with `INIT_NOT_A_CHECKOUT`.
[First run](getting-started/first-run.md) lists what `init` writes.

## 4. First run

```bash
dockingbird claude
```

The first start checks your branch, builds the image, starts Dockingbird and copies the branch for the agents.
The build takes about 5 minutes and downloads about 1 GB, once.
The first start of each tool also fetches that tool's latest release.
Dockingbird refuses a branch holding a symlink that leaves the repo, a submodule or a Git LFS file. It does so in seconds, names each file, and sets nothing up.
Then it starts `claude-1`.

Claude shows a sign-in link once. Open it on this Mac, sign in, and paste the code back.
Codex works the same way with `dockingbird codex`: open its link and enter the one-time code.
With no Claude or ChatGPT account, quit the sign-in. Then run `dockingbird login claude --api-key` or `dockingbird login codex --api-key`.

The repo's own settings, hooks and MCP servers load in the agent, and Claude does not ask whether to trust `/work/your-repo`.
For a repo you do not control, run `dockingbird trust --off` in it.
To leave the agent working, close the window. A bare `dockingbird claude` in that repo reconnects to it.
Dockingbird turns itself off after 30 minutes with no agent, and the next command turns it back on.

Done when the start prints these lines and Claude opens its sign-in.

```text
Copying your-repo (main) for the agents ({size}) ... done ({elapsed})
Starting claude-1 on your-repo (main). Claude will show a sign-in link:
open it on this Mac, sign in, then paste the code here. Only this once.
```

Run as many agents as you like, each in its own terminal, in as many repos as you like.

## 5. Every day

```bash
dockingbird status
dockingbird sync
dockingbird stop
```

- `status` shows who is working on what and what needs you. Its first line reads "Dockingbird {version}, signed in to Claude and Codex".
- `sync` takes the agents' commits and sends yours. It prints "Updated your {branch} to {head}." for commits taken and "up to date." when nothing moved.
- `stop` turns everything off and prints "Dockingbird is off until you next use it." Nothing is lost.
- Agents start from your last commit, never from uncommitted edits, and their work reaches you only through `dockingbird sync`.
- `sync` never rewrites history. It keeps your uncommitted edits, and when both sides have new commits it offers to merge.
- To undo an agent's commit, make a commit of your own with `git revert COMMIT`, then run `dockingbird sync`.
- A one-shot works too: `dockingbird claude -p "Summarize the open TODOs"` prints only the answer.
- `dockingbird login claude` signs in again, `dockingbird update` gets the latest versions, and `dockingbird clean` frees disk space.
- A second computer joins with `dockingbird fleet hosts set NAME --ssh DEST`, or with `--gcloud VM --zone ZONE --project PROJECT`. [Choose a topology](getting-started/choose-a-topology.md) compares the options.
- `dockingbird ui --install` installs the GUI, and `dockingbird ui` shows every agent in one window with your inbox beside it. See [the GUI](guides/gui.md).

## 6. Delegate

```bash
dockingbird start "Fix the flaky test"
dockingbird wait claude-1
dockingbird inbox
dockingbird read 1
dockingbird search "closed issues"
dockingbird send claude-1 "The new one"
dockingbird results claude-1
dockingbird stop claude-1
```

`start` hands an agent a task without a terminal. `wait` shows its next message as it comes.
`inbox` lists what waits for you. `read` opens one message and the files it names. `search` finds a message by its words.
`send` answers a question or sends a new task. `results` saves the files it attached. `stop claude-1` stops it, and its messages and results stay.
A question the agent asks also leads `dockingbird status` until you answer it.

Done when `start` prints "claude-1 started on your-repo (main)." and a thread line that names `dockingbird wait claude-1`.
`dockingbird inbox` prints "Nothing is waiting in your inbox." when no message waits.
[Delegating tasks](guides/delegating-tasks.md) has the full loop.

## 7. Uninstall

```bash
dockingbird clean --all
uv tool uninstall dockingbird
```

`clean --all` lists what it removes, then asks you to type `delete`. It gives this computer's seat back first.
Uninstalling first would leave Dockingbird's containers, volumes and image behind.
`clean --all` keeps one empty folder, `logs`, in the Dockingbird home, so a later start works while Docker Desktop still shares it.
Docker keeps the build cache of Dockingbird's image, shared with every other project's, and `docker builder prune` frees all of it.

Done when `clean --all` prints these lines.

```text
Removed everything Dockingbird made ({freed}). Your code is untouched.
To remove the command too: uv tool uninstall dockingbird
```

## When it fails

- [`DOCKER_NOT_INSTALLED`](troubleshooting.md#docker_not_installed) appears when no `docker` command exists. Install Docker Desktop, or Docker on Linux.
- [`HOME_NOT_EMPTY`](troubleshooting.md#home_not_empty) appears when the folder Dockingbird would use holds files it did not make. Unset `DOCKINGBIRD_HOME` or point it at an empty folder.
- [`COMPLETION_ALREADY`](troubleshooting.md#completion_already) appears when you install completion a second time. Nothing is wrong.
- [`LICENSE_KEY_IN_ARGV`](troubleshooting.md#license_key_in_argv) appears when you type the key on the command line. Nothing ran, so run `dockingbird license activate` and paste the key.
- [`LICENSE_TRIAL_USED`](troubleshooting.md#license_trial_used) appears when this computer already had its trial. Activate it with a key.
- [`INIT_NOT_A_CHECKOUT`](troubleshooting.md#init_not_a_checkout) appears when `init` runs outside a git repo. Run it in your repo.
- [`INIT_INSIDE_HOME`](troubleshooting.md#init_inside_home) appears when `init` runs inside the Dockingbird home. Run it in your repo.
- [`SIGNIN_NEEDED`](troubleshooting.md#signin_needed) appears when the tool has no sign-in. Run `dockingbird claude` again, or use an API key.

Every command explains itself with `dockingbird -h`.
All messages are in [troubleshooting](troubleshooting.md), and the [operator guide](operator-guide.md) has the rest.
