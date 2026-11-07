---
title: Commands
summary: Every command a customer can type, with its arguments, one line of purpose, its exit statuses and the guide that explains it.
audience: daily
commands:
  - dockingbird claude
  - dockingbird codex
  - dockingbird status
  - dockingbird sync
  - dockingbird stop
  - dockingbird init
  - dockingbird login
  - dockingbird logout
  - dockingbird trust
  - dockingbird egress
  - dockingbird env
  - dockingbird homes
  - dockingbird start
  - dockingbird send
  - dockingbird inbox
  - dockingbird read
  - dockingbird questions
  - dockingbird answer
  - dockingbird wait
  - dockingbird results
  - dockingbird search
  - dockingbird set
  - dockingbird swarm
  - dockingbird license
  - dockingbird update
  - dockingbird pin
  - dockingbird clean
  - dockingbird completion
  - dockingbird fleet
  - dockingbird cp
  - dockingbird node
  - dockingbird org
  - dockingbird work
  - dockingbird inspect swarm
  - dockingbird connect
  - dockingbird connections
  - dockingbird revoke
  - dockingbird disconnect
  - dockingbird serve
  - dockingbird watch
  - dockingbird config
  - dockingbird mcp
  - dockingbird ui
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Commands

Each table lists the commands of one group with their arguments, one line of purpose, the exit statuses they end with and the page that explains them.
Statuses 0, 1 and 2 are on every command, and [exit-codes.md](integration/exit-codes.md) explains 69, 77, 78 and the tool's own.
`dockingbird COMMAND -h` prints the same arguments from the installed release, and the unlisted `fleet`, `work` and `inspect swarm` commands are included here.

## Global options

| Option | Where it goes | What it does |
|---|---|---|
| `--json` | before the command | prints every message as one line of JSON, an envelope; see [json.md](integration/json.md) |
| `--verbose` | before the command | adds ids, codes, paths and timings, and shows each message's id in brackets such as `[NOTHING_NEEDS_YOU]` |
| `--home NAME` | before the command | runs in the home `homes/NAME` of the default home; refused with exit 2 when `DOCKINGBIRD_HOME` is also set; see [home-layout.md](files/home-layout.md) |
| `-h`, `--help` | alone, or after any command | prints the help; under `--json` it is an envelope whose `id` is `HELP` |
| `-v`, `--version` | alone | prints the versions of Dockingbird, Claude Code and Codex, and marks a pinned one |

For `claude` and `codex` the global options go before the tool's name, as in `dockingbird --verbose claude`, because everything after it belongs to the tool.
After a command, `--home NAME` belongs to `--host` on `status`, `swarm` and `inspect`, and names a home of that host.

