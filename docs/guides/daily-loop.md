---
title: The daily loop
summary: Start an agent at your terminal, read status, take its commits with sync, stop, and recover when a laptop sleeps, a terminal closes or an agent ends with work not shared.
audience: daily
commands:
  - claude
  - codex
  - claude --as NAME
  - status
  - sync
  - sync --accept
  - sync --let-go
  - stop
  - clean NAME
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# The daily loop

This page walks through one normal day: start an agent at your terminal, read what it is doing, take its commits, and stop. It also says what resumes by itself and what needs a command when a laptop sleeps, a terminal closes or an agent ends with work not shared.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version. The first start is in [first run](../getting-started/first-run.md).
- Docker Desktop is running. `docker version` answers.
- You stand in a git repository with at least one commit. `git log -1` prints it. Agents start from your last commit and never see uncommitted edits.

## 1. Start an agent

```bash
cd myapp
dockingbird claude
```

Use `dockingbird codex` for Codex. The first agent is `claude-1`, and the numbers climb across the whole installation, so the next one is `claude-2`. `--as NAME` picks a name made of lowercase letters, digits and `-`. `--new` always starts a new agent instead of reconnecting to one.

The agent works in its own copy of your branch, in its own container. The last start line is the done line.

```text
To leave it working, close this window.
```

Message id `AGENT_LEAVE_HINT`. The agent keeps working when you close the window.

## 2. Read status

```bash
dockingbird status
```

`status` only looks. It starts nothing and waits at most 10 seconds for Docker. Its first line names the version and the sign-ins.

```text
Dockingbird 0.11.1, signed in to Claude and Codex
```

Each repo and branch lists its agents, how long each has worked, how far behind you are and the step that fixes it. An agent that asks you something shows "asks you" with the count; answer it as [delegating tasks](delegating-tasks.md) says. An agent that reported on its task shows idle until you run `dockingbird stop NAME`. The last line is the done line.

```text
Nothing needs your attention.
```

Anything under "Needs your attention" comes with its own command.

## 3. Take the agents' commits

```bash
dockingbird sync
```

`sync` works on the branch you are on, in the checkout you run it in. Agents' commits arrive on the ref `dockingbird/<branch>`. The model is on [the sync model](../concepts/sync-model.md). The result is one of these lines.

```text
myapp (main): up to date.
myapp (main): sent your 1 commit to the agents. They'll build on it.
Updated your main to 5555555. Review them: git log -p 1111111..5555555
```

When you are behind, `sync` fast-forwards your branch and names each commit with the agent that shared it. Message ids `SYNC_UP_TO_DATE`, `SYNC_SENT` and `SYNC_UPDATED`. Run `git log -p` as the last line says before you build or run anything.

### You and the agents both have new commits

On a terminal, `sync` shows the commits and asks.

```text
myapp (main): you and the agents both have new commits.
Merge theirs into yours now? [Y/n]
```

Yes runs a git merge with sync's protections, then sends the merge to the agents. The done line follows.

```text
Merged, and sent the merge to the agents. Review: git log -p 1111111..main
```

A conflict stops the merge with `Fix them, commit, then run this again.` (`SYNC_CONFLICTS`). Finish the merge, commit, and run `dockingbird sync` again. Starting an agent on such a branch offers the same merge first (`START_MERGE_OFFER`). Without a terminal, `sync` prints the look-first command and `git merge dockingbird/main`.

### Edits you have not committed

Your open edits stay as they are. When the agents changed a file you are editing, `sync` merges nothing and names the files (`SYNC_OVERLAP`). Commit or stash them, then run it again.

### Turning a commit down

Undo an agent's commit with a commit of your own, then sync.

```bash
git revert COMMIT
dockingbird sync
```

Resetting or deleting your branch does not remove it. The agents' copy keeps the commit, and the next sync brings it back.

### A paused branch

When the agents' copy of a branch changed outside Dockingbird, sharing pauses and nothing is lost (`SYNC_PAUSED`).

```bash
dockingbird status --verbose
dockingbird sync --accept 5555555
```

The first command shows what changed. The second goes on from the commit `sync` named.

### A branch made again under its old name

If you deleted a branch and made it again, and you do not want the agents' commits on it, `dockingbird sync --let-go` asks once and names what goes.

```text
Let go of 2 commits the agents made on feature/x and make yours the branch? [y/N]
```

Answer y and yours is the branch (`SYNC_LET_GO_DONE`). The agents' copies keep their work, but a copy built on the commits let go cannot share until it syncs onto yours.

## 4. Stop

```bash
dockingbird stop
```

With agents working, `stop` asks first. `--yes` skips the question, and without a terminal it refuses without `--yes`.

```text
Stop claude-1 (working) and turn Dockingbird off?
Its work is kept. [y/N]
```

Done when the command prints this line. Nothing is lost.

```text
Stopped claude-1. Dockingbird is off until you next use it.
```

`dockingbird stop claude-1` stops one agent. Its work is kept, and `dockingbird claude --as claude-1` picks it up. Dockingbird also turns itself off after 30 minutes with no agent, and the next command turns it back on.

## Reconnect, or start a new agent

Close the terminal and the agent keeps working (`AGENT_KEEPS_WORKING`).

```text
claude-1 keeps working without a terminal: dockingbird claude --as claude-1
```

A bare `dockingbird claude` in that repo reconnects to the one Claude that has no terminal, and lists them when there are two. `dockingbird claude --as claude-1` reconnects to that agent from any branch or checkout. When another terminal shows it, this terminal takes it over, and the other one says `claude-1 is now shown in another terminal. It keeps working.` `dockingbird claude --new` starts a fresh agent. Arguments for the tool and `--egress` never reconnect, because an agent's egress is fixed at its start.

