---
title: Dockingbird changes from v0.7.0 to v0.15.28
summary: One page of the changes a customer sees in each release from v0.7.0 to v0.15.28, newest first, with the upgrade step of each release that needs one.
audience: daily
commands:
  - dockingbird update
  - dockingbird init
  - dockingbird org create
  - dockingbird org login
  - dockingbird fleet update
  - dockingbird fleet submit
  - dockingbird fleet describe
  - dockingbird fleet release
  - dockingbird fleet retire
  - dockingbird fleet replace
  - dockingbird fleet queue
  - dockingbird fleet where
  - dockingbird homes
  - dockingbird send
  - dockingbird expect
  - dockingbird set
  - dockingbird connect
  - dockingbird serve
  - dockingbird cp init
  - dockingbird node join
  - dockingbird work
  - dockingbird license
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Dockingbird changes from v0.7.0 to v0.15.28

This page lists what changed for you in each of the 42 releases from v0.7.0 to v0.15.28, newest first: new commands and flags, changed defaults, renamed or removed keys, and the upgrade step when a release needs one. [v0.6.5](v0.6.5.md) has its own page and [the next release's draft](next.md) lists what comes after v0.15.28. [Updates](../guides/updates.md) says how to run `dockingbird update`, and [the commands reference](../reference/commands.md) has every flag.

## Before you jump several releases

- Each kernel migration that a home's `dockingbird update` applies cannot be undone. A home that took it cannot run an older coordinator image (`SCHEMA_AHEAD`). The PostgreSQL move from 17 to 18.6 in v0.15.4 cannot go back either.
- A release that adds a fleet-store migration needs `dockingbird org create`, run as the owner of the `fleet` schema's tables, before the workers move. The migrations and their releases: `0006` and `0007` in v0.8.0, `0008` in v0.12.0, `0009` in v0.14.0, `0010` in v0.15.0, `0011` in v0.15.2, `0012` in v0.15.4, `0013` in v0.15.6 and `0014` in v0.15.14. The usual order is `org create`, the workers, then the admitter. v0.15.4 moves the admitter first.
- A release that names a Dockingbird GUI version installs it with `dockingbird update`. A GUI that is already open keeps its version until its server stops. See [the GUI](../guides/gui.md).

## v0.15.28

- A swarm definition's `[[role]]` takes `branch = "SUFFIX"`: its agents work on the task branch `<source branch>-SUFFIX` in a clone of their own. A role whose `reviews` or `tests` names a role on another branch is refused `branch-mismatch`. An earlier release's `fleet submit` refuses the key. See [the swarm definition](../reference/files/swarm-definition.md).
- `fleet queue` prints `held: NAME: REASON` for each agent whose start was refused, and `fleet why` says `fleet replace` or `fleet retire` frees its slot.
- `dockingbird -h` and each command's help screen have no line cap.

## v0.15.27

- `dockingbird-find defn NAME...` takes several names in one call. It exits 0 when it found any definition and 1 when it found none.
- Every `dockingbird update` ends the home's agents whose containers stopped by themselves, unless a hand-over is open. See [Updates](../guides/updates.md).
- A start in a home whose swarm record holds 64 swarms drops the swarms none of whose agents the home keeps. `dockingbird swarm add NAME --swarm LABEL --role ROLE` records a swarm that started unrecorded.
- Dockingbird ends each message it pastes into a screen-form Claude Code agent with one space, so a last word that opens a typeahead list (an emoji word, an `@` name) is submitted as sent.

## v0.15.26

- `dockingbird update` leaves a stopped home stopped and ends the home's agents whose containers stopped by themselves, saving their logs under `logs/agents/`.
- The fleet worker stops by name an agent that stops itself when its swarm ends, pauses or retires it, so its container goes at once.
- `dockingbird status` shows a retried turn as working while it runs.
- `dockingbird work status --agent NAME` and `--owner KIND` filter the list. See [the work queue](../guides/work-queue.md).

## v0.15.25

- `fleet prune` removes the swarm's clone under the engine home's `clones` folder once every agent of that host is cleaned, unless another live workload works in it. `fleet why` of a finished swarm names its last prune.
- `dockingbird serve` and `serve --all` move to the home's new release by themselves, between two requests. A serve started before this release stops once, and its unit starts it again.
- A failed switch at idle names its cause, for example `DOCKER_NOT_ANSWERING`. See [the message catalogue](../troubleshooting.md).
- `cp init` and `node join` record the home's program, so the fleet worker reads those homes with their own program.

## v0.15.24

- `fleet retire`, `fleet replace --fresh` and `fleet replace` of an idle agent wait only for a request the agent has not taken yet. See [swarms](../guides/swarms.md).
- A `question`, and a message sent with `requires_ack` (`send --requires-ack`), stays open until its target replies or acknowledges. The target sees it again on the bus's reminder schedule and its sender is told once at the deadline. `--reply-required` does the same for a `task_request`, `handoff` or `review_request`.
- `dockingbird expect KIND --from NAME --prefix TEXT --within SECONDS` registers a message you expect and alerts you once when none arrives. `expect --list` (with `--closed`) lists them and `expect --withdraw ID` withdraws one. Agents use `bus_expect`.
- Dockingbird types a pasted message's Enter into a screen agent 1 second after the paste and retries it every 3 seconds, up to twice.
- Upgrade step: each home's `update` applies kernel migration `0034_delivery_guarantee`. See [agents and the bus](../concepts/agents-and-the-bus.md) and [delegating tasks](../guides/delegating-tasks.md).

## v0.15.23

- A `browser_login` sign-in waits up to 30 seconds for a login form that the page draws after it loads.

## v0.15.22

- `browser_login` with a login and an address alone finds the username, password, code and submit fields. `browser_read` lists a page's fields. See [secrets and the vault](../guides/secrets-vault.md).
- `dockingbird claude`, `codex` and the fleet's agent starts find their branch's repository on a home with more than 100 registered repositories.
- `dockingbird-find` prints a definition by name (`defn NAME`), a Markdown section or file outline (`section FILE [HEADING]`) or the top sections for some words (`docs WORDS`, after `dockingbird-find index`). Every agent container carries it.
- Upgrade step: this release changes the agent base, so `dockingbird update` builds a new one.

## v0.15.21

- A Claude agent in `models` or `allowlist` egress starts when its home's Claude login goes through a gateway named by a host name. Its proxy admits that host on the gateway's port alone. A gateway named by an IP address is still refused at start. See [egress and network](../guides/egress-and-network.md).
- Changed default: an agent with a fallback tool moves to it only after `refusal`. `rate_limit`, `network`, `auth`, `billing` and `server` retry on the agent's own tool after `retry_wait` (5 minutes), at most `retry_max` (3) times. To restore a move, set `on.CLASS = "fallback"` in the `[fallback]` table. See [your own commands](../guides/your-own-commands.md).
- The shipped roles set `compact_at`: `coordinator` and `hands` at 300k tokens, `implementer`, `reviewer`, `tester` and `reader` at 500k.
- A definition's `[params]` expand in `key`, `priority` and `[source]`. `fleet describe` prints a parameter with no value as `"required": true`. See [swarm parameters](../guides/swarm-parameters.md).
- The `dockingbird-swarm` skill ships a standard definition, `.agents/skills/dockingbird-swarm/library/standard`, with parameters `source-repository`, `source-branch`, `implementers` (2, 1 to 12), `reviewers` (1, 1 to 4), `testers` (1, 1 to 3), `harness` and `plan`. Upgrade step: run `dockingbird init` in the checkout.

## v0.15.20

- Both code prunes (a roll's end and `clean`) keep the code key of every container the home lists, so a browser sidecar or switched agent no longer meets `LAUNCH_CODE_MISSING` after a roll.
- `dockingbird COMMAND --as NAME --fallback` and the engine's pickups move an agent to its fallback tool, at most three pickups per agent.
- `dockingbird status` names an agent whose browser or proxy runs an older release (`STATUS_SIDECAR_BEHIND`). Run `dockingbird stop NAME`, then start the agent again, to take the new one.

## v0.15.19

- `dockingbird fleet release ID` starts a swarm that held before any agent started (a `skills_refused` hold on a new branch, for example), instead of holding it again `no_checkout`.
- `browser_login` signs in at a single sign-on page that keys each step in its address.

## v0.15.18

- A role whose `fallback` table sets `placement = "require-login"` runs only in a home signed in to the role's tool and its fallback tool. `fleet queue` lists each home's sign-in words and `fleet why` names the missing one. Sign in with `dockingbird login claude` or `dockingbird login codex`.
- A turn that a safety system refused is classed `refusal`. A hand-started agent that asked to move is picked up by a watcher, and `status` names the command `dockingbird start --as NAME --fallback`.
- A fleet event over the store's 4096-byte bound (a hold on 43 or more hosts) no longer fails every admitter pass. `fleet why` says how many hosts the record left out.
- `.dockingbird/skills.lock` is format 2 with no `release` line. Upgrade step: run `dockingbird init` once, or `init --check` calls a format-1 lock stale.

## v0.15.17

- `dockingbird status` reads a bus agent with no turn run and no task waiting as `idle`, a fresh one included. Before, it read `working` for good and the scheduler never offered it work.

## v0.15.16

- A reviewer's `approved SHA by AUTHOR: TASK` line is recorded whatever author it names. A line the engine cannot record gets one status message back naming the problem.
- `dockingbird inbox --all --since TIME` lists a home's rows sent since TIME, read or not.

## v0.15.15

- The Dockingbird GUI 0.1.20 shows its Claude, Codex and Dockingbird tiles as images inside tmux with `allow-passthrough on`. A terminal without Kitty graphics, or tmux with it off, keeps the text tiles. `dockingbird update` installs it over 0.1.19. See [the GUI](../guides/gui.md).

## v0.15.14

- A swarm role and a library role take a fallback table: `[role.fallback]` in a definition, or `fleet submit --set ROLE.fallback.KEY=VALUE`. A moved agent is picked up by name on the fallback tool with its conversation, at most once. Upgrade step: fleet-store migration `0014_harness_fallback`. Run `dockingbird org create`, then move the workers and the admitter.
- An agent with `browser = "chrome"` and a gopass vault connection signs in with a vault login. Dockingbird types the password or code into the container's Chrome, and the agent never reads it. The browser refuses the agent's commands for at most 300 seconds meanwhile. See [secrets and the vault](../guides/secrets-vault.md).
- `fleet retire ID NAME` retires the agent at the first tick that finds it idle with no question open and no request it has not taken yet. `fleet replace ID NAME` starts it again at the worker's next pass on the same terms. A busy agent's ask is refused and dropped, so run the command again. A plain replace of a failed or crashed agent proceeds whatever is open. See [swarms](../guides/swarms.md).
- `dockingbird inbox` keeps its row numbers and read marks across the seven-day credential renewal.
- Upgrade step: this release changes the agent image's launcher, so a home's update builds a new agent base.

## v0.15.13

- The Dockingbird GUI 0.1.19 draws its Claude and Codex tiles as text inside tmux, where image tiles landed out of place with `allow-passthrough on`. `dockingbird update` installs it over 0.1.18. See [the GUI](../guides/gui.md).

## v0.15.12

- `dockingbird set NAME --skills PATHS` adds skills to a running agent, and its tool lists them from its next turn. `--skills` beside another `set` change is refused (`OPTIONS_NOT_BOTH`). See [skills](../guides/skills.md).
- Every start attempt of a swarm in the worker's own clone, a `fleet release ID` after a hold included, fetches and fast-forwards that clone first, so a fix you pushed after the hold reaches the start.

## v0.15.11

- `dockingbird send` takes `--all`, `--swarm SWARM` and `--role ROLE`, and `bus_send` takes `all`, `swarm` and `role`. Each recipient passes the `send_to` check. `RECIPIENTS_MAX` defaults to 0, which bounds nothing.
- Upgrade step: the minimum of `DOCKINGBIRD_MCP_MAX_CHARS` rises from 1200 to 1350. A home that sets it between those values refuses to start. Raise it to at least 1350 or unset it.
- An agent starts from your own Claude Code `settings.json` or Codex `config.toml`: `--harness-config PATH` at a start, `harness_config` in a config or on a role, and `dockingbird set NAME --harness-config PATH` on a running agent. Dockingbird's keys win. The file holds at most 262,144 bytes. See [your own commands](../guides/your-own-commands.md).
- A swarm `[[role]]` and a library role take `skills`. A start whose clone lacks a path holds the swarm `skills_refused` until you push the fix and run `fleet release ID`. See [skills](../guides/skills.md).
- A failed turn names its class, as `turn 3 failed (rate_limit)`: `rate_limit`, `usage_limit`, `auth`, `billing`, `server`, `network`, `invalid_request`, `context`, `cap`, `exited` or `other`. `--json` carries `last_turn_class`.
- A config's `[fallback]` table sets each class's rule (`retry`, `retry-then-fallback`, `fallback` or `report`). `start` takes `--fallback`, `--fallback-model`, `--fallback-effort` and `--fallback-placement`. A `usage_limit` retries after 1, 5 and 15 minutes, then every 30 minutes for 24 hours. An agent moves at most once, and not to a tool the home cannot sign in (`FALLBACK_NO_LOGIN`). Upgrade step: each home's `update` applies kernel migration `0033_harness_fallback`.
- A Claude turn that failed because the model API was unreachable runs again after 60 seconds, and again after each try that ends the same way.
- `dockingbird serve` keeps serving through an update's coordinator swap and waits up to 600 seconds. A longer update stops it with exit 1 (`SERVE_UPDATE_TOO_LONG`).
- An update to the same version that changes the base image replaces Dockingbird on the new base. An update whose new Dockingbird stops at its start fails at once and says what it printed.

## v0.15.10

- An agent gets skills from a config's `[skills]` table (`path`, and `into` as `both`, `claude` or `agents`) or from `--skills PATHS` on `claude`, `codex`, `start` and every config's command. A repository config's skills apply only in a checkout you have not marked untrusted. See [skills](../guides/skills.md).
- `dockingbird update` installs each release into its own folder, `~/.local/share/dockingbird/programs/VERSION/`, and moves your `dockingbird` command with one rename, so a command started during an update runs whole. `clean` removes program folders no home names. A `uv tool upgrade dockingbird` that gets anything new puts the command back on uv's own folder until your next `dockingbird update`. See [home layout](../reference/files/home-layout.md).
- On a control-plane home, `dockingbird fleet scrape` prints eight `dockingbird_relay_*` families: answered, refused and dropped requests and seconds per request. See [metrics](../reference/metrics.md).
- Upgrade step: this release changes the agent image's base, so a home's update builds a new agent base.

## v0.15.9

- A coordinator whose version label cannot be read is refused in words (`VERSION_UNREADABLE`) before any hand-off. The way out is `dockingbird stop`, then `dockingbird update`.

## v0.15.8

- `dockingbird fleet hosts policy NAME --lease-headroom CORES,SIZE` sets a host's lease headroom without re-adding the host.
- `dockingbird fleet run --priority P` (P0 to P3) records the lease with that priority. `fleet run` reads its pending lease every 5 seconds instead of 30.

## v0.15.7

- The fleet engine retires a builder whose last `turn N` hand-back opens with `status: done`, and stops by name an idle agent asked to stop or retire that has not stopped after 600 seconds.

## v0.15.6

- Every agent start passes a host guard. A host whose latest figures read a gate line red refuses with `HOST_OVERLOADED`, in its `STALE` form while the worker's `guard.json` is older than 180 seconds. A home runs at most 24 agents, and the next start refuses with `HOST_AGENT_CAP`. `dockingbird start --wait TIME` waits for room. `fleet host-history` shows a host's recent samples. See [limits](../reference/limits.md) and [the fleet scheduler](../guides/fleet-scheduler.md).
- Upgrade step: fleet-store migration `0013_host_guard`. Run `dockingbird org create` before the workers move.
- The cap of 100 registered repositories is gone. `dockingbird native repo release --repository R` drops one registration. A start refused for a reason no other message covers says `REPO_LINK_REFUSED`. Kernel migration `0032_repository_release` is applied by each home's update and cannot go back.
- `dockingbird fleet admitter` keeps admitting when its metrics address is in use (`FLEET_METRICS_UNSERVED`). `--metrics-port N` picks the port: 0 asks for a free one, and 9107 stays the default.

## v0.15.5

- A pool computer without a Codex login of its own runs Codex agents. The worker of the computer that has the login pushes a mirror form, with the refresh token left out, to each host whose `hosts.toml` entry says `login_push = ["codex"]`, within 30 seconds of a change. `status` shows when a pushed copy expires, and an expired copy is refused. See [the hosts file](../reference/files/hosts-file.md).
- A screen hook no longer ends a prompt the agent took as a false `NOT_TAKEN` failure under load. `dockingbird clean` keeps the code every running agent uses.

## v0.15.4

- Each home's PostgreSQL moves from 17 to 18.6. Upgrade step: the home's first start after the update upgrades its database in place (a few seconds) and keeps the old one as `pg.old-17-TIME`. The step cannot go back, and `status` says so if the new Dockingbird then does not come up.
- `dockingbird status` and the bus commands (`send`, `inbox`, `read`, `wait`, `results`) answer several times faster. `status` took six to seven seconds on a home with 21 workspaces.
- A role takes `context = "fresh"`: each task delivery starts a new conversation. The default is `"kept"`. A v0.15.3 submitter refuses the key, so move the admitter and every pool worker first.
- A definition's `[placement]` takes `spread = true`: the engine places the swarm on one host when it fits, and otherwise one role group at a time. `dockingbird fleet where ID` names where each agent runs.
- Upgrade step: fleet-store migration `0012_agent_placement`, admitter first. Run `dockingbird org create`, restart the admitter at this release, then move the workers and the submitters. Run no `fleet submit` between `org create` and the admitter's restart.

## v0.15.3

- A session config's `context = "fresh"` starts every task delivery in a new conversation (a role takes it from v0.15.4).
- `dockingbird node join` retries its enrolment while the computer's fleet link has not reached the hub.
- Kernel migration `0031_live_claim_groups_by_claim_key` keeps `status` fast on a home whose PostgreSQL never gathered statistics for its small tables. A home updated to it cannot run an older coordinator image (`SCHEMA_AHEAD`).

## v0.15.2

- The organisation's work queue lives in the fleet database, in the schema `work`. `dockingbird work` reads and writes it through the org login, with `--json` on every action. See [the work queue](../guides/work-queue.md).
- Upgrade step: fleet-store migration `0011_work_queue`. Run `dockingbird org create` once as the owner of the `fleet` schema's tables, then restart the workers, then the admitter. A worker or admitter of this release refuses to start until the store carries it (`FLEET_STORE_BEHIND`).
- `dockingbird update` on a home whose Dockingbird stopped itself idle swaps the stopped coordinator for the new one, instead of failing with "Dockingbird didn't start properly."
- The control plane's home runs the hub on that computer's loopback only, binds each member's calls to that member, and keeps only each computer's public key and its token's digest. A member's label is reserved: no other agent of the project may be named `LABEL-...`. The operator guide gains the steps for joining a computer and the one `tailscale serve` line. See [the control plane](../concepts/control-plane.md) and [Tailscale](../guides/tailscale.md).

## v0.15.1

- A bus agent whose config workspace is `scratch` starts with a screen. Open it with `dockingbird codex --as NAME` (`dockingbird claude --as NAME` for Claude). An agent started before this release keeps its form until you stop it and pick it up again.
- An agent's open question survives a Dockingbird restart, and a question asked during a restart is recorded once it ends.
- After an update, an agent that could not take the new version is named with its fix: run `dockingbird update` again.
- The five library role rules and six shipped agent definitions name the kind of each message an agent sends. `dockingbird init` replaces an unedited copy and keeps an edited one unless you add `--force`.

## v0.15.0

- A swarm definition kept at `.dockingbird/swarms/NAME/swarm.toml` is submitted by name from anywhere in the checkout: `dockingbird fleet submit NAME`. `--set KEY=VALUE` (repeatable) gives a `[params]` value, a role's setting (`grader.count=6`) or a helper's (`grader.helper.max=4`). `--values FILE` gives the same as JSON, and `--key KEY` names the swarm. `fleet submit` prints every refusal as `refused: FIELD: RULE`, and `dockingbird fleet describe NAME` prints every settable field as JSON. See [swarm parameters](../guides/swarm-parameters.md).
- A role takes its settings from a library: `use = "NAME"` names `.dockingbird/roles/NAME.toml`, and `use = "dockingbird/NAME"` one of the five shipped roles (`coordinator`, `implementer`, `reviewer`, `tester`, `reader`), which `dockingbird init` copies in. A role's `send_to` names whom its agents may message, and the bus refuses any other send (`FORBIDDEN`, reason `NOT_IN_SEND_RULES`). See [the swarm definition](../reference/files/swarm-definition.md) and [roles and connections](../reference/files/roles-and-connections.md).
- A role names the connections its agents get at start (`connections`). `dockingbird connect NAME --mcp URL` adds an MCP server, and `--writes` beside `--database` lets the broker write to a database. `connect NAME --revoke --role ROLE` takes a connection from a role's running agents at their next request, and `--to-role ROLE --until ISO` gives it back. `dockingbird serve --all` serves every connection of a home in one process, and `serve --unit` prints its service unit. See [connections](../guides/connections.md).
- A swarm whose roles all use `workspace = "scratch"` needs no `[source]`. `fleet submit` refuses a repository tool on a scratch role, and an `allow` beside an `egress` other than `allowlist`, with the rule `conflict`.
- `dockingbird cp init --hub-address IPV4` turns a home into the fleet's control plane. `cp token --host LABEL --platform macos|linux` prints the join bundle once, and `dockingbird node join` on that computer's home reads it from standard input. `cp status` lists the computers, `cp remove LABEL` takes one out at once, `node leave` leaves, and `cp off` returns the home to a plain home once every computer is removed. The relay (container `cp-relay`) serves the fleet session on the coordinator's own socket `cp.sock`, and each agent on a joined computer gets a fleet inbox beside its own through the fleet-link container. See [the control plane](../concepts/control-plane.md) and [join a computer to a control plane](../../examples/join-a-computer-to-a-control-plane/README.md).
- The Dockingbird GUI 0.1.18 opens the log of a running agent that has no screen (`screen: none` in `dockingbird --json status`, such as a Codex bus agent) when you click or tap its row, with a line to send it messages (`dockingbird fleet attach --container ID`). `dockingbird update` installs it over 0.1.17. See [the GUI](../guides/gui.md).
- `dockingbird status` names the agents an update waits for.
- Upgrade step: each home's `update` applies kernel migration `0030_swarm_roles`, and `dockingbird org create` applies fleet-store migration `0010_role_config`. Every definition valid before still submits and starts as it did.

## v0.14.0

- `dockingbird update` adds rolling updates and no longer waits for agents to end. The new release takes over at once, and each bus agent moves to it at its next stopping point between turns, in the same container and session, with its conversation resumed. A terminal agent keeps its code until its terminal closes. Claims survive the short restart. See [Updates](../guides/updates.md).
- An update that changes the engine or an agent's base image moves each running agent to a fresh container that continues the same session. `update` names what it moves and refuses what it cannot roll, with the reason, and `status` lists the agents it could not ask to move.
- `dockingbird set NAME --switch-code KEY` asks a running agent to take code KEY at its next stopping point, and `--switch-code -` takes the ask back. `status` shows each agent's code, version and pending switch.
- The image no longer holds Dockingbird's own code. Each release's code goes into a shared code store, so an update needs a new image only when the system, the tools or the Python packages change.
- Dockingbird reads what its next release writes: an unknown field is ignored, and a word from a newer release holds that one read (`CONTRACT_AHEAD`) until the reader updates. A home's coordinator and agents can move one at a time.
- `dockingbird fleet update` moves the fleet's computers to a release one after another, in the pool's order. Per computer it installs the release, updates the homes, moves the `installs/current` link, restarts the services with the host's `repoint` line from `hosts.toml`, and waits up to 10 minutes for the worker to report the release. Run again after a stop, it skips finished computers. This computer joins the pool as a `[[host]]` with `local = true`. See [team fleet](../guides/team-fleet.md) and [the hosts file](../reference/files/hosts-file.md).
- The fleet records the release each worker and the admitter run (fleet-store migration `0009_rolling_updates`). `fleet queue` and `fleet hosts` list each process with its release, and an earlier worker shows `unknown`.
- The agent image carries nats-server 2.15.1, the hub that a fleet's control plane uses. Node credentials for the control plane exist inside the coordinator container, with no host command yet.
- Upgrade step: run `dockingbird org create` as the owner of the `fleet` schema's tables, move each machine's worker and the admitter to the new release, then run `--home NAME update` from the new install for each home a worker runs.

## v0.13.0

- The agent image's Ubuntu packages come from a local pool, a folder under `~/.local/share/dockingbird/apt-pool/`, and no longer from Ubuntu's snapshot service at build time. The first build on a computer without the folder fills it, 441 MB once per snapshot, checking every file's size and sha256. Every later build reads the folder alone, even when the snapshot service is down. If the service cannot be reached during that first fill, the build stops.
- `dockingbird clean --all` also removes the home's `program` file, and a home left with only that record can be started or cleaned again.

## v0.12.0

- The fleet engine starts every agent on its role's model and effort with its task as the first turn. A bus agent whose start sends a task feeds no other message before it. An agent started this way cannot be handed back to an earlier release.
- `dockingbird status NAME` shows a `set`'s values as asked as soon as the set is written. In the screen form, `/model`, `/effort` and `/autocompact` are typed one at a time, each once the status line confirms the one before. After three tries, `status` says the tool runs another model or effort under "Needs your attention".
- A Codex agent reports what a Claude agent reports: model and effort, context and window, tokens per model and compactions, in `status`, `status --json`, `/metrics` and `fleet scrape`. Reasoning tokens are the new `result_reasoning_output_tokens`. Codex reports no cost, so those fields stay null. See [metrics](../reference/metrics.md).
- Upgrade step: two migrations, both one-way. Fleet-store `0008_sql_audit` is applied only by `dockingbird org create`: move the admin computer's install, run `org create` there at once, then move every other host and restart its worker, then restart the admitter. A worker restarted first refuses with `FLEET_STORE_BEHIND 0008_sql_audit`, and its host is marked stale after 180 seconds. Kernel `0028_sql_audit_indexes` runs at each home's `update`, and the home cannot run an older coordinator image again (`SCHEMA_AHEAD`).
- Inside an agent's container, `DOCKINGBIRD_CPUS` and the worker counts that pytest-xdist, OpenMP, cargo and Go read are set to the container's CPU limit rounded up. A value you set in the config's `[env]` stays yours.

## v0.11.1

- Upgrade step: kernel migration `0027_deliveries_target` cannot go back per home. A home updated to this release cannot run an older Dockingbird (it refuses with `SCHEMA_NOT_CURRENT`). Update each computer's command line first, then each home (a home whose swarm runs, once that swarm has ended), then the fleet install.
- `dockingbird fleet agents`, and `fleet hosts set` as it adds a host, list each swarm with a running agent: running and waiting counts, project, priority, state, roles, and who reviews and tests each agent's commits.
- `dockingbird inspect swarm --roster` lists a home's agents without deciding for every pair whether one may message the other.
- A license seat is one person who may link up to three computers. `license status` shows `Computers per seat: 3`, and `activate` and `activations` show `Computers linked: 4 of 30 (10 seats, 3 computers each)`. `activations` lists at most 80 computers, the longest unseen first. A full license refuses with exit 1 and lists the ids that `license activations --release ID` takes. Run `dockingbird license deactivate` or `clean --all` before destroying a computer, because a rebuilt one with a new identifier counts again. An unreleased one stops counting after 90 days. See [licensing](../guides/licensing.md) and [the licensing model](../concepts/licensing-model.md).
- The Dockingbird GUI 0.1.17's Swarms tab shows the swarms that run on every host, with an arrow from each agent to its reviewer and a dashed one to its tester. It has two views, `1 Topology` and `2 Configuration`, and the Permissions view is gone. A GUI that is already open keeps its version until its server stops. See [the GUI](../guides/gui.md).

## v0.11.0

- Every agent container carries ripgrep 15.2.0 (`rg`) and ast-grep 0.51.0, and the rules every agent gets say to locate a name with `rg`, outline a long file before reading it, and find a definition by structure with `ast-grep`. `dockingbird update` builds the image that carries them. An agent started from the previous image runs without them until its home is updated.

## v0.10.3

- The Dockingbird GUI 0.1.16 changes its sidebar only when you toggle it, with ` » sidebar `, `« hide` or `prefix b`, and remembers the choice for the next launch. The self-closing drawer and `pin` are gone. See [the GUI](../guides/gui.md).

## v0.10.2

- The Dockingbird GUI 0.1.15 keeps the sidebar beside the panes, never over them, and resizes the panes when it opens and closes.

## v0.10.1

- The Dockingbird GUI 0.1.14 reads any home whose coordinator answers `inspect`, whatever its Dockingbird version, and its Swarms roster lists the agents that run. The keys row names `hjkl` beside the arrows.

## v0.10.0

- `dockingbird homes` says for each home whether `dockingbird inspect` can read it and what a command from here would do. A home whose coordinator runs 0.6.2 or later is readable for inspection whatever its version. `--json` rows gain `inspectable` and `inspect_from`. See [Updates](../guides/updates.md).
- `inspect swarm` and `inspect config --agent NAME` in a home older than 0.6.2 say so and run nothing (`INSPECT_NOT_SUPPORTED`, exit 1). An answer in a newer form than this Dockingbird reads is refused (`INSPECT_SCHEMA_NEWER`, exit 1). To read it, update this computer's Dockingbird.
- `dockingbird --json inspect swarm` lists only the agents that run. Past 64 it lists the first 64 by name, sets `complete` false and adds `ROSTER_TRUNCATED`.
- `fleet queue` separates "still working", "waiting to start" (with the first hold) and "starting". `fleet why ID` of a running swarm answers the same, with the hold's figures.
- The Dockingbird GUI 0.1.13 makes the Topology's `−`, `+` and `fit` clickable, and `fit` shows the whole roster.

## v0.9.1

- The Dockingbird GUI 0.1.12 opens with its sidebar closed, as a drawer that ` » sidebar ` or `prefix b` opens over the panes. A selection copies only its pane's text. A drag over the Inbox and Swarms tabs copies, and homes are headed by name. `dockingbird update` installs it. See [the GUI](../guides/gui.md).

## v0.9.0

- `dockingbird --home NAME COMMAND` runs a command in the home `homes/NAME` under your data root, made by the first command that claims it. NAME is lowercase letters, digits and `-`. The option goes before the command and is refused with exit 2 when `DOCKINGBIRD_HOME` is also set.
- `dockingbird homes` lists a home by its name and the default home as `default`. `--json` rows gain `name`.
- The data root keeps five folders of its own: `homes/`, `clones/`, `installs/`, `cache/` and `org-db/`. `clean --all` leaves them. See [home layout](../reference/files/home-layout.md).
- A `[[home]]` or `[[host.home]]` table of `hosts.toml` names its home with `name` in place of `path`. `fleet hosts set NAME --home HOME` adds a home by name, and `--home NAME` after `--host` names a home of that host. See [the hosts file](../reference/files/hosts-file.md).
- Upgrade step: update every fleet install (each host's worker, the admitter and each submitter) before any file or definition names a home by name. An older install refuses the new form.

## v0.8.0

- The fleet database gains the `org` schema (projects, the model and effort of each kind of role, people and memberships) in migrations `0006_org` and `0007_membership`. See [the org file](../reference/files/org-file.md) and [the fleet store](../reference/files/fleet-store.md).
- Upgrade step, before any worker, admitter or submitter restarts at the new build: back up (`pg_dump -Fc`) and rehearse on a restored copy. As the cluster's superuser, run `ALTER ROLE fleet_admin CREATEROLE;` and `GRANT fleet_submitter TO fleet_admin WITH ADMIN TRUE, INHERIT FALSE, SET FALSE;`, and the same grant for each `fleet_submitter_PROJECT` group. Then run `dockingbird org create` as `fleet_admin` where it owns the `fleet` schema's tables, else `store.migrate` as the superuser through the operator guide's line. Then add the persons and memberships, move each computer's login to its person, retire the project logins, and last restart the workers and the admitter.
- `dockingbird org` manages the store, each verb run as your `user` login: `org create`, `org projects [add SLUG | set SLUG | remove SLUG]` (`--name`, `--url`, `--branch`), `org roles [set KIND --harness H --model M --effort E | unset KIND --harness H]`, `org people [add ROLE --account ACCOUNT | remove ROLE]` and `org members [--project SLUG | add | remove ROLE --project SLUG]`. A verb that changes the store is refused to a role that is no `fleet_admin` member (exit 77). A store without the `org` schema is named with `org create` (exit 78).
- A swarm definition's roles need no model or effort. `fleet submit` takes each from the role, then the project file's `[roles.KIND]`, then the store.
- A person connects as a login of their own and acts for a project as a member of its group. `fleet submit` and `fleet run` refuse a non-member, naming `dockingbird org members add PERSON --project SLUG` (exit 77).
- A `password` in `fleet.toml` is refused. A fleet command that finds one on a computer with no org login ends 78, naming `dockingbird org login --from-fleet-toml --as KIND`. Run that line on each computer with the kind its home connects as (`user`, `worker` or `admitter`).
- The swarm skill is renamed from `dockingbird-feature-pipeline` to `dockingbird-swarm`, and `dockingbird init` installs the new folder.
- `dockingbird init` registers the project in the store when the org login's `user` role is an admin. `--no-register` skips the step.

## v0.7.0

- `dockingbird init` makes any git repository ready for the agents and the fleet in one command. It writes `.dockingbird/project.toml`, `.dockingbird/rules.md`, an example swarm, the release's skills and agent definitions, and `.dockingbird/skills.lock`. Run it again after an update: it changes only what the release changed and keeps a file you edited unless you add `--force`. `init --check` changes nothing and exits 1 when the files are not the running release's. See [first run](../getting-started/first-run.md).
- The fleet's database login leaves `fleet.toml`. `dockingbird org login HOST:PORT --as user --role fleet_admin` keeps a role's password in `~/.pgpass` and the database and each kind's role in `~/.config/dockingbird/org.toml`. `org status` shows the login and `org logout` takes it away. The password is asked without echo or piped with `--password-stdin`. See [the org file](../reference/files/org-file.md).
- Upgrade step: a `password` in `fleet.toml` still works in this release and is called deprecated on every command. On each computer, run `dockingbird org login --from-fleet-toml --as KIND` (`user`, `worker` or `admitter`), which moves the login and takes the password out of the file.
- `dockingbird fleet submit` takes a definition's folder and reads its `swarm.toml`.
- A Claude Code bus agent whose model changes keeps its compact point.
- Any reply closes a question an agent asked you: `dockingbird answer ROW`, `send NAME TEXT`, or `send NAME TEXT --kind KIND --reply-to ROW`. A second answer is refused. An agent that asked without waiting is listed by `dockingbird questions` as `not waiting`.
