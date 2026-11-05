---
title: The work queue
summary: Keep one board of items, agents and requests in the organisation's store that people, scripts and agents read and write from any computer.
audience: team-admin
commands:
  - work status
  - work show
  - work search
  - work new
  - work needs-you
  - work set
  - work log
  - work eta
  - work check
  - work requests
  - work respond
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# The work queue

This guide for teams sets up one shared board of what is being built. The board lives in your organisation's store, so a person, a script and an agent read and write the same rows from any computer that has the org login. It holds items, the agents that work on them and the requests agents file.

## Before you start

- The store exists and this computer has an org login. `dockingbird org status` ends with `Connected as {role}.` when it does. [The team fleet guide](team-fleet.md) sets both up.
- `dockingbird org create` has run at this release. It makes the `work` schema beside `fleet` and `org`. Run it again after an update to apply a newer migration.
- The top help screen does not list `work`. `dockingbird work -h` shows every action, and every action takes `--json`.

## What the board holds

| Row | What it is |
|---|---|
| item | one unit of work with a title, area, status, priority, owner, ETA, deadline, a line for what is happening now and the step after it, the items it waits for and, when it waits for you, the ask |
| event | one change to an item, or one thing that happened to it, such as a merge, a review, a hand-back or a note; events are only added, so an item's log is its history |
| agent | one session that works on an item, with its task, role, model, effort, the item and pull request, its ETA and, once it ends, its outcome |
| request | what an agent asks of the coordinator, such as a bug, a feature, a question or a hand-off, kept with the answers it gets |

The admin and each person's login read and write the board, a person through membership of a project's group. A machine's worker only reads. A write it tries is refused by the database. Each event and each answer records the database login that wrote it.

## 1. Read the board

`work status` lists the items in work, those not archived and not in the backlog, by priority, then ETA, then id. `--all` adds the backlog. `--area`, `--status` and `--priority` each take one value.

```bash
dockingbird work status
dockingbird work needs-you
dockingbird work show login-page
dockingbird work search "login"
dockingbird work check
dockingbird work requests
```

`needs-you` lists the items whose status is `waiting-user`, each with its ask. `show` prints one item's fields, then its events, newest first. `search` prints the best 50 hits over items, events, agents, requests and answers, an exact item id or request number first. `check` prints what the schema cannot refuse by itself: a dependency cycle, an agent with no end on an archived item, and a request still open on one. It ends 1 when it prints any. `requests` lists the open requests, and `--all` adds the answered ones.

```text
{priority} {item_id} {state}, owner {owner}, ETA {eta}, waits for {waits}
  now: {text} ({count} of {total} {unit})
  asks: {text}
{requests} open requests, {agents} agents running
The queue checks out: no dependency cycle, and nothing open on an archived item.
```

An empty read prints one of `No item is in work.`, `No item waits for you.`, `No agent is running.`, `No request is open.` or `Nothing in the queue matches.`

## 2. Add and change an item

`work new` makes an item in the backlog, as a feature, unless `--status` or `--kind` says otherwise. The id is a slug. `work set` changes one field and records the change as an event. `work eta` sets the ETA that long from now, as an `estimate` or as `measured`. `work log` adds one event. All of them record the time of the computer they run on.

```bash
dockingbird work new login-page --title "Login page" --area web --priority P1 --owner user
dockingbird work set login-page status in-progress
dockingbird work set login-page now "wiring the form" --count 2 --total 5 --unit steps
dockingbird work eta login-page --in 2h --kind estimate
dockingbird work log login-page --kind merge --pr 42 --sha SHA --text "merged to main"
```

```text
Added login-page: P1, backlog, owner user.
Set status of login-page to in-progress.
Set now of login-page to wiring the form.
login-page: ETA {eta}, estimate.
Logged merge on login-page.
```

`work set` takes these fields: `title`, `area`, `status`, `priority`, `kind`, `owner`, `agent`, `project`, `workload`, `observed_at`, `deadline`, `depends_on`, `links`, `ask`, `now`, `next` and `eta`. `depends_on` and `links` are comma lists that replace what was. `deadline` takes a date, a date with a time, or `none`. `eta` takes only `none` and clears it. An event kind of `work log` is `log`, `merge`, `review`, `launch` or `handback`, and a `merge` needs `--pr` and `--sha`. `--ago MIN` records an event noticed late, at most 1,440 minutes ago.

An item of kind `bug` names the commit it was seen at with `--observed-at`. An item whose status is `waiting-user` carries its ask. `dockingbird work set ITEM status done` archives the item, and it leaves `work status`.

## 3. File and answer requests

