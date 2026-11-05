---
title: Harbor benchmark tasks
summary: Run a Harbor benchmark task's two baselines and one real trial with your own login, then list, read and clean its jobs.
audience: integrator
commands:
  - harbor baseline
  - harbor run
  - harbor jobs
  - harbor results
  - harbor clean
  - harbor version
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Harbor benchmark tasks

The place of this page in the customer docs is pending a decision.

A Harbor benchmark task is a folder with a `task.toml`, an `instruction.md`, an `environment/` folder and a `tests/test.sh`. Each branch of a task repository holds one task. The `dockingbird harbor` commands run a task on this computer with the Harbor commit that the repository's CI pins, which Dockingbird installs under its own folder the first time it is needed. A finished job leaves only its folder of results.

## Before you start

- Docker Desktop is running. `docker version` answers.
- You stand in the task's folder, or you name it with `-p DIR`. Without a `task.toml` there, the command stops with `HARBOR_NOT_A_TASK`.
- For a real trial with Claude Code, a saved token or key. Run `claude setup-token`, then `pbpaste | dockingbird login claude --oauth-token -`, or use `dockingbird login claude --api-key`. See [sign-in and API keys](sign-in-and-api-keys.md).

## 1. Run the two baselines

```bash
dockingbird harbor baseline
```

This runs an `oracle` job, whose `solution/solve.sh` must score 1, then a `nop` job, an agent that does nothing, which must score 0. `-k 3` runs each three times. The first run installs Harbor at the pinned commit, with one live line for the step. Done when the line prints.

```text
Both baselines pass: oracle scored 1 and nop scored 0 on every attempt.
```

Message id `HARBOR_BASELINE_OK`. A failure names each failing trial and the last lines its verifier printed (`HARBOR_BASELINE_FAILED`). Fix the task and run it again.

## 2. Run one real trial

```bash
dockingbird harbor run -a claude-code
```

This runs one trial with Claude Code and your own login. Dockingbird lends the credential to the task's container for the whole trial: a saved token or key first, else your computer's own login when its expiry covers the trial. Any other word goes to Harbor's own `run` as Harbor reads it, such as `-k 3` or `--timeout-multiplier 2`. `--keep-images` keeps the images a job built, for a faster next run. Run `claude-code` only on a task whose `environment/` you trust: the task's image owns its container and can read the credential. Done when the job ends.

```text
Job {job} ran {count} trials:
{trials}
Results: {folder}
```

Message id `HARBOR_JOB_DONE`. With no saved credential and no usable login, nothing runs: `No Claude sign-in or saved key is stored, so a claude-code trial can't run.` (`HARBOR_NO_SIGNIN`).

## 3. List, read and clean jobs

```bash
dockingbird harbor jobs
dockingbird harbor results JOB
dockingbird harbor clean
dockingbird harbor version
```

`jobs` lists what ran, newest first, in `DOCKINGBIRD_HOME/harbor/jobs/`. `results JOB` shows each trial's reward.

```text
Job {job} ({state}), {count} trials:
{trials}
Folder: {folder}
```

Message id `HARBOR_JOB_RESULTS`. A job is `running` while its command runs, `done` once Harbor wrote its result, else `stopped`. `clean` asks once, then removes the job folders and the leftovers of earlier jobs.

```text
These Harbor jobs go:
{jobs}
Remove them? [y/N]
```

Message id `HARBOR_CLEAN_QUESTION`. `--yes` asks nothing, and `--all` removes Harbor's install too, which the next run installs again. `version` says whether the pinned commit is installed (`HARBOR_VERSION`). When a job ends, its containers, networks, volumes and the images it built are removed, unless `--keep-images`. Docker's build cache stays; `docker builder prune` removes it.

`dockingbird harbor check`, which would hand a bundle to Harbor's `check` so a model reads it at your cost, is not yet available and says so.

## When it fails

- Run `harbor run` or `harbor baseline` in a folder with no `task.toml` and you get [`HARBOR_NOT_A_TASK`](../troubleshooting.md#harbor_not_a_task). Change folder, or pass `-p DIR`.
- A baseline trial that scores other than what its job wants, or hits an error, gives [`HARBOR_BASELINE_FAILED`](../troubleshooting.md#harbor_baseline_failed) with the last lines its verifier printed. Fix the task, then run it again.
- A `claude-code` trial needs a credential. With no saved token or key and no usable login, nothing runs, and [`HARBOR_NO_SIGNIN`](../troubleshooting.md#harbor_no_signin) says how to save one.
- When your computer's login would expire before the trial ends, [`HARBOR_SIGNIN_TOO_SHORT`](../troubleshooting.md#harbor_signin_too_short) shows what it has and what the trial needs. A token from `claude setup-token` lasts much longer.
- A task with several steps, or one that sets Windows, gives [`HARBOR_TASK_UNSUPPORTED`](../troubleshooting.md#harbor_task_unsupported). Run that task with Harbor itself.
- An option that would mount a folder of this computer into the task is refused with [`HARBOR_OPTION_REFUSED`](../troubleshooting.md#harbor_option_refused).
- On a computer where no job has run, `harbor jobs` prints [`HARBOR_NO_JOBS`](../troubleshooting.md#harbor_no_jobs).
