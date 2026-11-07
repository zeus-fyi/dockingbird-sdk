---
title: Your own commands
summary: Add a command of your own, such as dockingbird review, from a TOML config in your repo or one shared by every repo.
audience: daily
commands:
  - config add
  - config list
  - config remove
  - start --command
---

# Your own commands

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

A config is a small TOML file that adds a command to Dockingbird, such as `dockingbird review "Check the login flow"`. Each command runs Claude Code or Codex with the settings you chose filled in. This page writes one, runs it, makes it the default, shares it across repos and removes it. Every key is in [the app config reference](../reference/files/app-config.md).

A command is a preset. `dockingbird review "Check the login flow"` is `dockingbird start --command review "Check the login flow"`, and the agent it starts is a delegated agent, named `review-1`, `review-2` and so on. Dockingbird ships no such command. The names `review`, `triage` and `notes` here are examples, and none exists until a config of yours adds it.

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- You stand in a git checkout when the config lives in the repo. A config with `workspace = "scratch"` needs none.
- `dockingbird config list` runs. A home with no config prints the first line below.

```text
No configs yet. Put one in this repo's .dockingbird/ folder,
or add one: dockingbird config add PATH
```

## Steps

1. Write the config in the repo's `.dockingbird/` folder. Each `*.toml` file there is a config, and its commands exist in that checkout with nothing to register. Dockingbird reads the file at every start, so an edit counts from the next one. Every key is optional.

   ```toml
   # .dockingbird/review.toml
   command = "review"
   summary = "Review this branch and list what to fix"
   skill = "skills/review.md"
   instructions = "review-role.md"
   tools = "bus"
   workspace = "repo"
   mode = "bus"
   context = "fresh"
   ```

   The skill file becomes the agent's first turn on the bus, with the task put where `$TASK` stands. The instructions file is role text that follows Dockingbird's own rules. Both paths start from the config's folder.

   ```markdown
   Review the changes on this branch for this task:

   $TASK

   List what to fix, file by file, in a Markdown file you attach, then mark the task done.
   ```

2. Check that Dockingbird sees it. The list shows this repo's configs first. Each row gives the config's source, commands, workspace, mode and connections, and the start of its digest, with the summary under it.

   ```bash
   dockingbird config list
   ```

   The step is done when a row names review with the source "this repo". Below the rows, the list names each config, key or command that cannot run, with its file and key and never a value. The top help screen lists the command after the everyday ones, with its summary and file.

3. Run the command. It takes every option of `start` except `--command`, among them `--terminal`, `--harness`, `--as`, `--new`, `--file` and `--task -`.

   ```bash
   dockingbird review "Check the login flow"
   ```

   The step is done when the command prints these lines. From there the agent behaves like any delegated agent: wait, inbox, read and results work on it, and its status row shows its command and mode.

   ```text
   review-1 started on myapp (main).
   Thread <id>. Watch: dockingbird wait review-1
   ```

## The four keys that decide what a command does

| Key | Values | Effect |
|---|---|---|
| `tools` | `bus` (default), `default`, `full` | `bus` moves messages and files only, and no commits reach `sync`. `default` and `full` let the agent's commits reach you through `dockingbird sync`. |
| `workspace` | `repo` (default), `scratch` | `repo` is a copy of the repo. `scratch` is an empty folder of its own, needs no git repo, and an added config's command then runs from any folder. |
| `mode` | `bus` (default), `terminal` | `bus` runs the agent in the background through messages. `terminal` runs it at your terminal. A `mode` you write is fixed, and `--terminal` or `--bus` that disagrees is refused. |
| `context` | `kept` (default), `fresh` | `kept` is one conversation for every task delivery. `fresh` starts a new conversation for each, under the same rules. Bus only. |

The file can also pin three start flags. Write harness, mode or a limit in it, and a start that asks for something else is refused before anything starts. A key left out stays open to its flag.

| File key | Flag it fixes |
|---|---|
| `harness` | `--harness` |
| `mode` | `--terminal` and `--bus` |
| `[limits]` `cpus`, `memory`, `session_hours` | `--cpus`, `--memory`, `--session-hours` |

```text
review runs with mode = bus: .dockingbird/review.toml says so.
Drop the flag, or change the file.
```

The skill is different: only a bus agent takes it as a first turn, and a terminal agent receives the task as a plain message.

## The default command

One command of a repo's configs may say `default = true`. In that checkout, `dockingbird start "Check the login flow"` with no `--command` then runs it and says so first.

```text
Using review from .dockingbird/review.toml for this checkout
```

Two configs that each mark one command cancel each other out. A config that marks two commands is refused whole. A default in an added config is ignored, and `dockingbird claude` and `dockingbird codex` never use one.