## Everyday

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `claude` | `[--as NAME] [--new] [--egress MODE] [--cpus N] [--memory SIZE] [--no-toolchain] [--no-deps] [--agent-md PATH] [--claude-md PATH] [--skills PATHS] [-- TOOL ARGS]` | starts Claude Code on this repo in its own container, picks up kept work, or reconnects to a running agent | the tool's own, 1, 2 | [daily-loop.md](../guides/daily-loop.md) |
| `codex` | the same as `claude`; `--claude-md` is refused | starts Codex on this repo in its own container, picks up kept work, or reconnects to a running agent | the tool's own, 1, 2 | [daily-loop.md](../guides/daily-loop.md) |
| `status` | `[NAME] [--host NAME] [--home NAME]` | shows who works on what, what was shared today and what needs you; with a name, one agent; reads only | 0, 1, 2 | [daily-loop.md](../guides/daily-loop.md) |
| `sync` | `[--accept COMMIT] [--let-go]` | takes the agents' commits on your branch and sends yours; `--accept` resumes after a pause, `--let-go` makes your branch the one after you refused a deleted branch's commits | 0, 1, 2 | [daily-loop.md](../guides/daily-loop.md) |
| `stop` | `[NAME ...] [--yes]` | stops the named agents, or every agent and Dockingbird itself; nothing is lost | 0, 1, 2 | [daily-loop.md](../guides/daily-loop.md) |
| `init` | `[--project SLUG] [--check] [--force] [--no-register]` | makes this repo ready: the project file, rules, an example swarm, skills and agent definitions; `--check` writes nothing and exits 1 when files are not this release's | 0, 1, 2 | [first-run.md](../getting-started/first-run.md) |
| `login` | `TOOL [--here] [--api-key [--base-url URL]]`, `claude --oauth-token - [--base-url URL]`, `codex --auth-json -` | signs in again or as someone else; TOOL is `claude` or `codex`; the last login wins | 0, 1, 2 | [sign-in-and-api-keys.md](../guides/sign-in-and-api-keys.md) |
| `logout` | `TOOL` | signs the tool out and removes its saved API key; your own sign-ins are untouched | 0, 1, 2 | [sign-in-and-api-keys.md](../guides/sign-in-and-api-keys.md) |
| `trust` | `[PATH] [--off] [--forget]` | marks a repo trusted, or with `--off` keeps its own settings, hooks and MCP servers off on this computer; `--forget` is `--off` | 0, 1, 2 | [trust-and-repo-settings.md](../guides/trust-and-repo-settings.md) |
| `egress` | `[MODE] [--allow ENTRY]...`, `--reset` | shows or sets what new agents may reach: `allowlist`, `models`, `none` or `full` | 0, 1, 2 | [egress-and-network.md](../guides/egress-and-network.md) |
| `env` | none | shows the toolchain the repo's agents get | 0, 1, 2 | [toolchains.md](../guides/toolchains.md) |
| `env install` | none | installs those versions now, so a start waits for none | 0, 1, 2 | [toolchains.md](../guides/toolchains.md) |
| `env lock` | none | writes each version into the repo's `mise.toml` and locks it in `mise.lock` | 0, 1, 2 | [toolchains.md](../guides/toolchains.md) |
| `env use` | `TOOL VERSION` | writes one version into `mise.toml`; agents started from now get it | 0, 1, 2 | [toolchains.md](../guides/toolchains.md) |
| `homes` | none | lists every Dockingbird home on this computer, one line each; reads only | 0, 1, 2 | [updates.md](../guides/updates.md) |

## Agents

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `start` | `[TASK] [--command NAME] [--terminal] [--bus] [--harness TOOL] [--egress MODE] [--cpus N] [--memory SIZE] [--compact-at N] [--session-hours N] [--cpu-shares N] [--pids-limit N] [--no-toolchain] [--no-deps] [--agent-md PATH] [--claude-md PATH] [--skills PATHS] [--as NAME] [--swarm NAME] [--role ROLE] [--new] [--file PATH]... [--task -] [-- TOOL ARGS]` | gives an agent a task; it works in the background on the bus and `start` prints its name | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `send` | `NAME TEXT [--file PATH]... [--reply-to ROW] [--kind KIND] [--payload JSON] [--withdraw ROW]` | answers an agent's question or gives it more to do | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `inbox` | `[--all] [--page N] [--priority P0 to P3] [--questions] [--clear] [--swarm NAME,NAME] [--engine ID,ID] [--no-swarm]` | lists the questions and results waiting for you, one numbered row each | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `read` | `ROW [--keep] [--swarm NAME,NAME] [--engine ID,ID] [--no-swarm]` | reads one message in full; `--keep` leaves it unread | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `questions` | `[ROW]` | lists the open questions your agents ask, or shows one whole | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `answer` | `ROW (--option N or TEXT)` | answers a question by its option number or in words | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `wait` | `[NAME] [--seconds SECONDS]` | waits up to 25 seconds by default for an agent's next message | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `results` | `NAME [--to DIR]` | saves the files an agent shared as files on your computer, overwriting nothing | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `search` | `TEXT` | finds the newest messages whose subject or body has every word of TEXT | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `set` | `NAME [--model MODEL] [--effort LEVEL] [--compact-at POINT] [--skills PATHS] [--stop-after-turn] [--run-turns]` | changes a running bus agent's model, effort or compact point from its next turn; `--skills`, given alone, adds skills to a running agent; `--stop-after-turn` ends it after its running turn | 0, 1, 2 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| `swarm list` | `[--json]` | lists each swarm of this home and how many agents it has | 0, 1, 2 | [swarms.md](../guides/swarms.md) |
| `swarm add` | `NAME --swarm SWARM [--role ROLE]` | puts an agent in a swarm and takes it out of any other | 0, 1, 2 | [swarms.md](../guides/swarms.md) |
| `swarm remove` | `NAME` | takes an agent out of its swarm | 0, 1, 2 | [swarms.md](../guides/swarms.md) |
| `swarm role` | `NAME --role ROLE` | changes an agent's role in its swarm | 0, 1, 2 | [swarms.md](../guides/swarms.md) |
| `swarm assign` | `NAME [--reviewer NAME] [--tester NAME] [--no-reviewer] [--no-tester]` | names the members that review and test an agent's work | 0, 1, 2 | [swarms.md](../guides/swarms.md) |

