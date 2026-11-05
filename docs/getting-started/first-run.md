---
title: First run
summary: Make a repository ready with init, start the first agent, sign it in, and learn what the product prints at each point.
audience: first-day
commands:
  - dockingbird init
  - dockingbird claude
  - dockingbird codex
  - dockingbird login claude --api-key
  - dockingbird login codex --api-key
  - dockingbird status
  - dockingbird stop
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# First run

Pick a git repository you work in, run `dockingbird init` there, then start `claude-1` and sign it in. Each step below shows the lines Dockingbird prints when it worked.

## Before you start

- Dockingbird is installed and activated. `dockingbird --version` prints a version, and `dockingbird license status` prints "Licensed: ..." or the trial line. See [install](install.md) and [activate](activate.md).
- Docker answers. `docker version` prints without an error.
- You are in a git repository with at least one commit on a branch. Agents start from your last commit, never from uncommitted edits.

## 1. Make the repository ready

```bash
cd your-repo
dockingbird init
```

`dockingbird init` runs anywhere inside a repository, and it writes these files.

- `.dockingbird/project.toml` holds the project's slug, the release that wrote it, its rules file, and each shipped role's harness, model and effort.
- `.dockingbird/rules.md` holds the lines every agent of the project gets after Dockingbird's own rules.
- `.dockingbird/swarms/example/` holds an example swarm.
- `.agents/skills/` holds this release's skills, and `.claude/skills` is a link to them.
- `.claude/agents/` holds the agent definitions.
- `.dockingbird/skills.lock` lists every installed file with its digest.

The slug is `--project SLUG`, else the name of the `origin` remote, else the folder's name.
Without an `origin` remote, `init` says so and names the project after the folder.

Done when `init` prints this and exits 0.

```text
Set up {project} for Dockingbird {release}: the project file, its rules,
an example swarm, the skills and their agents. Keep them in git:
git add .dockingbird .agents .claude && git commit
Then start an agent: dockingbird claude
```

Two more lines follow, about running the example swarm on the fleet once its hosts are filled in.

Commit the files now, so the agents' copy of the branch holds them.

```bash
git add .dockingbird .agents .claude && git commit
```

Without an org login on this computer, `init` also says the project is not in your organisation's store.
It still exits 0. `dockingbird init --no-register` skips that step.

A later run changes only what a new release changed.
It keeps an installed file you edited and names it, and `--force` replaces it.
It never rewrites `project.toml`, `rules.md` or a swarm.
`dockingbird init --check` writes nothing and exits 1 when an installed file is not the running release's.
It prints "{project} is not set up for Dockingbird {release}: init would change it." and "To change it: dockingbird init".
When nothing differs, `init` prints "{project} is set up for Dockingbird {release}: nothing to change."

## 2. Start the first agent

```bash
dockingbird claude
```

The command does five things in order.

1. It checks your branch. A symlink that leaves the repo, a submodule or a Git LFS file gets the branch refused in seconds. Each file is named, and nothing is set up.
2. It checks the platform and starts Docker Desktop if needed.
3. It builds the image on your computer. This takes about 5 minutes, downloads about 1 GB, and happens once.
4. It starts Dockingbird and copies your branch for the agents.
5. It downloads Claude Code's latest release the first time, then starts `claude-1` in its container.

On a terminal, each wait is one line redrawn in place.
In a pipe or a file, the build prints its heading at once, then a progress line at most once a minute.

```text
Setting up Dockingbird, first time only (about 5 min):
still setting up: step 12 of 41, 3 min so far
```

The copy and the start print these lines.

```text
Copying your-repo (main) for the agents ({size}) ... done ({elapsed})
Starting claude-1 on your-repo (main). Claude will show a sign-in link:
open it on this Mac, sign in, then paste the code here. Only this once.
```

On a terminal, the last line is "To leave it working, close this window."
Done when `AGENT_STARTING` or `SIGNIN_FIRST_TIME` has printed and `claude-1` shows its sign-in, or its prompt when a login already exists.

