---
title: Search the docs
summary: Search these docs from a clone with one Python command, offline, and see how it ranks what it finds.
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../llms.txt).

# Search the docs

`search/search.py` searches every page of these docs on your own computer. It reads two files from the `search/` folder and needs no network or package.

## Before you start

- `python3 --version` must print 3.9 or a later version.
- Run the command from the root of a clone of this repository, where the `search/` folder is.

## Search from a clone

```bash
python3 search/search.py "trust" --top 1
```

```text
1. docs/guides/trust-and-repo-settings.md#1-mark-a-checkout-untrusted  score 55.21
   Trust and repo settings > 1. Mark a checkout untrusted
   dockingbird trust --off
```

| Line | What it shows |
|---|---|
| 1 | the rank, the page with the section's anchor, the score, and `(phrase)` when the section holds the whole query |
| 2 | the heading path, from the page title down to the section |
| 3 | the section's first line, cut at 160 characters |

Open the page at the anchor to read the whole section. Flags work as queries too, so `python3 search/search.py --json` lists every section that uses `--json`.

| Option | What it does |
|---|---|
| `--top N` | prints N sections instead of 10 |
| `--audience NAME` | doubles the score of sections for one reader: `first-day`, `daily`, `integrator` or `team-admin` |
| `--index PATH` | reads another `index.json.gz`, with its `chunks.jsonl` in the same folder |

| Exit status | Meaning |
|---|---|
| 0 | at least one section matched |
| 1 | no section matched, and the command printed `no results` |
| 2 | an option is wrong or an index file is missing, and the message names it |

## The files the build writes

A workflow runs `.github/scripts/build_index.py` on every push to `main` and commits what it writes.
A rebuild overwrites these files, so change the pages and leave the files to the build.

| File | What it holds | Who reads it |
|---|---|---|
| [llms.txt](../llms.txt) | one line per page with its summary, in reading order, under Start here, Concepts, Guides and the rest | a coding agent on its first read |
| [docs/manifest.json](manifest.json) | one record per page: path, title, summary, audience, the commands it shows and the message ids it names | a script or an agent that picks pages by audience, command or id |
| `search/index.json.gz` | the word counts of each section, field by field | `search/search.py` |
| `search/chunks.jsonl` | one line per section: page, heading path, anchor, text, commands, flags, ids, tool names, audience, first sentence | `search/search.py`, and any tool that wants the text |
| `docs/troubleshooting/<area>.md` | ten index pages, each message id of one area with the line saying when it appears | a reader who knows the area but not the id |
| `search/search.py` | the search command, copied from `.github/scripts/` | you |

The build exits 1 and the workflow commits nothing when a page breaks a rule.
It checks for missing front matter, links to missing files, unclosed code fences and ids the catalogue lacks.
The file `search/queries.txt` pairs 30 queries with the page each one must find.
The workflow fails when one of those pages drops out of its query's top 3.

## How the search ranks

1. A word the docs never use becomes the closest word they do use, at most two letters off. The output prints each correction on its own line, above the results.
2. A section that holds a query of three or more words, word for word, comes first. A line copied from the screen therefore lands on its message's entry.
3. A message id, an MCP tool name, and a command or flag shown in a `bash` block score five times a plain word. A word in a heading scores twice a word in the text.
4. A flag keeps its dashes and a tool name keeps its underscores, so each stays one word. Ids also split at `_`, so `completion already` finds `COMPLETION_ALREADY`.
5. A command counts by its subcommand, so `trust` finds every section whose `bash` block runs `dockingbird trust`.
6. When the query names a message id, that id's entry in the [catalogue](troubleshooting.md) ranks above every guide. Words that spell an id with spaces count as naming it. Otherwise the guides and the other pages rank above the catalogue.
7. With `--audience`, sections written for that reader score twice as high as the rest.
8. Equal scores follow the reading order of `manifest.json`, from getting started to reference.

A long section cut into several parts appears once in the results, at its best part.