Each `swarm` action changes this home's record only: no agent starts, stops or is told.
`swarm` also takes `--host NAME`, `--home NAME` and `--json`.

## Licensing and updates

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `license activate` | `[--label TEXT] [--accept-terms VERSION]` | takes one seat for this computer; the key is asked for without echo or piped in, never an argument | 0, 1, 2 | [licensing.md](../guides/licensing.md) |
| `license trial` | `[--label TEXT] [--accept-terms VERSION]` | starts this computer's trial, one per computer | 0, 1, 2 | [licensing.md](../guides/licensing.md) |
| `license status` | `[--refresh]` | shows the plan, the seats and the day the term ends; `--refresh` asks the license server first | 0, 1, 2 | [licensing.md](../guides/licensing.md) |
| `license activations` | `[--release ID]` | lists the computers that hold a seat; `--release ID` frees one | 0, 1, 2 | [licensing.md](../guides/licensing.md) |
| `license deactivate` | none | gives this computer's seat back | 0, 1, 2 | [licensing.md](../guides/licensing.md) |
| `update` | `[--check]` | gets the newest Dockingbird with Claude Code and Codex; with agents running it stages the new version and switches when they end | 0, 1, 2 | [updates.md](../guides/updates.md) |
| `pin` | `TOOL VERSION`, `--clear TOOL` | runs one version of Claude Code or Codex, or follows the latest again; writes `versions.toml` | 0, 1, 2 | [updates.md](../guides/updates.md) |
| `clean` | `[NAME ...] [--all] [--yes]` | frees disk; with names, deletes those stopped agents; `--all` removes everything Dockingbird made after you type `delete` | 0, 1, 2 | [clean-and-uninstall.md](../guides/clean-and-uninstall.md) |
| `completion` | `SHELL`, `--install [SHELL]` | prints the completion script for `zsh`, `bash` or `fish`, or installs it | 0, 1, 2 | [install.md](../getting-started/install.md) |

## Hosts and fleet