The agent works in its own copy of your branch, mounted at `/work/your-repo` in its container.
It never sees your uncommitted edits.

## 3. Sign in

Dockingbird reads the Claude Code or Codex login already on this computer, and keeps a copy.
Without a login, each tool signs in once, inside its container.

- Claude shows a link. Open it on this Mac, sign in, and paste the code back.
- Codex, started with `dockingbird codex`, shows a link and a one-time code. Open the link and enter the code. If device code login is off, turn it on in ChatGPT's security settings.
- With no Claude or ChatGPT account, quit the sign-in and run `dockingbird login claude --api-key` or `dockingbird login codex --api-key`.

Quitting the sign-in ends the agent and prints these lines.

```text
Claude isn't signed in yet. Run dockingbird claude again to sign in.
Or use an API key: dockingbird login claude --api-key
```

The agent's empty copy is removed, and the next start shows the sign-in again.
Done when the agent starts and `dockingbird status` shows `claude-1` working.
The first line of `status` reads "Dockingbird {version}, signed in to Claude and Codex".

## 4. What the repo's own settings do

Every checkout is trusted.
The repo's own hooks, settings and MCP servers run inside the agent, and Claude does not ask whether to trust `/work/your-repo`.
`dockingbird trust --off` marks a checkout untrusted, which keeps those settings off.
[Trust and repo settings](../guides/trust-and-repo-settings.md) says what then changes.

## 5. Leave, return and stop

Closing the window leaves `claude-1` working.
A bare `dockingbird claude` in that repo reconnects to the one Claude without a terminal. `dockingbird claude --as claude-1` reconnects to it by name.
When the tool ends, Dockingbird prints what was shared.

```text
claude-1 is done: 2 commits shared on main. Get them: dockingbird sync
```

Dockingbird turns itself off after 30 minutes with no agent, and the next command turns it back on.
`dockingbird stop` stops every agent and prints "Stopped {names}. Dockingbird is off until you next use it."
Nothing is lost.

[Choose a topology](choose-a-topology.md) covers a second computer or a team pool, and the [quickstart](../quickstart.md) continues with the daily loop.

## When it fails

- No `docker` command gives [`DOCKER_NOT_INSTALLED`](../troubleshooting.md#docker_not_installed). Install Docker Desktop, or Docker on Linux.
- A Docker that has not started in time gives [`DOCKER_NOT_RUNNING`](../troubleshooting.md#docker_not_running). Start it and run the command again.
- A missing buildx plugin stops the build with [`DOCKER_BUILDX_MISSING`](../troubleshooting.md#docker_buildx_missing).
- Files that Dockingbird did not make in the home folder give [`HOME_NOT_EMPTY`](../troubleshooting.md#home_not_empty). Unset `DOCKINGBIRD_HOME`, or point it at an empty folder.
- Ctrl-C during the build gives [`SETUP_INTERRUPTED`](../troubleshooting.md#setup_interrupted). Nothing changed, so run the command again.
- A build that fails gives [`IMAGE_BUILD_FAILED`](../troubleshooting.md#image_build_failed), names the step, and shows Docker's own output with `--verbose`.
- A command run outside a git repo gives [`NOT_A_GIT_REPO`](../troubleshooting.md#not_a_git_repo). `cd` into your project first.
- A symlink out of the repo, a submodule or a Git LFS file gives [`LINK_TREE_POLICY`](../troubleshooting.md#link_tree_policy). Fix the files named, commit, and run the command again.
- Running inside a submodule gives [`SUBMODULE_NOT_YET`](../troubleshooting.md#submodule_not_yet). `cd` into the main repo.
- `init` outside a git repo gives [`INIT_NOT_A_CHECKOUT`](../troubleshooting.md#init_not_a_checkout), and writes nothing.
- `init` inside the Dockingbird home gives [`INIT_INSIDE_HOME`](../troubleshooting.md#init_inside_home), and writes nothing.
- A tool without a sign-in gives [`SIGNIN_NEEDED`](../troubleshooting.md#signin_needed). Run `dockingbird claude` again, or use an API key.
