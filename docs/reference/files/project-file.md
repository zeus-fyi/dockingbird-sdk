---
title: What dockingbird init writes
summary: The files dockingbird init writes into a repo, and every key of .dockingbird/project.toml.
audience: daily
commands:
  - dockingbird init
  - dockingbird init --check
  - dockingbird init --force
  - dockingbird init --project
  - dockingbird init --no-register
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# What dockingbird init writes

Run `dockingbird init` anywhere in a repo and it writes a project file, a rules file, an example swarm, the skills of the release, the agent definitions, and a lock file that lists each installed file with its digest.
Commit all of them with `git add .dockingbird .agents .claude && git commit`, so every clone of the repo has the same set-up.

## The files

| Path | What it holds | Later runs of `init` |
|---|---|---|
| `.dockingbird/project.toml` | the project's file; keys below | never rewritten |
| `.dockingbird/rules.md` | the lines every agent of the project gets after Dockingbird's own rules; an agent's whole rules text may be 64 KB at most | never rewritten |
| `.dockingbird/swarms/example/` | an example swarm; fill its `[placement] hosts` from `dockingbird fleet hosts`, then `dockingbird fleet submit .dockingbird/swarms/example` | never rewritten |
| `.dockingbird/roles/` | the role library: `index.toml` and one file for each shipped role, which you edit freely; see [roles-and-connections.md](roles-and-connections.md) | `--force` writes the release's `index.toml` again |
| `.agents/skills/` | this release's skills | changed only where a new release changed a file |
| `.claude/skills` | a link to `../.agents/skills` | kept |
| `.claude/agents/` | this release's agent definitions | changed only where a new release changed a file |
| `.dockingbird/skills.lock` | every file `init` installed, each with its digest; its `release` line only records which release last wrote it and is never judged | changes with the files it lists |

A file you edited is kept and named, and `--force` replaces it.
`init` writes nothing through a link: a `.dockingbird`, `.agents` or `.claude` that is a link, or a `.claude/skills` that links anywhere but `../.agents/skills`, stops it before anything is written.

## Keys of project.toml

`slug` and `version` are required; every other key is optional.
A key or a table outside this list is refused, and the refusal names the key.

| Key | Values | Default | What it holds |
|---|---|---|---|
| `version` | `1` | `1` | the file's format; another number is refused |
| `slug` | lowercase letters, digits and `-` | `--project SLUG`, else the name of the repo's `origin` remote, else its folder's | the project's name in your organisation's store |
| `release` | text | the release that ran `init` | the release whose `init` wrote the file and its skills |
| `[org] ops_repository` | `owner/name` | empty | written empty by `init`; leave it empty |
| `[checks] runner_host` | a host name of `hosts.toml` | empty | written empty by `init`; leave it empty |
| `[checks] runner_script` | a path in the repo | empty | written empty by `init`; leave it empty |
| `[rules] file` | a path in the repo | `.dockingbird/rules.md` | the project's rules file, read at every start; a file that is missing, a link, not UTF-8 text or holding a Dockingbird credential stops the start |
| `[roles.NAME] harness` | `claude` or `codex` | `claude` | the tool a bus agent of the role `NAME` runs; one table for each shipped role |
| `[roles.NAME] model` | the tool's model word | empty | empty means the organisation's store row for that kind of role, else `fleet submit` refuses the role |
| `[roles.NAME] effort` | the tool's effort word | empty | empty means the store's row, else `fleet submit` refuses the role |
| `[lint] forbidden` | list of words | none | words this repository refuses, each a non-empty single line |

## Registering the project

| Case | Result |
|---|---|
| an org login on this computer | `init` adds the project to your organisation's store as your `user` role: its slug, the `origin` remote's address, the default branch and this release, once; a later run says the store has it |
| a login that is not an admin, a store that is not made yet, or a store that does not answer | the line names the cause and `init` still ends 0 |
| no org login | the line says to log in first with `dockingbird org login HOST --as user --role ROLE` |
| `--no-register` | skips the step |

## Messages

| Id | When |
|---|---|
| [INIT_DONE](../../troubleshooting.md#init_done) | the first run wrote the files |
| [INIT_CURRENT](../../troubleshooting.md#init_current) | everything is already this release's |
| [INIT_OUT_OF_DATE](../../troubleshooting.md#init_out_of_date) | `init --check` found files that are not this release's; exit 1 |
| [INIT_FILE_EDITED](../../troubleshooting.md#init_file_edited) | a file you edited was kept |
| [INIT_PROJECT_FILE_INVALID](../../troubleshooting.md#init_project_file_invalid) | `project.toml` has a key or value Dockingbird does not read |
| [RULES_FILE_MISSING](../../troubleshooting.md#rules_file_missing) | `[rules] file` names a file that is not there, so no agent starts |