## Share a config across repos

Adding a config copies it, with the files it names, into Dockingbird, and its commands then work in every repo. The copy is what runs, so add the file again after each change. The config takes its file's name unless you pass `--name NAME`.

```bash
dockingbird config add agents/triage.toml
dockingbird config remove triage
```

The step is done when these lines print. The "Replaced" line appears instead of "Registered" when you add a name you added before.

```text
Registered triage: dockingbird triage "task"
Replaced triage (was 7608094fd9980624)
Removed triage.
```

Agents already running keep the config they started with. Cleaning everything removes the added configs and never touches a repo's `.dockingbird/` folder.

| Case | What wins |
|---|---|
| A name in the repo's config and in an added one | the repo's own command, in that checkout; `dockingbird -h` says so |
| A name in two of the repo's own configs | neither runs |
| A name Dockingbird keeps, such as `status`, `start` or `claude` | the config is refused whole, and `config add` refuses it |

One file can hold several commands, each in a `[commands.NAME]` table, in place of the top-level `command`, `default` and `skill`. A table sets its own summary, default, skill and instructions, and may override any other key. The top instructions come before each command's own, and a top summary reaches no command.

## Skills

A config's `[skills]` table gives the agents of its commands skills their tool lists as its own. The `skill` key, singular, is another key: the first turn's text.

```toml
# Skills its tool lists (Claude Code's Skill tool and / menu, Codex's $ mention): one skills folder, or skill folders, each a path from this checkout's top. Default: none.
[skills]
path = ".agents/skills"
# Where they go in the agent's home: both (~/.claude/skills and ~/.agents/skills), claude or agents. Default: both.
into = "both"
```

A repo's own config's skills apply only in a checkout you have not marked untrusted. An added config's paths are relative to its file's folder, and `config add` copies them with it, so its skills are the ones it had when you added it, until you add it again. `--skills PATHS` on a start does the same for that start, and a skill it names replaces the config's skill of the same name. [Give agents skills](skills.md) has every rule, the bounds and how each tool lists the skills.

## Trust, tool arguments and secrets

A repo's own config comes with the repo, so whoever can push to it decides what it says. In a checkout you marked untrusted with `dockingbird trust --off`, three keys are off: `harness_args`, `[env]` and `repo_settings = true`. An added config's `harness_args` and `[env]` apply everywhere, since you chose to add it. The page [trust-and-repo-settings.md](trust-and-repo-settings.md) has the whole trust model.

`harness_args` take only Claude Code's `--model`, `--fallback-model`, `--max-turns` and `--effort`, with `low`, `medium`, `high`, `xhigh` or `max` as the effort. For Codex they take `--model`, `-m` and `-c model_reasoning_effort=LEVEL`. Anything else is refused, and the refusal names the allowed flags.

Only an added config may name `connections` and `browser`, and only by the names of connections you recorded with `dockingbird connect`, never as a value. See [connections.md](connections.md). A value in any config's `[env]` flows into the agent's environment, where the agent can read it. A key or a password therefore goes in an added config and never in the repo's file. Dockingbird refuses a config that holds one of its own tokens, or a sign-in or API key it keeps.

Your own Claude Code or Codex can start these commands too, through `dockingbird mcp`. See [mcp-server.md](mcp-server.md).

## When it fails

- [`CONFIG_INVALID_FILE`](../troubleshooting.md#config_invalid_file) refuses a file or a start. The line names the key and why, in words such as "a name Dockingbird keeps", "not an allowed value" or "only for a config you added", and never shows the value.
- [`CONFIG_PROBLEM_ROW`](../troubleshooting.md#config_problem_row) is one row of `dockingbird -h` or `config list` for a config, key or command that does not apply, such as `.dockingbird/review.toml: harness_args applies after dockingbird trust`.
- [`CONFIG_READ_FAILED`](../troubleshooting.md#config_read_failed) means Dockingbird could not read the configs. Its own commands still work.
- [`CONFIG_NOT_REGISTERED`](../troubleshooting.md#config_not_registered) means `config remove` found no added config of that name. `config list` shows the names.
- [`START_COMMAND_UNKNOWN`](../troubleshooting.md#start_command_unknown) means no config here gives that command. The message lists the ones that do.
- [`START_CONFIG_FIXED`](../troubleshooting.md#start_config_fixed) means a flag such as `--harness` or `--terminal` disagrees with a key the file fixes. Drop the flag or change the file.
- [`START_SKILLS_REFUSED`](../troubleshooting.md#start_skills_refused) means a start's `--skills` names what Dockingbird cannot use, such as a path with no skill or a link. Nothing was started. Fix that skill folder, or leave it out of `--skills`.
