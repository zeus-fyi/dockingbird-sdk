---
title: Your own review command
summary: Write a .dockingbird/review.toml with a skill and instructions, run dockingbird review in the repo, then register it for every repo.
audience: daily
commands:
  - config add
  - config list
  - review
---

# Your own review command

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Goal: add a `dockingbird review "task"` command that starts a Claude agent on the bus, hands it your review skill and role text, and returns a list of fixes. You write one config, run it in one repo, then register it for every repo. The guide behind it is [your-own-commands.md](../../docs/guides/your-own-commands.md), and every key is in [the app config reference](../../docs/reference/files/app-config.md). The file below grows from the template in [templates/.dockingbird/app.toml](../../templates/.dockingbird/app.toml), plus its `context` key.

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- You stand in a git checkout of your repo, here called `myapp`. `git status` runs.
- No config of that name exists yet. `dockingbird config list` prints "No configs yet." or does not list `review`.

## Steps

1. Write the config file `.dockingbird/review.toml`. Every key has a comment, and a key you drop takes its default. The skill and instructions paths are read from the folder that holds this file.

   ```toml
   # .dockingbird/review.toml: adds dockingbird review in this checkout. Every key is optional.

   # The command: dockingbird review "...", agents review-1, review-2. Default: the file's name.
   command = "review"
   # Its one line in dockingbird -h and config list, and for your own harness through dockingbird mcp. Default: none.
   summary = "Review this branch and list what to fix"
   # true: dockingbird start with no --command runs review in this checkout. Default: false.
   default = false
   # On the bus, this file's text, with $TASK replaced by the task, is the first turn. Default: none.
   skill = "skills/review.md"
   # Role text, given to the agent after Dockingbird's own rules. Default: none.
   instructions = "review-role.md"
   # claude or codex. Default: claude. Set here, it is fixed: a start's --harness can't change it.
   harness = "claude"
   # repo: a copy of this repo; scratch: an empty folder of its own, no git repo needed
   # (an added config's command then runs from any folder). Default: repo.
   workspace = "repo"
   # bus: in the background, through messages; terminal: at your terminal. Default: bus. Set, it is fixed.
   mode = "bus"
   # kept: one conversation for all its deliveries; fresh: every task delivery starts a new conversation,
   # under the same rules (bus only). Default: kept.
   context = "fresh"
   # true: load the repo's own Claude Code or Codex settings, hooks and MCP servers, once trusted. Default: false.
   repo_settings = false
   # Its tools: "bus" (messages and files), "default" (claims and commits) or "full" (both). Default: "bus".
   tools = "bus"
   # allowlist: through a proxy of its own, its tool's hosts and those of allow; models: its tool's hosts alone;
   # none: no network, not even its model's API; full: its own network, open to the internet.
   # Default: full, or what dockingbird egress set.
   egress = "allowlist"
   # With allowlist, what else it may reach: the presets registries (package registries) and github
   # (GitHub's content), or hosts such as "docs.python.org" and "*.corp.example".
   # Default: the list dockingbird egress set, else nothing beyond its tool's own hosts.
   allow = ["registries", "github"]
   # Fixed arguments for the tool, such as its model. Default: none.
   harness_args = ["--model", "claude-haiku-5-5"]
   # mise's environments for its agents, comma-separated: "ci" makes mise read mise.ci.toml over mise.toml
   # (MISE_ENV). Default: none.
   mise_env = "ci"

   # Variables the agent's tool sees: settings, never secrets. Default: none.
   [env]
   REVIEW_STYLE = "short"

   # Bounds on an agent that works on the bus.
   [limits]
   # A turn that runs longer is interrupted and reported; at least 1.
   # Default: no turn deadline (a stuck turn ends with the session).
   turn_minutes = 20
   # The agent stops itself after this many hours; at least 1, and at most
   # the installation's maximum (168 by default). Default: 12.
   session_hours = 4
   ```

   The bus tools mean the agent shares no commits, so it reports through messages and attached files. A fresh context means a new conversation for each review.

2. Write the skill file `.dockingbird/skills/review.md` as plain Markdown. On the bus the agent gets it as its first turn, with your task where `$TASK` stands.

   ```markdown
   Review the changes on this branch for this task:

   $TASK

   List what to fix, file by file, in a Markdown file you attach, then mark the task done.
   ```

3. Write the role file `.dockingbird/review-role.md`. Two or three lines are enough, and the agent reads them right after Dockingbird's own rules.

   ```markdown
   You review code; you never change it.
   ```

4. Ask Dockingbird to list its configs. This repo's come first, each with its summary beneath.

   ```bash
   dockingbird config list
   ```

   The step is done when a row shows review with the source "this repo" and the summary sits below it. The other cells hold the workspace, the mode, the connections and the start of the digest.

   ```text
     review  this repo  review  repo  bus  <connections>  <digest>
       Review this branch and list what to fix
   ```

5. Run the command. It accepts every option of `start` except `--command`, and your task lands in the skill.

   ```bash
   dockingbird review "Check the login flow"
   ```

   The step is done when the command prints these lines.

   ```text
   review-1 started on myapp (main).
   Thread <id>. Watch: dockingbird wait review-1
   ```

   Then `dockingbird wait review-1` returns the agent's messages, and `dockingbird results review-1` saves the Markdown file it attached.

6. Register the command for every repo. The copy of the config and the two files it names go into Dockingbird, and the command then works in any repo. Add it again after each change, because the copy is what runs. An added config's `harness_args` and `[env]` apply at once, since you chose to add it.

   ```bash
   dockingbird config add .dockingbird/review.toml
   ```

   The step is done when the command prints this line. It prints "Replaced review" with the old digest when you add it again.

   ```text
   Registered review: dockingbird review "task"
   ```

   In this checkout the repo's own command still wins over the added one, and `dockingbird -h` says so with a line that starts `configs/review/config.toml: commands.review is replaced here by this repo's own`. In every other repo the added command runs.

7. Remove the added copy when you no longer want it in every repo. The repo's own file is untouched.

   ```bash
   dockingbird config remove review
   ```

   The step is done when the command prints this line.

   ```text
   Removed review.
   ```

## When it fails

- [`CONFIG_INVALID_FILE`](../../docs/troubleshooting.md#config_invalid_file) refuses the file in step 4, 5 or 6. The line names the key and the cause, such as "not an allowed value" or "a name Dockingbird keeps", and never shows the value.
- [`CONFIG_PROBLEM_ROW`](../../docs/troubleshooting.md#config_problem_row) lists a key that does not apply yet. In a checkout you marked untrusted, it reads `harness_args applies after dockingbird trust`, and `[env]` and `repo_settings = true` are off the same way.
- [`START_COMMAND_UNKNOWN`](../../docs/troubleshooting.md#start_command_unknown) in step 5 means no config here gives `review`. Run `dockingbird config list` from the checkout that holds the file.
- [`START_CONFIG_FIXED`](../../docs/troubleshooting.md#start_config_fixed) means a flag such as `--terminal` or `--harness codex` disagrees with the `mode` or `harness` the file fixes. Drop the flag, or edit the file.
- [`CONFIG_NOT_REGISTERED`](../../docs/troubleshooting.md#config_not_registered) in step 7 means no added config has that name. `dockingbird config list` shows the added ones.