## When the laptop sleeps or the network drops

| Situation | What resumes by itself | What needs a command |
|---|---|---|
| A closed terminal | The agent keeps working | `dockingbird claude --as NAME` to show its screen again |
| Docker Desktop waking from Resource Saver | The command waits and prints `Waking Docker ...` (`DOCKER_WAKING`) | Past 2 minutes it ends with "Docker is answering slowly." or "Docker isn't running."; restart Docker Desktop and run the command again |
| `status` while Docker is slow | It prints what it last knew (`STATUS_DOCKER_SLOW`) | Run it again in a moment |
| A restart of Docker or Dockingbird | Nothing: the agent is stopped and its copy may hold work (`STATUS_STOPPED_BY_RESTART`) | The pick-up command on its status row |
| The laptop sleeps | Not documented yet | Not documented yet |
| The network drops during an agent's model call | Not documented yet | Not documented yet |
| A host unreachable over ssh | Not documented yet | `fleet agents` prints `Couldn't read lab: ...` (`FLEET_HOST_NOT_READ`); fix the route, see [hosts](hosts.md) |

No behaviour is documented yet for a sleeping laptop, for a network drop during a model call, or for the recovery of an unreachable host. The rows say so instead of guessing.

## An agent that ended with work not shared, or crashed

Agents say how they ended. A tool that exits cleanly with commits shared prints the first line. A tool that ended with a copy kept prints one of the next two.

```text
claude-1 is done: 2 commits shared on main. Get them: dockingbird sync
claude-1 stopped, with 2 commits not shared yet. Pick it up:
dockingbird claude --as claude-1
```

A crash, most likely the out-of-memory killer, keeps the copy every time and says so (`AGENT_CRASHED`).

```text
claude-1 crashed 3 min ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
dockingbird claude --as claude-1
Log: logs/agents/claude-1-<stamp>.log
```

The word "may" means Dockingbird could not count the copy's own commits, usually because the branch moved on since the copy started. `dockingbird status` lists every kept copy under "Needs your attention" with its pick-up command, from where you stand: `git switch feature/r7, then dockingbird claude --as keep7` when the copy is on another branch.

The kept copy lives in the Docker volume `dockingbird-state`, never on your Mac. `dockingbird status claude-1` names its commits and files not shared, at most 5 of each, and where the log is.

Pick it up with `dockingbird claude --as claude-1`. The tool resumes its conversation. When nothing of the conversation could be kept, one line says "The earlier conversation couldn't be restored, so this is a new one." Its copy's commits then reach you through `dockingbird sync`.

### What clean asks

`dockingbird clean` removes an empty copy at once and asks about every other one. The default answer is no.

```text
claude-1 left 2 commits not shared yet. Remove its copy anyway? [y/N]
```

Message id `CLEAN_ASK_UNSHARED`. Answer y only when you have taken the work or do not want it. `dockingbird clean claude-1` deletes one stopped agent whole, with its copy, results and history, after the same question. See [clean and uninstall](clean-and-uninstall.md).

## When it fails

Sixteen messages can show up in a normal day. Most only inform, and each one names its own next command.

- A sync that took the agents' commits ends with [`SYNC_UPDATED`](../troubleshooting.md#sync_updated) and the `git log -p` line to review them.
- When you committed on the branch too, [`SYNC_BOTH_MOVED`](../troubleshooting.md#sync_both_moved) asks whether to merge. Starting an agent on such a branch shows [`START_MERGE_OFFER`](../troubleshooting.md#start_merge_offer) with the same question.
- A merge that hits conflicts stops with [`SYNC_CONFLICTS`](../troubleshooting.md#sync_conflicts). Fix the files, commit, and run `dockingbird sync` again.
- An agent edited a file that you are editing and have not committed: [`SYNC_OVERLAP`](../troubleshooting.md#sync_overlap) names it. Commit or stash it first.
- Someone changed the agents' copy of a branch outside Dockingbird, so [`SYNC_PAUSED`](../troubleshooting.md#sync_paused) pauses sharing. `dockingbird sync --accept COMMIT` goes on from there.
- Without a terminal, `dockingbird stop` prints [`STOP_REFUSED_NO_TTY`](../troubleshooting.md#stop_refused_no_tty). Add `--yes`.
- Docker Desktop asleep gives [`DOCKER_WAKING`](../troubleshooting.md#docker_waking) while the command waits, and `status` shows [`STATUS_DOCKER_SLOW`](../troubleshooting.md#status_docker_slow) when Docker is too slow to answer.
- Closing a terminal leaves [`AGENT_KEEPS_WORKING`](../troubleshooting.md#agent_keeps_working) on screen with the command that reconnects.
- A restart of Docker or Dockingbird shows [`STATUS_STOPPED_BY_RESTART`](../troubleshooting.md#status_stopped_by_restart) on the agent's row, with its pick-up command.
- An agent that ended with a copy kept prints [`AGENT_STOPPED_NOT_SHARED`](../troubleshooting.md#agent_stopped_not_shared), and a killed one prints [`AGENT_CRASHED`](../troubleshooting.md#agent_crashed). Both give the pick-up command.
- `dockingbird clean` asks [`CLEAN_ASK_UNSHARED`](../troubleshooting.md#clean_ask_unshared) before it deletes a copy that holds commits. The default answer is no.
- `dockingbird status NAME` can print [`STATUS_KEPT_WORKTREE`](../troubleshooting.md#status_kept_worktree) when the kept copy has a worktree with commits on no branch. A start under that name then gets a fresh copy.
- A host that ssh cannot reach shows up as [`FLEET_HOST_NOT_READ`](../troubleshooting.md#fleet_host_not_read) in `dockingbird fleet agents`.