When an agent needs something from the coordinator, it files a request, and the coordinator answers it. The body comes from `--text`, or from a UTF-8 file named by `--file`. A sender may hold only one open request with a given title, and case does not count. Any answer but `needs-info` closes the request, while `needs-info` leaves it open for the sender's `request info` reply.

```bash
dockingbird work request new --from build-1 --kind question --title "Which API version" --text "v1 or v2?"
dockingbird work respond 7 --decision answered --text "v2"
dockingbird work request show 7
dockingbird work request info 7 --text "the client is v2 only"
```

```text
Filed request 7 for {recipient}.
Answered request 7: answered.
```

## 4. Track a swarm

The item for a feature exists before the swarm is submitted. When `fleet submit` answers with the workload's id, the item takes it. Each agent of the roster gets a row, and each hand-back ends its row.

```bash
dockingbird work set login-page workload ID
dockingbird work agent start build-1 --task "login form" --kind implementer --model MODEL --effort EFFORT --item login-page --pr 42
dockingbird work agent eta build-1 --eta 45m --why "tests rerun"
dockingbird work agent done build-1 --outcome done --result "merged"
dockingbird work agents
```

Each command confirms itself, and `work agents` lists the agents that have not ended. A running agent shows as `working` while its ETA is ahead or not set, and `past its ETA` after.

```text
Recorded build-1: implementer, MODEL, EFFORT.
build-1: ETA {eta}.
build-1 ended: done.
{agent} ({kind}, {model}, {effort}) {state}, started {age} ago, ETA {eta}: {text}
```

## Words the board accepts

Your organisation owns four words: an area, a model, an effort and a project. An area is a slug of lowercase letters, digits and `-`, at most 63 characters long, and a project is the slug of one of your projects. The other fields take only the words in the table. A word outside the table is refused by the field's name, and the command prints the words that field takes. The agent kinds are the six roles Dockingbird ships, plus `other`.

| Field | Words |
|---|---|
| status | `backlog`, `ready`, `in-progress`, `review`, `blocked`, `waiting-user`, `done` |
| priority | `P0` now, `P1` this week, `P2` soon, `P3` when there is time |
| kind | `feature`, `bug`, `task`, `decision`, `program` |
| owner | `main` (the coordinating session), `user` (the operator), `agent` (the agent the item names), `none` |
| ETA kind | `measured`, `estimate`, `none` |
| agent kind | `coordinator`, `implementer`, `reviewer`, `tester`, `hands`, `reader`, `other` |
| agent outcome | `done`, `partial`, `blocked`, `stopped` |
| request kind | `bug`, `feature`, `question`, `handoff`, `claim`, `progress`, `finish`, `release` |
| answer decision | `accepted`, `granted`, `refused`, `done`, `needs-info`, `answered` |

## Limits and exit statuses

A body is at most 65,536 bytes of UTF-8. A title, an ask, a now line and a log line are one line of at most 1,000 characters. No event is changed or deleted, whatever the login. See [exit codes](../reference/integration/exit-codes.md).

| Exit status | Meaning |
|---|---|
| 0 | the command did its work |
| 1 | the store refused a write, or names no such item, agent or request |
| 2 | the words or options were refused before any connection |
| 69 | the database did not answer |
| 78 | the org login is missing or turned down |

## When it fails

- [`WORK_NOT_FOUND`](../troubleshooting.md#work_not_found) means the queue has no such item, agent or request. `work status --all` lists what it holds.
- [`WORK_REFUSED`](../troubleshooting.md#work_refused) means a value broke a rule, such as an id in use, a word outside a list or a request of that title still open.
- [`WORK_OPTION_NEEDED`](../troubleshooting.md#work_option_needed) means an option is missing, such as `--title` for `new`, or neither `--text` nor `--file` for a request.
- [`WORK_OPTION_NOT_HERE`](../troubleshooting.md#work_option_not_here) means an option belongs to another action. Nothing was read.
- [`WORK_FILE_UNREADABLE`](../troubleshooting.md#work_file_unreadable) means the `--file` is not readable UTF-8 text, or is longer than a body may be.
- [`WORK_PROBLEM`](../troubleshooting.md#work_problem) comes from `work check`. Fix each problem it names with `work set`, `agent done` or `respond`.
- [`ORG_ROLE_MISSING`](../troubleshooting.md#org_role_missing) means this computer has no login for the kind the command connects as.
- [`FLEET_DB_UNREACHABLE`](../troubleshooting.md#fleet_db_unreachable) means the database did not answer, and the command ends 69.
- [`FLEET_DB_REFUSED`](../troubleshooting.md#fleet_db_refused) means the database turned the login down, and the command ends 78.
