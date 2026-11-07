---
title: Give agents skills
summary: Give an agent skills its tool lists as its own, at one start, from a config, on a running agent or for a swarm role.
audience: daily
commands:
  - start --skills
  - claude --skills
  - set --skills
  - fleet submit
  - fleet why
  - fleet release
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Give agents skills

A skill is a folder holding a `SKILL.md` and the files it uses (scripts, references, Codex's `agents/openai.yaml`), named by its folder. Dockingbird gives an agent skills its tool lists as its own: Claude Code in its Skill tool and its `/` menu, Codex for its `$` mention. This page shows four ways to give an agent skills: at one start, from a config, on a running agent and for a swarm role. A config's `skill` key, singular, is another key: the text of the agent's first turn, which [your own commands](your-own-commands.md) covers.

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- You stand in the git checkout that holds the skill folders. The examples use two skills in `.agents/skills`:

  ```text
  .agents/skills/a/SKILL.md
  .agents/skills/b/SKILL.md
  ```

- Each `SKILL.md` has a frontmatter that names a `description`. Codex lists no skill whose `SKILL.md` lacks one. Claude Code lists a skill with no frontmatter among its slash commands.

## 1. Give skills at one start

```bash
dockingbird start --skills .agents/skills "Fix the failing test"
dockingbird start --skills .agents/skills/a,.agents/skills/b "Fix the failing test"
```

`--skills PATHS` names skill folders, comma-separated, or a skills folder, each path relative to the folder you run the command in, or absolute. The first line gives the agent every skill of `.agents/skills`, the second those two. `dockingbird claude`, `dockingbird codex` and every config's command take the same option. A skill it names replaces a config's skill of the same name. Done when the start prints the agent, the thread and the way to follow it.

```text
claude-1 started on myapp (main).
Thread <id>. Watch: dockingbird wait claude-1
```

Message id `AGENT_STARTED_BUS`. A path Dockingbird cannot use stops the start, and nothing is started.

## 2. Name them in a config

A config's `[skills]` table gives the skills to every start of its command. Add it to a config such as the one [your own commands](your-own-commands.md) writes.

```toml
# .dockingbird/app.toml
command = "review"

[skills]
path = ".agents/skills"
into = "both"
```

- `path` is one skills folder, each of whose folders holding a `SKILL.md` is one skill (`path = ".agents/skills"`), or a list of folders, each one skill or a skills folder (`path = [".agents/skills/review", "tools/skills"]`). A repo's own config names paths from the checkout's top.
- `into` is where they go in the agent's home. `both`, the default, writes each skill to `~/.claude/skills`, where Claude Code finds personal skills, and to `~/.agents/skills`, where Codex finds a user's. `claude` or `agents` writes only that one.
- A repo's own config's skills apply only in a checkout you have not marked untrusted with `dockingbird trust --off`. An added config's skills, and the ones `--skills` names, apply everywhere.
- An added config's paths are relative to its file's folder, and `config add` copies them with it. Its skills are the ones it had when you added it, until you add it again.

Run the command. Done when it prints its start lines.

```bash
dockingbird review "Check the login flow"
```

```text
review-1 started on myapp (main).
Thread <id>. Watch: dockingbird wait review-1
```

In a checkout you marked untrusted, the command runs without the skills, and `dockingbird config list` and `dockingbird -h` say so in a row: `.dockingbird/app.toml: skills applies after dockingbird trust` (`CONFIG_PROBLEM_ROW`).

## 3. Add skills to a running agent

```bash
dockingbird set claude-1 --skills .agents/skills/a
```

`set` names the skills as `--skills` names them at a start, and reads them on this computer first. When one cannot be read, nothing changes. A skill of a name the agent has is replaced, and none is removed. Done when the line names the skills added.

```text
claude-1: skills added: a; its tool lists them from its next turn.
```

Message id `SET_SKILLS_DONE`. The end of the line says when the agent's tool lists them.

| The agent runs | Its tool lists the skills | The line ends |
|---|---|---|
| on the bus | from its next turn: Claude Code is told `/reload-skills` before that turn, and Codex reads them when its next turn starts | `its tool lists them from its next turn.` |
| on the bus, with its screen running | from its next idle prompt, where Claude Code is typed `/reload-skills` and Codex reads them again itself | `its tool lists them from its next idle prompt.` |
| at a terminal | within seconds, through Claude Code's own watcher or Codex's own re-read | `its tool lists them within seconds.` |

`--skills` goes alone. Beside another change, such as `--model`, `set` refuses both and changes nothing. The skills do not outlive a stop: a pick-up has the skills its own start names. A Codex agent started with no skill lists the skills added later within Codex's own budget, 2% of its context window, since Dockingbird sets its `skills.max_context_tokens` only at a start with skills.

## 4. Give a swarm role skills

A swarm's `[[role]]`, or a library role, may name `skills`, a table as a config's `[skills]` takes it. `path` is one skill or skills folder or a list of them, each a path from the top of the swarm's source, a library role's too. `into` is `both`, `claude` or `agents`.

```toml
[[role]]
name = "builder"
harness = "claude"
count = 2
brief = "briefs/builder.md"

[role.skills]
path = "tools/skills"
into = "both"
```

`fleet submit` reads the paths from the top of the checkout the definition is in, by a config's rules: no link, no hidden entry, the skills' bounds. It refuses `skills` in a swarm with no `[source]`, which has no clone. `fleet describe` reads no tree. Every start of the role's agents reads the trees from the swarm's clone, where its agents run, and places them as a config's skills are placed. The example names `tools/skills`, outside the clone's own `.agents/skills`, so a Codex role lists each skill once ([How each tool lists them](#how-each-tool-lists-them)).

```bash
dockingbird fleet submit NAME
```

Done when the swarm is queued.

```text
{id} pending, position {position}
```

Message id `FLEET_SUBMITTED`. What the submit cannot read is refused at its key, one `FLEET_REFUSED` line each: `role[N].skills.path`, `role[N].skills.<name>` for one skill, or `role[N].skills` for the set's bounds.

```text
refused: role[N].skills.path: not a skills table: path (skill or skills folders of the source checkout), into (both, claude or agents)
```

A start whose clone lacks a path, as when its branch moved after the submit, holds the swarm. The worker's log names the agent, its role, the key and the cause, and `fleet why` names the hold.

```bash
dockingbird fleet why ID
```

```text
{id} is held: skills_refused
```

Message id `FLEET_WHY_STATE`. Push the fix to the swarm's branch, then release the swarm.

```bash
dockingbird fleet release ID
```

Done when the line names the state the swarm entered.

```text
{id} {state}
```

Message id `FLEET_STATE_NOW`. From v0.15.12, every start attempt of a swarm in a clone of the worker's own, the one `fleet release` makes included, first fetches and fast-forwards that clone from its `origin`, so the fix you pushed reaches the start. A clone that cannot fast-forward, because it holds commits not yet pushed, is used as it is, and the worker's log says so. A checkout your home links by hand is never fetched. Before v0.15.12, only a swarm's first attempt fetched, so a release after a hold read the clone as the first attempt left it and held the swarm again.

## How each tool lists them

Dockingbird places each `SKILL.md` as it is, its frontmatter and any hooks it names included.

| Topic | Claude Code | Codex |
|---|---|---|
| Where `into` writes them | `~/.claude/skills`, where Claude Code finds personal skills (`both` or `claude`) | `~/.agents/skills`, where Codex finds a user's (`both` or `agents`) |
| How it lists them | in its Skill tool and its `/` menu | in a table of its skill roots, each with an alias (`r0`, `r1`, ...), `~/.agents/skills` among them, and one line per skill naming its `SKILL.md` under its root's alias |
| Listing budget | 1% of its context window | 2% of its context window, or 8,000 characters when it doesn't know the window; for an agent started with skills, the 10,000 tokens Dockingbird sets (below) |
| Each description cut at | 1,536 characters | 1,024 characters |
| A `SKILL.md` without a frontmatter `description` | listed among its slash commands when it has no frontmatter | not listed |
| A skill of the same name in the checkout's own `.claude/skills` or `.agents/skills`, which the tool loads | lists only the one in your personal folder, the one Dockingbird wrote | lists both |

Past its budget, Codex shortens the descriptions, then leaves out whole skills, user skills (the ones in `~/.agents/skills`) first. For an agent with skills, Dockingbird sets Codex's `skills.max_context_tokens` to its cap, 10,000 tokens. A skill whose `agents/openai.yaml` turns implicit use off (`allow_implicit_invocation: false`) is left out of Codex's list and reached by a `$` mention alone. A Codex role whose `path` is the clone's own `.agents/skills` lists each skill twice, the placed copy and the repository's; name a folder outside it to list each once.

## Bounds

| Bound | Figure |
|---|---|
| Entries in one `skills.path` or one `--skills` | 16 |
| Skills of one agent, a config's and a start's together | 32 |
| Files in one skill | 64 |
| Depth of a file under its skill folder | 8 path parts |
| One file of a skill | 1 MiB |
| One agent's skills together, as Dockingbird records them | 4 MiB |
| Codex's `skills.max_context_tokens` for an agent with skills | 10,000 tokens |

A refusal past a bound names the key that went over, never a path.

## When it fails

- [`START_SKILLS_REFUSED`](../troubleshooting.md#start_skills_refused) stops a start whose `--skills` names what Dockingbird cannot use: an empty path between commas, a path with no skill, a link, a skill named twice, a skill folder named `synced` (Claude Code's folder of synced skills), or a file it can't read safely. The line `--skills: {key}: {cause}` names the key and why, and nothing was started. Fix that skill folder, or leave it out of `--skills`.
- [`SET_SKILLS_REFUSED`](../troubleshooting.md#set_skills_refused) refuses `set --skills` for the same causes, or when the agent's skills with those added would be more, or larger, than an agent may have. The line `--skills: {key}: {cause}; nothing was changed.` names the key and why. Fix that skill folder, or leave it out of `--skills`.
- [`CONFIG_INVALID_FILE`](../troubleshooting.md#config_invalid_file) refuses a config whose `[skills]` table Dockingbird cannot use. The line names the key, such as `skills.path`, and why, and never shows the value. Fix that, then run the command again.
- [`OPTIONS_NOT_BOTH`](../troubleshooting.md#options_not_both) means `set --skills` came with another change, such as `--model`. Nothing changed. Give `--skills` in a `set` of its own.
- [`FLEET_REFUSED`](../troubleshooting.md#fleet_refused) names a role's `skills` key that `fleet submit` could not read, such as `role[N].skills.path`, or `skills` in a swarm with no `[source]`. Fix the folder or the key, then submit again.
- [`FLEET_WHY_STATE`](../troubleshooting.md#fleet_why_state) prints `{id} is held: skills_refused` when a start's clone lacks a path a role's `skills` names. Push the fix, then run `dockingbird fleet release ID`.