The scheduler's commands read your org login first; [org-file.md](files/org-file.md) holds it.

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `fleet probe` | `[--json] [--disk]` | reads this computer and its Docker; changes nothing | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet read-home` | `[--json]` | reads this home's numbers and fixed words | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet scrape` | `[--json]` | reads this home's metrics | 0, 1, 2 | [metrics.md](../guides/metrics.md) |
| `fleet hosts` | `[--json]` | lists the hosts of `hosts.toml` | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet agents` | `[--json] [--host NAME]` | lists every agent on every host | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet attach` | `[--host NAME] --container ID` | opens a remote agent's screen; the container id comes from `fleet agents --json` | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet hosts set` | `NAME --ssh DEST [--path PATH] [--home HOME] [--docker-host URL]`, `NAME --gcloud VM --zone ZONE --project PROJECT` | adds or updates a host in `hosts.toml` after reading it | 0, 1, 2 | [hosts.md](../guides/hosts.md) |
| `fleet hosts rename` | `OLD NEW` | renames a host in `hosts.toml` | 0, 1, 2, 69, 78 | [hosts.md](../guides/hosts.md) |
| `fleet hosts forget` | `NAME` | removes a host from `hosts.toml` | 0, 1, 2, 69, 78 | [hosts.md](../guides/hosts.md) |
| `fleet hosts add` | `NAME --os mac or linux --cores N --memory SIZE --line FIGURE=BOUND,CLEAR... [--agent-cap N] [--rank N] [--lease-headroom CORES,SIZE] [--no-swarms] [--power gcloud]` | adds a host to the pool | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet hosts policy` | `NAME [--takes-swarms yes or no] [--agent-cap N] [--rank N] [--line FIGURE=BOUND,CLEAR]...` | changes a pool host's policy | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet hosts drain`, `undrain`, `remove` | `NAME` | drains a pool host so it takes no new work, undrains it, or removes it from the pool | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet describe` | `NAME or FOLDER or FILE [--project SLUG]` | prints a swarm definition's parameters and settable fields as JSON | 0, 1, 2 | [swarms.md](../guides/swarms.md) |
| `fleet submit` | `NAME or FOLDER or FILE [--set KEY=VALUE]... [--values FILE] [--key KEY] [--project SLUG]` | checks a swarm definition and queues it | 0, 1, 2, 69, 77, 78 | [swarms.md](../guides/swarms.md) |
| `fleet run` | `--cores N --memory SIZE --bound TIME [--wait TIME] [--hosts H,...] [--project SLUG] [--kind KIND --exclusive] -- CMD...` | leases capacity and runs a command under the lease | the command's own, 1, 2, 77, 78, 124 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet queue` | `[--host NAME] [--metrics]` | shows each host and workload | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet why`, `ledger`, `release`, `pause`, `resume`, `cancel`, `done` | `ID` | explains why a workload waits, shows its ledger, releases it, pauses it, resumes it, cancels it, or marks it done | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet hold` | `ID --reason TEXT` | holds a workload | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet set` | `ID --priority P0 to P3` | changes a workload's priority | 0, 1, 2, 69, 78 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet retire`, `fleet replace` | `ID NAME [--fresh] [--reason TEXT]` | retires or replaces an agent of a running swarm; `--fresh` is for replace | 0, 1, 2, 69, 78 | [swarms.md](../guides/swarms.md) |
| `fleet add` | `ID ROLE [--count N] [--reason TEXT]` | adds agents of a role to a running swarm, up to the role's `max` | 0, 1, 2, 69, 78 | [swarms.md](../guides/swarms.md) |
| `fleet assign` | `ID NAME [--reviewer R] [--tester T] [--no-reviewer] [--no-tester]` | changes who reviews and tests an agent of a running swarm | 0, 1, 2, 69, 78 | [swarms.md](../guides/swarms.md) |
| `fleet prune` | `ID --merged SHA [--reason TEXT]` | prunes a swarm's agents after their commits merged | 0, 1, 2, 69, 78 | [swarms.md](../guides/swarms.md) |
| `fleet update` | `[--release V] [--host NAME]` | moves the pool's hosts to a release, one after another, in the pool's order | 0, 1, 2, 69, 77, 78 | [updates.md](../guides/updates.md) |
| `fleet worker` | `--host NAME` | runs a host's worker, a long-running service under the machine's service manager | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `fleet admitter` | none | runs the admitter, a long-running service under the machine's service manager | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `cp init` | `--hub-address IPV4` | makes this home the control plane; refused while agents run here | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `cp token` | `--host LABEL --platform P` | adds a computer and prints the join bundle once; P is `macos` or `linux` | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `cp status` | none | lists the computers, their versions, their fleet inboxes and when each was last heard from | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `cp remove` | `LABEL` | takes a computer out at once | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `cp off` | none | makes this home a plain home again once no computer is in the fleet | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `node join` | none | joins this computer to the fleet with the bundle read from standard input | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `node leave` | none | leaves the fleet once no agent here still uses it | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `org login` | `HOST[:PORT] --as KIND --role ROLE [--database NAME] [--project SLUG] [--password-stdin] [--replace]`, `--from-fleet-toml [PATH] --as KIND [--yes]` | signs this computer in to your organisation's store; KIND is `user`, `worker` or `admitter`; writes `org.toml` and `~/.pgpass` | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `org status` | none | shows the login and connects once as `user` | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `org logout` | `[--as KIND]` | takes the login away, or one kind's | 0, 1, 2 | [team-fleet.md](../guides/team-fleet.md) |
| `org create` | none | makes the store, or brings it to this release; admin only | 0, 1, 2, 69, 77, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `org projects` | `[add, set or remove SLUG] [--name TEXT] [--url URL] [--branch NAME]` | lists or changes the store's projects; admin only | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `org roles` | `[set ROLE --harness H --model M [--effort E]]`, `[unset ROLE --harness H]` | lists or changes the model and effort of each kind of role; admin only | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `org people` | `[add ROLE --account ACCOUNT]`, `[remove ROLE]` | lists or changes the store's persons; admin only | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `org members` | `[--project SLUG]`, `[add or remove ROLE --project SLUG]` | lists or changes who is a member of which project; admin only | 0, 1, 2, 69, 78 | [team-fleet.md](../guides/team-fleet.md) |
| `work status` | `[--area AREA] [--status STATUS] [--priority P] [--all]` | prints the items in work, by priority, then ETA, then id; `--all` adds the backlog | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work show` | `ID` | prints one item's fields, then its events, newest first | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work search` | `TEXT` | prints the best 50 hits over items, events, agents, requests and answers whose words match | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work needs-you` | none | prints the items waiting on you, each with the ask it waits on | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work check` | none | prints a dependency cycle, an agent with no end on an archived item, or a request open on an archived item; exits 1 when it prints any | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work agents` | none | prints the agents that have not ended, each `working` or `past its ETA` | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work stamp` | none | prints this computer's local time as `YYYY-MM-DD HH:MM ZONE` | 0, 1, 2 | [work-queue.md](../guides/work-queue.md) |
| `work new` | `ID --title TEXT --area AREA --priority P --owner OWNER [--agent NAME] [--status STATUS] [--kind KIND] [--project SLUG] [--observed-at SHA] [--ask TEXT] [--now TEXT] [--depends-on ID,...] [--links LINK,...] [--deadline DATE]` | makes an item, in the backlog and as a feature unless `--status` or `--kind` says otherwise | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work log` | `ITEM --kind KIND --text TEXT [--pr N,...] [--agent NAME] [--stage STAGE] [--sha SHA] [--usd AMOUNT] [--ago MINUTES]` | adds one event to an item's log; KIND is `log`, `merge`, `review`, `launch` or `handback` | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work set` | `ITEM FIELD VALUE [--count N --total N --unit UNIT]` | changes one field of an item and records the change as an event | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work eta` | `ITEM --in DURATION --kind measured or estimate` | sets an item's ETA that long from now; a DURATION is `45m`, `2h`, `1h30m` or `2d` | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work agent start` | `NAME --task TEXT --kind KIND --model MODEL --effort EFFORT [--item ID] [--pr N] [--workload ID] [--eta DURATION]` | records an agent that has started | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work agent eta` | `NAME --eta DURATION [--why TEXT]` | moves a running agent's ETA, keeping the reason | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work agent done` | `NAME --outcome OUTCOME [--result TEXT]` | records an agent's end; OUTCOME is `done`, `partial`, `blocked` or `stopped` | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work requests` | `[--all]` | prints the open requests; `--all` adds the answered ones | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work request show` | `N` | prints one request with its body and each answer | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work request new` | `--from NAME --kind KIND --title TEXT [--to NAME] [--item ID] [--priority P] [--observed-at SHA] (--text TEXT or --file PATH)` | files a request and prints its number | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work request info` | `N --text TEXT` | adds the requester's own word to a request that waits for more information | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `work respond` | `N --decision DECISION [--item ID] (--text TEXT or --file PATH)` | answers a request | 0, 1, 2, 69, 78 | [work-queue.md](../guides/work-queue.md) |
| `inspect swarm` | `[--swarm NAME] [--roster] [--host NAME] [--home NAME] [--json]` | reads this home's agents and, for every pair, whether one may message the other; reads only, and it reads homes of other versions | 0, 1, 2 | [updates.md](../guides/updates.md) |

Every `work` action takes `--json`, which prints one JSON line for each line it prints, and `--as KIND` to connect as `user`, `worker` or `admitter`.
`fleet` takes `--as KIND` too.

## Connections and configs

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `connect` (GitHub) | `NAME --github OWNER/REPO [--key PATH or --agent] [--branch BRANCH] [--known-hosts PATH]` | lets agents fetch and push a GitHub repo without seeing your key | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (folder) | `NAME --folder PATH` | gives agents a folder of this computer, read-only unless its config says `write` | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (database) | `NAME --database URL [--password] [--writes]` | gives agents a read-only database, or writes through the broker with `--writes`; they never see its password | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (service) | `NAME --service FILE` | registers a program of this computer and its typed arguments, run by `serve` | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (MCP) | `NAME --mcp URL` | registers a streamable-HTTP MCP server for the swarm roles that list `NAME` | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (browser) | `NAME --browser BROWSER` | lends your `chrome`, `firefox` or `safari` while `serve` runs | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (vault) | `NAME --vault gopass [--store NAME] --login ALIAS ORIGIN USERNAME... [--totp ALIAS...]` | connects a gopass store whose logins `serve` types into the agent's browser | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connect` (grants) | `[NAME] --config FILE [--to AGENT --until ISO]`, `NAME --to-role ROLE --until ISO`, `NAME --revoke --role ROLE [--swarm KEY]` | grants a connection to an agent or a swarm role until a time, or revokes a role's grant | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `connections` | `[NAME] [--release]` | lists connections and who may use them; `--release` frees a push whose result is unknown | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `revoke` | `NAME --to AGENT` | takes a connection from one agent | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `disconnect` | `NAME` | disables a connection and removes Dockingbird's copy of its key | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `serve` | `NAME [--once]`, `--all [--once]`, `--unit` | runs a service, browser or vault connection here as you; `--unit` prints the launchd or systemd unit that runs `serve --all` at login | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `watch` | `NAME [--no-open]` | shows an agent's browser in your VNC viewer and lets you take over its screen | 0, 1, 2 | [connections.md](../guides/connections.md) |
| `config add` | `PATH [--name NAME]` | copies a config into Dockingbird so its commands work in every repo | 0, 1, 2 | [your-own-commands.md](../guides/your-own-commands.md) |
| `config list` | none | lists each config, this repo's first, and each one that cannot run | 0, 1, 2 | [your-own-commands.md](../guides/your-own-commands.md) |
| `config remove` | `NAME` | removes an added config's copy | 0, 1, 2 | [your-own-commands.md](../guides/your-own-commands.md) |
| your own command | `["TASK"]` and the options of `start` but `--command` | a command a config adds, such as `dockingbird review "task"`, which is `start --command review`; Dockingbird ships none | 0, 1, 2 | [your-own-commands.md](../guides/your-own-commands.md) |

## MCP and GUI

| Command | Arguments | What it does | Exit | Guide |
|---|---|---|---|---|
| `mcp install` | `[--show] [--connected NAME] [--check]` | connects Dockingbird's tools to each Claude Code and Codex on your path and prints how to undo it | 0, 1, 2 | [mcp-server.md](../guides/mcp-server.md) |
| `mcp` | none | the stdio server your harness starts; you never run it yourself; tools in [mcp.md](integration/mcp.md) | 0, 1, 2 | [mcp-server.md](../guides/mcp-server.md) |
| `ui` | `[stop] [--install]` | opens the Dockingbird GUI over every agent, stops its server, or installs it; not yet available | 0, 1, 2 | [gui.md](../guides/gui.md) |

The GUI binary is not yet available, so `ui` and `ui --install` cannot open a GUI today.
