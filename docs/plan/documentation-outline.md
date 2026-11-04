# Dockingbird customer documentation: outline and search plan

Draft for review, 2026-11-04. This document plans the public documentation set. It names every page the set should
hold, what each page covers, which commands it shows, the cookbooks and examples, the troubleshooting plan, the
copy-and-paste prompt for a customer's coding agent, the diagrams, and the search index that ships with the docs. It
does not write the pages.

Readers of the docs: a developer who knows Docker, git and a terminal and has never seen Dockingbird; the person who
runs a team's hosts; a developer who scripts against `--json` or the MCP server; and the coding agent (Claude Code or
Codex) that a customer points at these docs to do the set-up.

Three rules hold for every page.

1. The docs are the single source of the customer's commands. A cookbook shows the command a reference page already
   prints, with the done line that page prints. A planned onboarding check (build order, step 4) will run the
   documents' own commands, so a page that drifts from the product will fail that check.
2. Every step names its done line: the exact line the product prints when the step worked, or the message id when it
   did not. A reader, or an agent, can tell at each step whether to go on.
3. Nothing internal. Section G is the boundary. The export that writes this repository refuses part of it by code;
   the rest is a review item on every export.

## What exists today

The repository holds 18 pages from one export: the README's customer part, the quickstart, the operator guide's
Docker-mode part (29 sections, about 740 lines), the troubleshooting catalogue (1,164 message entries, generated), four
integration pages (the `--json` envelope, the MCP host tools, the hosts file, the compatibility promise), one release
note, five examples (one Mac, two Macs over ssh, a cloud VM, a team fleet, three Python task scripts) and two templates
(an `AGENTS.md`, an `app.toml`).

Measured against the 40-step onboarding journey (read the docs, install, activate, status, seats, trial, update, first
start, hosts, completion, offline, term end, deactivate, clean, init, org login, the GUI): 22 steps are documented with
their done line, 11 are documented without it, 3 have no page (moving a seat to another computer, an install that fails
on a bad key, the offline and expiry day counts), and 3 depend on features a customer cannot use yet (licence
enforcement, the GUI binary, the hosted store).

Topics no page covers: a glossary, an architecture picture, data and privacy, backup and restore of a home, limits, a
FAQ, the version scheme, the support path, and a line saying Intel Macs, x86 Linux and Windows are not supported.

## A. Repository structure

Status column: exists (exported today), new (to write), split (exists inside the operator guide, becomes its own page),
not yet (the feature is not available to a customer; the page ships when it is), decision pending (the page ships, or
the command leaves the docs, once it is decided).

`llms.txt`, `SUPPORT.md`, `LICENSE`, `CHANGELOG.md`, `docs/plan/`, `docs/manifest.json` and `search/` are authored in
this repository, so the product's export must list them in its keep list before it runs again.

### Root

| Path | Status | Covers | Commands |
|---|---|---|---|
| `README.md` | exists | what Dockingbird is in four lines, prerequisites, the install line, the command table, a link to the exit codes page, links to the quickstart and the troubleshooting page | `uv tool install`, `license activate`, `claude`, `status`, `sync`, `stop` |
| `llms.txt` | new | the agent's entry point: one line per page with its summary, in reading order (section F) | none |
| `SUPPORT.md` | new; its channel is decided before the first public export | five lines: where to ask, where to file an issue, what to attach (`dockingbird --version`, `status --json`, the message id) | `dockingbird --version`, `status --json` |
| `LICENSE` | new, pending a decision | the licence of the examples and templates | none |
| `CHANGELOG.md` | new | one line per release pointing at `docs/release-notes/<tag>.md` | none |

### `docs/getting-started/`

The quickstart stays as the one-page path. These pages hold the detail each quickstart step links to.

| Path | Status | Covers | Commands |
|---|---|---|---|
| `docs/quickstart.md` | exists; add the `init` step, the done line of each step, the bare-install warning and git among the prerequisites | install, activate, make a repo ready, first run, daily loop, delegation, uninstall | the quickstart's 20 commands |
| `prerequisites.md` | new | Apple silicon Mac or arm64 Linux; Docker Desktop or Docker Engine with buildx; uv; git at the system path; disk for the image (about 1 GB) and the home; what is not supported (Intel Mac, x86 Linux, Windows); the check for each | `docker version`, `docker buildx version`, `uv --version`, `git --version` |
| `install.md` | new | the Mac install line and the Linux variant; why the key goes through the environment and never argv; the version check; what a failed install looks like (a 401 on a wrong or revoked key, a bare `uv tool install` with no index) | `uv tool install`, `dockingbird --version`, `uv tool update-shell`, `completion --install` |
| `activate.md` | new | one seat is one person with up to three computers: the licence counts computers per seat, and in this release nothing refuses a start; activate, the done lines (activated, then the terms); a trial and its limits (no index install, no update); where the key is stored; a key typed as a word is refused | `license activate`, `license trial`, `license status` |
| `first-run.md` | new | `init` and what it writes; the first start: the image build (about 5 minutes once), the copy of the branch, the sign-in link or an API key; the lines the product prints at each point; the trust default, in one sentence: every checkout is trusted, so the repo's own hooks, settings and MCP servers run inside the agent unless `trust --off` marks it (`guides/trust-and-repo-settings.md`); the 30-minute idle stop | `init`, `claude`, `codex`, `login claude --api-key`, `status`, `stop` |
| `choose-a-topology.md` | new | one computer, two computers over ssh, a cloud VM, a team pool; which pages and examples each one needs | none |

### `docs/concepts/`

Explanation pages. No commands to run, one diagram each (section E).

| Path | Status | Covers |
|---|---|---|
| `architecture.md` | new | a host runs the CLI and one or more homes; a home runs agent containers; the agents' commits come back over sync; nothing from the computer mounts into an agent unless connected by name |
| `glossary.md` | new | home, agent, the bus, a turn, a delivery, a question row, config, connection, host, pool, swarm, role, workload, the control plane, seat, computer |
| `agents-and-the-bus.md` | new | how a task reaches an agent, how its answer comes back, what `wait`, `inbox`, `read`, `send` and `results` each move, what a question row is and why a start can block on one |
| `sync-model.md` | new | how the agents' commits reach you: each agent works in a copy of your branch from your last commit; commits travel both ways as git bundles and arrive on the ref `dockingbird/<branch>`; when you are behind, `sync` fast-forwards and names each commit's agent; when both sides moved, it offers a merge on a terminal and prints the look-first command without one; a conflict, and a merge in progress that stops every later sync and start; turning a commit down with `git revert` (a reset brings it back at the next sync); `sync --let-go` for a branch made again; `sync --accept` after a pause; your uncommitted edits stay; what is refused before a bundle (a symlink leaving the repo, a submodule, a Git LFS file); the protections your git runs with during a sync; claims and shares; branches: which branch a copy holds, two agents on one branch, a branch switch while an agent runs, a linked worktree (verified by a run before it is written) |
| `claude-code-and-codex.md` | new | what differs between the two tools an agent runs: the sign-in (Claude shows a link and takes a pasted code, Codex a device code); `set` refused for a Codex agent at a terminal; `pin stable` for Claude only; `harness_args` per tool; `--agent-md` for both, `--claude-md` for Claude only; Claude as a config's default tool; cost figures from Claude only; how to pick the model and effort for each |
| `swarms-and-roles.md` | new | a definition's roles, counts and `send_to`; a role library; a coordinator role; values at submit; what a workload is |
| `fleet-and-hosts.md` | new | the hosts file versus the pool; the one-name rule; placement order; the control plane's home; what a worker and an admitter do |
| `licensing-model.md` | new | seats, computers, the computer id (what makes a computer "the same" after a reboot, a VM rebuild or a container), check-ins, offline grace, term end; that enforcement is advisory in the current release; one paragraph, until the hosted store ships, on the three ways to run it: the customer runs the store and the hosts (available today), the publisher runs the store (not yet), the publisher runs the store and the customer runs the hosts (not yet) |
| `security-model.md` | new | what an agent can reach (egress modes), what it cannot (your home folder, your keychain, other repos), where secrets live (connections hold them, agents never do), what `clean --all` removes |

### `docs/guides/`

Task pages. Each opens with the goal, lists prerequisites, shows the commands with their done lines, and ends with
the message ids a reader may meet and the page that explains each.

| Path | Status | Covers | Commands |
|---|---|---|---|
| `daily-loop.md` | split | start an agent at your terminal, read status, take its commits with `sync` (`--accept` after a pause, `--let-go` for a branch made again; the model is on `concepts/sync-model.md`), stop; the reconnect and the `--new` start; when the laptop sleeps or the network drops (Docker Desktop waking from Resource Saver, a closed terminal, the agent's model calls during a drop, a host unreachable over ssh), each with what resumes by itself and what needs a command; an agent that ended with work not shared or crashed: the pick-up by `--as NAME`, where the kept copy is, what `clean` asks; its "when it fails" block names `SYNC_UPDATED`, `SYNC_BOTH_MOVED`, `SYNC_CONFLICTS`, `START_MERGE_OFFER`, `DOCKER_WAKING`, `AGENT_KEEPS_WORKING`, `AGENT_STOPPED_NOT_SHARED`, `AGENT_CRASHED`, `CLEAN_ASK_UNSHARED`, `STATUS_KEPT_WORKTREE` | `claude`, `codex`, `claude --as NAME`, `status`, `sync`, `sync --accept`, `sync --let-go`, `stop`, `clean NAME` |
| `delegating-tasks.md` | split | hand an agent a task on the bus, wait, read, answer a question, send more, save results; priorities and paging in the inbox; the one-shot `claude -p` | `start`, `wait`, `inbox`, `read`, `questions`, `answer`, `send`, `results`, `search`, `set` |
| `connections.md` | split | give agents a GitHub repo, a folder, a database, an MCP server, a program or a browser without handing them the secret; grants to one agent or a role; revoke; serve a connection as yourself; watch or take over an agent's browser | `connect`, `connections`, `revoke`, `disconnect`, `serve`, `serve --unit`, `watch` |
| `your-own-commands.md` | split | add a command of your own from an `app.toml`; the default command; a config shared across repos; the four keys that decide what it does: `tools` (`bus`, the default, moves messages and files and no commits reach `sync`; `default` or `full` let its commits reach you), `workspace` (a copy of the repo, or `scratch`, an empty folder), `mode` (on the bus or at your terminal, fixed once set), `context` (one conversation for every task, or `fresh`, a new one per task, on the bus only) | `config add`, `config list`, `config remove`, `start --command` |
| `toolchains.md` | split | the language versions agents get from `mise.toml` or `.tool-versions`; lock and change them | `env`, `env install`, `env lock`, `env use` |
| `trust-and-repo-settings.md` | new | which checkouts are trusted: every one, unless `trust --off` marks it or the `trust =` line of `config.toml` makes untrusted the default; what a trusted checkout loads inside the agent (the repo's own Claude Code and Codex settings, hooks and MCP servers, its rules file, its mise `[env]` and `[settings]`, its dependency installs); what an untrusted one gets (its toolchain alone, no repo rules, a question from Claude and a folder notice from Codex, which Dockingbird never answers); a trusted repo's Codex config that sets `developer_instructions`, refused; your own rules for every agent in the home's `instructions/` files; its "when it fails" block names `TRUST_NOTE`, `START_NO_SCREEN_TRUST`, `DEPS_SKIPPED_UNTRUSTED` | `trust`, `trust --off`, `trust --forget`, the `trust =` line of `config.toml`, `claude --no-toolchain` |
| `sign-in-and-api-keys.md` | split | reuse of the computer's sign-ins, at the first start or on demand with `login claude --here`; re-sign-in, sign-out, an API key, the last login wins | `login claude`, `login claude --here`, `login codex`, `login --api-key`, `logout` |
| `egress-and-network.md` | split | the four egress modes, an allowlist, what a blocked host looks like from inside the agent, a proxy | `egress`, `claude --egress`, `start --egress` |
| `hosts.md` | split | add a second computer over ssh or a cloud VM through gcloud; the `--path` and `--docker-host` fixes; read every agent on every host; attach to one | `fleet hosts set`, `fleet hosts rename`, `fleet hosts forget`, `fleet agents`, `fleet attach`, `fleet probe` |
| `swarms.md` | split, marked "for teams" | write a definition, describe it, submit it with values, follow it in the queue (`guides/fleet-scheduler.md`); while it runs: add agents of a role, retire or replace one, reassign a reviewer or tester, prune after a merge, and what each does to the agents still working (each stops after its running turn); this home's record of swarms and roles | `fleet describe`, `fleet submit --set`, `fleet submit --values`, `fleet add`, `fleet retire`, `fleet replace --fresh`, `fleet assign --reviewer --tester`, `fleet prune --merged`, `swarm list`, `swarm add`, `swarm remove`, `swarm role`, `swarm assign` |
| `work-queue.md` | split, marked "for teams" | for a team whose people, scripts and agents share one board of work in the organisation's store, from any computer with the org login: items, statuses, search, what needs you, an item's log and ETA, requests and their answers | `work status`, `work show`, `work search`, `work new`, `work needs-you`, `work set`, `work log`, `work eta`, `work check`, `work requests`, `work respond` |
| `licensing.md` | split, plus the three gap steps | activate, status, the seats list, free a seat, move a seat to a new laptop (one story), deactivate, the trial, what each refusal means, offline behaviour and the day counts | `license activate`, `license status --refresh`, `license activations --release`, `license deactivate`, `license trial`, `clean --all` |
| `updates.md` | split | check and update; a staged update when agents run and the switch at their stopping point; moving a fleet to a release; reading homes of another version, with one line on `inspect swarm`; pinning a tool version; a release that removes something: the one-release notice of the compatibility promise, `init --check` and `INIT_OUT_OF_DATE` after an update, the org store's migration order | `update --check`, `update`, `fleet update`, `homes`, `inspect swarm`, `pin`, `init --check` |
| `gui.md` | not yet | install and open the GUI, its tabs and keys (`ctrl+b`, then `d` and a letter), copy from it, detach | `ui --install`, `ui`, `ui stop` |
| `mcp-server.md` | split | let your own Claude Code or Codex start agents through `dockingbird mcp`; install into the harness; the eleven tools in one table | `mcp install`, `mcp install --check`, `mcp install --show`, `mcp install --connected` |
| `clean-and-uninstall.md` | split | free disk, delete stopped agents, remove everything and give the seat back, uninstall the tool; the disk a week of use takes (each agent's copy holds the repo's history, five Docker volumes, the toolchain store, Docker's build cache), with the sizes `clean` prints and `docker system df` | `clean`, `clean NAME`, `clean --all`, `docker system df`, `docker builder prune`, `uv tool uninstall` |
| `backup-and-restore.md` | new | what the home and its five Docker volumes hold (the sign-ins live in the volumes); what to save before replacing a computer (results, configs, `hosts.toml`); start fresh on the new computer and re-activate; a restore of a copied home is written only after a run proves it | `results --to`, `config list`, `homes`, `license activate` |
| `harbor.md` | decision pending | run a Harbor benchmark task's two baselines and one real trial with your own login, then list, read and clean its jobs; the decision: out (the README's rows, the top help screen's group and the catalogue's benchmark domain go before the first export) or in (this page, priority 3) | `harbor baseline`, `harbor run`, `harbor jobs`, `harbor results`, `harbor clean`, `harbor version` |
| `data-and-privacy.md` | new | what leaves the computer (licence check-ins, the model API traffic of the agent's own tool, nothing from a repo to the publisher), what is kept where, how to see it | `license status`, `egress` |

The operator guide stays in the repository as the long form until each of these pages exists; each new page links to
the guide section it replaces, and the guide gets a one-line pointer at the top of each section to its page. The
split happens at the source of the export, section by section.

### `docs/reference/`

Lookup pages, generated where the product can generate them, so they cannot drift.

| Path | Status | Covers |
|---|---|---|
| `commands.md` | new, generated from the help screens | every command a customer can type, with its arguments, one line of purpose, its exit statuses and a link to its guide page; the global options (`--verbose`, `--json`, `--home NAME`); the unlisted `fleet`, `work` and `inspect swarm` commands included; `native` and the other developer-only commands left out, `harbor` as its decision says |
| `files/hosts-file.md` | exists; add `repoint`, `name`, `clones` | every key of `hosts.toml`, with the `repoint` line `fleet update` runs and a worker home's `name` and `clones` |
| `files/org-file.md` | new | `org.toml` and the `~/.pgpass` line |
| `files/swarm-definition.md` | new | every top-level and `[[role]]` key of a definition at `schema = 1`, with defaults |
| `files/app-config.md` | new, from the template | every key of `.dockingbird/app.toml`, including `context` and `[limits]` |
| `files/roles-and-connections.md` | new | a library role file, a service connection file (`minimum`, `maximum`, `choices`, `max_chars`), a subagent block |
| `files/project-file.md` | new | what `init` writes: `project.toml`, `rules.md`, `skills.lock`, the roles |
| `files/home-layout.md` | split | what lives where under the home, the marker file, `--home NAME` for a second home on the same computer (it shares the computer's seat), `config.toml` with its `trust =` line, `egress.toml`, `versions.toml`, the instruction files, the lock files |
| `integration/json.md` | exists; its exit table moves to `exit-codes.md` | the envelope keys, with a link to the exit statuses |
| `integration/mcp.md` | exists | the eleven host tools by name and argument |
| `integration/compatibility.md` | exists; add `org.toml` and exits 69, 77, 78 | the promise |
| `integration/exit-codes.md` | new; the one exit table | 0, 1, 2, the tool's own, 69 (the store unreachable), 77 (a login outside `fleet_admin` on an admin command), 78 (a fleet refusal), each with what a script does on it; the page says both "exit code" and "exit status", and `json.md`, `compatibility.md` and the fleet pages link to it |
| `environment-variables.md` | new | every `DOCKINGBIRD_<NAME>` setting a customer may set, with its default |
| `limits.md` | new | one row per bound with its figure: no turn deadline unless a config sets one, a config agent's session of 12 hours (at most 168), the 30-minute idle stop, an 8-character fleet label, 80 computers in the activations list, a 64 KB rules file; the per-home agent cap (24), a fleet-started agent's session (48 hours), a terminal agent's limit, the hosts list cap and message sizes, each confirmed against the release by a run before it is written |

### Pages of sections H, I and J

Each page below has its one full row in its section's table.

| Section | Pages | Status |
|---|---|---|
| H. Networking and integrations | `guides/networking.md`, `guides/tailscale.md`, `guides/other-networks.md`, `guides/cloud-vms.md`, `guides/github.md`, `guides/mcp-and-services.md`, `guides/databases.md`, `guides/secrets-vault.md`, `reference/ports-and-hosts.md` | new |
| I. Observability | `concepts/observability.md`, `guides/metrics.md`, `guides/prometheus.md`, `guides/grafana.md`, `reference/metrics.md`, `examples/observability/` | new; the reference page generated |
| J. Fleet scheduling and the control plane | `concepts/fleet-scheduler.md`, `concepts/control-plane.md`, `guides/team-fleet.md`, `guides/fleet-scheduler.md`, `reference/fleet-tools.md`, `reference/files/fleet-store.md` | new and split, marked "for teams" |

### `docs/troubleshooting/`

Section C. The generated catalogue stays as one file; the folder adds the index pages.

### `docs/release-notes/` and `docs/legal/`

One file per tag, added by each release. `next.md` holds the draft. A `versioning.md` page states the scheme (what
a minor and a patch change may do to the integration surface) once decided. `legal/eula.md` and `legal/privacy.md`
ship when cleared.

### `docs/faq.md`

Thirty questions, three lines each, one link each. Thirteen questions are known today. The other seventeen come
from two logs: search queries that returned nothing, and questions an agent asked that no page answered (practice
15, section K).

| Question | The page its answer links to |
|---|---|
| Does it need the cloud? | `concepts/architecture.md` |
| What do I need: Mac or Linux, Docker, uv, git, disk? | `getting-started/prerequisites.md` |
| Where does the key go, and how do I know the install worked? | `getting-started/install.md`, `getting-started/activate.md` |
| What does the agent see of my computer and my repo? | `concepts/security-model.md` |
| Where are the agent's changes, and what if we both committed? | `concepts/sync-model.md` |
| Can two agents work on one branch at once? | `concepts/sync-model.md` |
| Can two people share a seat? | `getting-started/activate.md`: a seat is one person with up to three computers, and nothing refuses a start in this release |
| Why is the first start slow, and how much disk does it take? | `getting-started/first-run.md`, `guides/clean-and-uninstall.md` |
| What happens when I close the lid or lose the network? | `guides/daily-loop.md` |
| Claude Code or Codex: which should I use, and how do I pick the model? | `concepts/claude-code-and-codex.md` |
| How do I stop everything? | `guides/daily-loop.md` |
| How do I move to a new laptop? | cookbook 5 |
| Something failed: where do I ask, and what do I send? | `SUPPORT.md` |

### `examples/` and `templates/`

Section B. Templates gain `.dockingbird/roles/<role>.toml`, `.dockingbird/connections/<name>.toml` and a
`swarm.toml` beside the existing two.

### `search/` and `.github/`

Section F. Generated; never edited by hand.

## B. Cookbooks and examples

Each cookbook is one task, in order, with each command's done line and the message ids it may meet. Priority 1 ships
with the first public version; 2 within the next two releases; 3 when its feature is available.

| # | Cookbook | Goal | Commands it shows | Status | Priority |
|---|---|---|---|---|---|
| 1 | Day one on one Mac | install, activate, first run, one delegated task, sync | `uv tool install`, `license activate`, `claude`, `start`, `wait`, `inbox`, `read`, `send`, `results`, `sync` | exists | 1 |
| 2 | Delegate a task and collect the files | a script hands an agent a task and saves its files | `--json start`, `wait`, `read`, `results` | exists (Python) | 1 |
| 3 | Review a branch in CI | a one-shot review of a diff, exit status from the tool | `--json claude -p` | exists (Python) | 1 |
| 4 | Recover from a failed install | the three failures: no index, a bad key, a wrong platform; what each prints; the fix | `uv tool install`, `dockingbird --version` | new | 1 |
| 5 | Move your seat to a new laptop | free the old computer's link, activate the new one, what status shows on each | `license activations`, `license activations --release`, `license activate`, `license status --refresh` | new | 1 |
| 6 | Give agents a database without the password | a database connection with a brokered write, a service file with arguments, a grant to a role, a revoke | `connect --database`, `connect --service`, `connect --to-role`, `connect --revoke`, `connections` | new | 1 |
| 7 | Your own `dockingbird review` command | an `app.toml` with a skill and instructions, registered for every repo | `config add`, `config list`, `dockingbird review` | new | 1 |
| 8 | A second Mac over ssh | add the host, fix `PATH` and the Docker socket, read its agents, attach | `fleet hosts set --ssh`, `fleet agents --host`, `fleet attach` | exists | 1 |
| 9 | A cloud VM | start a stopped VM, add it through gcloud, read its agents | `fleet hosts set --gcloud`, `fleet agents --host` | exists | 1 |
| 10 | Lock the tools your agents run | pin Claude Code or Codex to a version, follow latest again | `pin`, `pin --clear`, `update` | new | 2 |
| 11 | Restrict what agents can reach | an allowlist with a registry preset and two hosts, what a blocked request looks like | `egress allowlist --allow`, `claude --egress` | new | 2 |
| 12 | Update with agents running | the staged update, the switch at the stopping point, what status shows while it waits | `update`, `status` | new | 2 |
| 13 | Before you replace a computer | save results, configs and `hosts.toml`, give the seat back, start fresh on the new one; a restore of a copied home waits for a run that proves it | `results --to`, `license deactivate`, `license activate` | new | 2 |
| 14 | A status dashboard | status and every host's agents as one JSON object | `--json status`, `fleet hosts`, `fleet agents` | exists (Python) | 2 |
| 15 | A team fleet on PostgreSQL | the store, roles, two hosts in a pool, a worker and an admitter as services: the launchd property list and the systemd user unit in the form `serve --unit` prints, the `repoint` line, the restart order | `org login`, `org create`, `fleet hosts add`, `fleet worker`, `fleet admitter`, `fleet update` | exists; its `fleet.toml` section is out of date and teaches a refused password key | 2 |
| 16 | A swarm from a role library | a coordinator and four graders from library roles, helpers, values at submit, brokered scores | `fleet describe`, `fleet submit --set`, `fleet submit --values`, `fleet add`, `fleet retire` | exists in the source, not exported; needs a neutral name and the argument keys `minimum` and `maximum` | 2 |
| 17 | Join a second computer to a control plane | the control plane's home, a token per computer, join, status, remove, then a new bundle and a rejoin after a lost home | `cp init`, `cp token`, `node join`, `cp status`, `cp remove`, `node leave` | new | 2 |
| 18 | Uninstall completely | stop, clean everything, give the seat back, remove the tool, prune the builder | `stop`, `clean --all`, `uv tool uninstall`, `docker builder prune` | exists in the quickstart | 1 |
| 19 | The GUI | install, open, the tabs, copy out, detach | `ui --install`, `ui` | not yet | 3 |
| 20 | A fleet on a tailnet | the control plane's tailnet address, the served hub port, the grant for a tagged VM, one join per computer | `cp init --hub-address`, `tailscale serve`, `cp token`, `node join` | new | 2 |
| 21 | A host behind a bastion | a `ProxyJump` entry, the host set over it, the `--path` fix | `fleet hosts set --ssh` | new | 2 |
| 22 | Prometheus and Grafana for a fleet | the exporter on each host, the two scrape jobs, the default dashboard imported, one alert | `fleet scrape`, `fleet probe --json`, `fleet queue --metrics` | new | 1 |
| 23 | Run a test suite under a lease | a lease of cores and memory, the wait for a host, the command's environment | `fleet run --cores --memory --bound` | new | 2 |
| 25 | Change a running swarm | add two agents of a role, retire one, prune after a merge | `fleet add`, `fleet retire`, `fleet prune` | new | 2 |

Every Python example reads the envelope's `id` and `fields` and never its `lines`, uses the standard library only, and
ends with the exit status its page states. A shell example is not admitted.

## C. Troubleshooting plan

The catalogue is one generated page: 1,164 entries, one per message id, 33 groups. An entry has five parts: a
"When:" line, the message text, its other forms, a next step and an exit status. The ids do not change between
releases, so a link to one holds. The page stays as it is. Four things get added around it.

1. Ten index pages under `docs/troubleshooting/`, one per domain, generated. Each lists its ids with the "When:"
   line and a link to the entry. The domains and their entry counts: install, Docker and licensing, 65; homes, the
   checkout and toolchains, 110; agents, status, sync and clean, 300; the bus, 70; configs, connections and host
   resources, 197; the fleet, swarms and the work queue, 210; benchmark jobs, 51; sign-ins and the org store, 91;
   updates, 43; the GUI and the MCP server, 27. Two entries exist for developers only. The generator skips them.
2. A "when it fails" list at the foot of every guide. It names the ids that page's steps can hit, in step order, one
   line and one link each. The getting-started pages take their order from the onboarding journey.
3. Three pages that tell a failure as a story, because a first-week reader hits these as a sequence and not as one
   message. Install fails: no index, a bad key, the wrong platform, no Docker, no git. Licence refused: seats full, a
   freed computer, a trial already used, the term over. First start stops: a file in the home, a folder that is not
   a checkout, a sign-in that never finishes.
4. Search fields. Every entry becomes one chunk. Its id, its "When:" line, its exit status and its domain are fields,
   so a query with an id in it, or a phrase copied from the screen, lands on the entry first (section F).

Three ways to find an id: `--verbose` prints it in brackets, `--json` carries it as `id`, and the shell's `$?` holds
the exit status.

## Fixes the pages need before the repository goes public

Found while mapping the pages; each is one edit at the source of the export.

- The operator guide's update section shows an install from the product repository's git address and names the GUI
  repository; the index install never runs that line.
- The GUI section names a private repository, an SSH key and a source file; the quickstart still advertises
  `ui --install`. The GUI page is marked not yet until a customer channel exists.
- The migrations section names source paths, planning documents and four specification numbers.
- The delegated agents section uses two swarm names that are specification numbers.
- The one-Mac example's GUI step names the private repository.
- The team fleet example teaches a `fleet.toml` with a password key the product refuses.
- The swarm graders example carries a name that may be a client's, and its two service files use `min` and `max` where
  the product reads `minimum` and `maximum`.
- The `app.toml` template lacks the `context` key the guide's example shows.
- The hosts file page lacks the `repoint` line `fleet update` runs and a worker home's `name` and `clones` keys.
- The envelope page omits exit 77; the promise omits `org.toml` and exits 69, 77 and 78.
- The quickstart and README omit git from the prerequisites and the `init` step.
- Four sections say "the owner" for a PostgreSQL role owner; "the role that owns" reads right to a customer.

## D. The copy-and-paste set-up prompt for a customer's coding agent

One block, `docs/agent-setup-prompt.md`, that a customer pastes into Claude Code or Codex on the computer that will
run Dockingbird. The agent reads the docs, checks the computer, hands the two key steps to the owner, makes the
repository ready, starts a first agent with `dockingbird start` and reports. The block is plain text under 120 lines,
in these sections, in order.

| # | Section | What it says |
|---|---|---|
| 1 | Who you are | "You are setting up Dockingbird on this computer with its owner. The owner types the licence key and does any sign-in; you run every other step, and only after the checks below pass." |
| 2 | Read first | `llms.txt`, `docs/quickstart.md`, `docs/getting-started/prerequisites.md`, `templates/AGENTS.md`, the topology page that matches (one Mac, two Macs, cloud VM, team). Read, do not skim: the done line of each step is on those pages. |
| 3 | Check before you act | OS and CPU (Apple silicon or arm64 Linux), Docker with buildx, `uv`, `git` at the path the prerequisites page names, free disk, an empty Dockingbird home. Report each check as pass or fail with the command used. Stop on any fail and show the troubleshooting entry. |
| 4 | Hand the key steps to the owner | Ask which repository to set up and which topology. Ask the owner to run, at their own terminal, the install line with the key and then `dockingbird license activate`. Never ask for the key: a key pasted into this chat lands in your transcript. |
| 5 | Check the owner's steps | `dockingbird --version`, then `dockingbird license status`. Done line: `LICENSE_SHOWN`. |
| 6 | Make the repository ready | `cd <repo>`, `dockingbird init`. Done line: `INIT_DONE`; with no org login `INIT_NOT_REGISTERED` follows it, and both mean success. |
| 7 | First start | `dockingbird start "say hello and stop"` (`--harness codex` for Codex), run in the background with a 10-minute wait: the first start builds the image (about 5 minutes) and adopts this computer's Claude Code or Codex sign-in. Then `dockingbird status` and `dockingbird wait`. On `SIGNIN_NEEDED` or `START_NO_SIGNIN_BUS`, stop: the owner signs in at the terminal with `dockingbird login claude` (or `login codex`), then run this step again. |
| 8 | Prove it | `dockingbird status --json`, `dockingbird license status`, one `dockingbird send` and `dockingbird read` round trip with the agent step 7 started. |
| 9 | Optional topology | `fleet hosts set` for a second computer, `org login` for a team store. |
| 10 | Report | a table of steps, commands, done line seen, exit status, and every troubleshooting entry hit, with the agent's own next step. |
| 11 | Never | ask for the key, or read it from the clipboard, a file or the chat; put it in argv, history, a file or the report; run `uv tool install dockingbird` without the index; edit files outside the repository being set up; run `clean --all` without the owner's word. |

The owner runs the steps that need a person at a terminal: the key prompt is hidden, a key pasted into a chat lands in
the agent's transcript, and a sign-in shows a link and asks for a code. The agent's first start works on the bus, so it
needs no screen. The guard rails come from the journey order (install, then activate, then init, then start) and from
the troubleshooting catalogue (every stop names an entry id). Each step's done line is the line the docs print, so a
doc that drifts from the product breaks the prompt at that step.

## E. System diagrams to produce

All Mermaid, in the page they explain, with a text alternative under each. One thing each must make clear:

| Diagram | Page | The one thing it must show |
|---|---|---|
| Hosts, homes, containers | concepts/architecture.md | one host runs many homes; one home runs many agent containers; the CLI on the host talks to its home |
| The bus | concepts/agents-and-the-bus.md | a message's path: `send` from the host, the agent's inbox, its turn, `results`, `read` and `wait` on the host; nothing reaches an agent except through the bus |
| An agent's life | concepts/agents-and-the-bus.md | start, turns, a question row, a stop; which commands move it between states |
| A swarm's life | guides/swarms.md | a definition's roles, `fleet submit`, placement on a host, the coordinator role, the roles' `send_to`, the end |
| A rolling update | guides/updates.md | `dockingbird update` on a home with running agents: each agent takes the release at its next stopping point; nothing is killed mid-turn |
| A workload's life | guides/fleet-scheduler.md | submitted, pending, held, admitted, starting, running, paused, done or cancelled, and the command that moves it |
| A member joins | guides/team-fleet.md | the bundle from `cp token` to `node join`, the hub port, the fleet session a start opens, the fleet inbox beside the agent's own |
| The fleet | concepts/fleet-and-hosts.md | the control plane's home, member computers joined with `node join`, the scheduler's pool and placement order |
| The sync model | concepts/sync-model.md | the agents' branch and the reader's branch; a bundle's path on `sync`; the both-sides merge offer; two agents on one branch |
| Swarms and roles | concepts/swarms-and-roles.md | a definition's roles and counts; `send_to` edges between roles; values at submit; the coordinator role |
| Hosting paradigms | concepts/hosting-paradigms.md | who runs the store and who runs the hosts in each of the three; which is available today |
| The security model | concepts/security-model.md | what an agent reaches (its container, its copy of the repo, the egress it is allowed) and what it never reaches (the home folder, the keychain, other repos) |
| A trust decision | guides/trust-and-repo-settings.md | the first-run trust question; what loads when trusted (the repo's settings, hooks, MCP servers) and what stays off |
| Seats and computers | guides/licensing.md | a key, a seat per person, up to three computers per seat, a computer id, activate and release; what runs offline and for how long |
| The integration surface | reference/integration/compatibility.md | the three doors: `--json` envelopes, the MCP host tools, the files a customer writes; the compatibility promise covers these and nothing else |
| The metrics path | guides/prometheus.md | an agent's `/metrics` inside its container network; the host's `fleet scrape` rendering it; the exporter; Prometheus; Grafana; nothing published from the container |
| A fleet on a tailnet | guides/tailscale.md | the control plane's hub port served on the tailnet; members joining over it; ssh routes over the same tailnet |
| Network egress | guides/egress-and-network.md | the agent container's egress modes (full, allowlist, models, none); which hosts each mode reaches |

## F. Search plan: pre-computed and static

A reader or an agent should find the one section that answers a question in one step, from a clone of the repo or
from the hosted page, offline, and the first tier installs nothing.

### The unit of search is a section

Every page is split at its H2 and H3 headings. A section over about 400 words is split again at paragraph breaks, at a
bold run-in heading that opens a paragraph and, for a paragraph still over the cap, at sentence breaks, so no chunk
passes about 400 words; the operator guide's long sections, kept until the split, are cut the same way. Each chunk
carries: page path, heading path (H1 > H2 > H3), the commands it names (backticked `dockingbird ...` words, indexed
whole and by the subcommand word alone, so `sync` matches `dockingbird sync`), the flags it names (tokens that start
with `--`), the message ids it names (tokens on the catalogue's id list, read from its H3 headings; any other upper-case
token, such as `DOCKINGBIRD_HOME`, is prose), the tool names it names (the MCP host tools and the fleet tools), the
audience tag from the page's front matter (first day, daily, integrator, team admin), and the first sentence as its
summary. The troubleshooting catalogue is chunked one entry per chunk, with its id, its "When:" line and its exit code
as fields.

### Four tiers, each built from the same chunks

| Tier | Artifact | Who uses it | Needs |
|---|---|---|---|
| 1 | `llms.txt` at the root and `docs/manifest.json` (page, summary, audience, commands, message ids) | coding agents on the first read | nothing; two files |
| 2 | `search/index.json.gz`: a BM25 index over the chunks (terms, document frequencies, per-chunk term counts) and `search/search.py`, a standard-library CLI: `python search/search.py "seats full"` prints the top 10 chunks as path, heading, score, first line | anyone with a clone or the raw files; agents in a container | Python 3.12, no packages |
| 3 | `search/embeddings.bin` (float16, 384 dimensions per chunk) plus `search/chunks.jsonl`, built with `BAAI/bge-small-en-v1.5` (MIT, 33M parameters) through `fastembed` (Apache 2.0, ONNX, CPU); the query side embeds with the same model and merges with tier 2 by reciprocal rank fusion | agents and tools that can run a 130 MB model; a hosted page | `fastembed` at query time, or the hosted page's worker |
| 4 | The hosted docs site's own search: Pagefind (MIT) indexes the built HTML at build time and serves chunked index files; the browser loads only the chunks a query touches | readers of the website | a static host |

Tiers 1 and 2 ship first. CI builds them. Tier 3 waits for a hosted page or an agent tool that wants vectors. Tier 4
arrives with the website.

### Why BM25 before embeddings

A customer types exact things: `LICENSE_SEATS_FULL`, `--release`, a file key. BM25 over the chunk fields finds those
tokens as typed. An embedding model breaks them into word pieces and ranks a prose chunk above the entry. Where
embeddings win is a paraphrase, "my second laptop can't activate". So embeddings come second, merged with BM25 by
reciprocal rank fusion. The tier 2 query side is plain Python and needs no network, which is what an agent inside a
container has.

### The build

- `.github/scripts/build_index.py`: walks `docs/`, `examples/*/README.md`, `templates/`, chunks, writes `docs/manifest.json`, `llms.txt`, `search/chunks.jsonl`, `search/index.json.gz`. Standard library only. Deterministic output (sorted keys, fixed chunk ids as a hash of path and heading path), so the diff of a rebuild shows only real changes.
- `.github/scripts/build_embeddings.py`: optional second step, reads `chunks.jsonl`, writes `embeddings.bin`; pins the model name and its revision in the file header.
- A GitHub Actions workflow in `.github/workflows/search-index.yml` runs both on every push to `main`, commits the artifacts back (or publishes them as a release asset if the repo should stay free of generated files), and fails the build if `manifest.json` names a page that does not exist, a page has no front matter, or a troubleshooting id in a page is absent from the catalogue.
- A second job runs a fixed query set (`search/queries.txt`: 30 questions with the expected page) and fails when the expected page leaves the top 3. This is the regression test for the docs' findability. Its first eleven entries are the table under "The first regression list".

### Where the search files live

The product repository exports most of this repository. The export deletes everything except `.git` and its keep
list. Today that list holds `.github/`. Before the next export it must also hold the paths section A names. The
workflow file and the two build scripts sit under `.github/` for that reason, and the workflow writes `search.py`
into `search/` on every run.

### Ranking rules

- Phrase first. If a chunk holds the whole query as a substring (case folded, a `{placeholder}` in a message
  matching any one word), it beats every field match. A line copied from the screen therefore lands on its entry.
- Then exact tokens. An id, a command, a flag or a tool name in the query gets a field boost of 5 on `ids`,
  `commands`, `flags` and `tools`. A heading match gets 2.
- `-` and `_` stay inside a token. Ids and tool names are indexed whole and also split at `_`, so `seats full` finds
  `LICENSE_SEATS_FULL` while `agent_send` stays one token.
- Spelling runs before ranking. A query word absent from the vocabulary becomes the nearest word within two edits,
  and the output says so.
- `--audience first-day` prefers chunks tagged for that reader.
- The catalogue ranks under the guides when the query has no id and no phrase match, and over them when it has an id.
- Ties go to page order in `manifest.json`: getting started first, reference last.

### The first regression list

The first eleven entries of `search/queries.txt` are these queries, each with the page that must stay in its top 3 and
the rule that keeps it there.

| Query | Must stay in the top 3 | Rule |
|---|---|---|
| `LICENSE_SEATS_FULL` | its catalogue entry | id field |
| `seats full` | the `LICENSE_SEATS_FULL` entry | ids indexed split at `_` |
| `Every computer this license admits is linked` | the `LICENSE_SEATS_FULL` entry | phrase match |
| `--release` | `guides/licensing.md` | flags field, `-` kept |
| `my second laptop can't activate` | cookbook 5, `getting-started/activate.md` | prose; tier 3 improves it |
| `docker not runing` | the `DOCKER_NOT_RUNNING` entry | spelling step |
| `DOCKINGBIRD_HOME` | `reference/files/home-layout.md` | ids from the catalogue's list only |
| `agent_send` | `reference/integration/mcp.md` | tools field, `_` kept |
| `exit code 78` | `reference/integration/exit-codes.md` | the page says "exit code" once |
| `sync asks to merge` | `concepts/sync-model.md`, the `SYNC_BOTH_MOVED` entry | commands field matched by the subcommand word |
| `how do I move to a new laptop` | cookbook 5 | heading boost |

## G. Public-repo boundary checklist

This list covers every page, every example and every PR body in this repo. The export refuses the first three items by code. The reviewer of each export diff checks the rest against this list.

These never appear in this repo.
- A path under any person's home folder.
- A link into the product repo with a path after its address (a file, a PR, a commit, a tree).
- A link to a page outside the exported set (specs, plans, status files, decision records, parameters).
- A spec number, a PR number, a decision number, a date of an internal decision, an agent's or a session's name.
- A client's or a person's name (examples use neutral names: `acme`, `lab`, `review-1`).
- Source code of the product: no module names, no function names, no line numbers, no internals of the bus, the scheduler, the switcher or the licence client.
- The work queue's internals (its tables and the publisher's own items), skills, agent definitions, native-mode documentation, test fixtures. The customer's `work` commands have their guide page.
- A secret, a key prefix, a token, a signing key, a hostname of an internal machine, a tailnet address.
- The publisher's own monitoring: its Grafana, Prometheus, exporters, recording rules, hosts and dashboards; any metric the product keeps for its own tests.
- Unreleased features: a page documents what the released version prints; a feature behind a disabled gate is marked "not yet" or left out.

These appear, and the page states the reason each time:
- Message ids, their `fields` and exit codes: a customer's script reads them, and the compatibility promise names them.
- The `--json` envelope keys: the integration surface.
- The MCP host tools by name and argument: the integration surface.
- The files a customer writes and every key: the customer owns them.
- The image's prerequisites and what the first build does (time, disk): the customer waits for it.
- The egress modes and the hosts each reaches: the customer's network team asks.
- Metric family names, labels and the general queries: a customer's Prometheus reads them, and the generated reference lists them.
- Debug output a customer sends to support: `status --json`, `inspect swarm`, the logs folder's layout.

## H. Networking and integrations

Customers reach their hosts over a private network they already run. The docs name the setups the product was built
against and show the one thing each needs. Internal addresses, device names and policies stay out; placeholders
stand in.

| Page | Covers | Commands and files |
|---|---|---|
| `guides/networking.md` | the product's three network uses: the CLI reaching a host over ssh or gcloud; member computers reaching the control plane's hub on its TCP port; agents reaching the internet through the egress modes. What each needs open, what nothing else needs. | `fleet hosts set --ssh`, `fleet hosts set --gcloud`, `cp init --hub-address`, `egress` |
| `guides/tailscale.md` | a tailnet as the fleet's network: the control plane's tailnet IPv4 as the hub address; `tailscale serve` to expose the hub port from loopback; the ACL grant a tagged cloud member needs; ssh over the tailnet with MagicDNS names in `hosts.toml`; what the tailnet makes unnecessary (no public ports, no VPN); Tailscale SSH as an alternative to keys | `tailscale ip -4`, `tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222`, the policy grant line, `fleet hosts set lab --ssh lab` |
| `guides/other-networks.md` | the same three uses on a plain VPN or a cloud VPC: a WireGuard mesh, a bastion with `ProxyJump` in `~/.ssh/config`, a cloud VM reached by `gcloud compute ssh` with no public IP; what to put in `hosts.toml` for each | `~/.ssh/config` entries, `fleet hosts set --ssh`, `fleet hosts set --gcloud --zone --project` |
| `guides/cloud-vms.md` | a Linux VM as a host: the arm64 image, Docker Engine with buildx, uv, git; a stopped VM that an admitter starts; disk sizing for the image and homes; the `--path` fix when the login shell differs | `fleet hosts set --gcloud`, `fleet hosts add --power gcloud`, `fleet probe` |
| `guides/github.md` | agents working on GitHub repositories: a deploy key or an ssh agent, a branch, known hosts; grants to one agent or a role; what the agent can and cannot push | `connect NAME --github OWNER/REPO --key PATH`, `connect --agent`, `connect --branch`, `connections`, `revoke` |
| `guides/mcp-and-services.md` | giving agents an MCP server by URL, a local program as a service with typed arguments, a browser in its own container; serving them as yourself on a schedule | `connect --mcp URL`, `connect --service FILE`, `connect --browser chrome`, `serve`, `serve --unit` |
| `guides/databases.md` | a brokered database connection: the password stays with the host, the agent gets a name; read and write grants; the connection file's keys | `connect NAME --database URL --password --writes`, `connect --to-role`, `connect --revoke` |
| `guides/secrets-vault.md` | a password store as the source of logins and TOTP for a browser session | `connect --vault gopass --store NAME --login ...` |
| `reference/ports-and-hosts.md` | every port the product opens or expects and on which interface: the hub's port on loopback, the agent's metrics port inside its container network, the admitter's metrics port, the ssh and gcloud routes; the hosts an allowlist preset covers | none |

Out of scope for the docs: any company's own tailnet, device names, ACL files, exporter hosts or VM names. The
examples use `tag:lab`, `control-plane.example`, `lab.example`.

## I. Observability: metrics, Prometheus and Grafana

Every agent container serves `GET /metrics` in the Prometheus text format on a fixed port inside its own container
network, labelled on the container. On Docker no port is published; the host renders the same figures with
`dockingbird fleet scrape`, read from the home's status, with the labels `profile`, `agent`, `session` and `tool` (plus
`team` and `role` for a swarm's agent). The host's own figures come from `dockingbird fleet probe --json`; the fleet
scheduler's admitter serves its families on its own port, and `dockingbird fleet queue --metrics` prints them.

| Page or file | Covers |
|---|---|
| `concepts/observability.md` | the three sources (an agent's `/metrics`, the host probe, the admitter), which figures each holds, how fresh each is (an agent's figures update at its turn's end), and what none of them hold (no message text, no repository content, no names a program printed) |
| `guides/metrics.md` | read the figures by hand: `fleet scrape`, `fleet probe`, `fleet read-home`, `fleet queue --metrics`, `status --json`; the labels; the `--json` forms for a script |
| `guides/prometheus.md` | collect them: a small exporter the customer runs on each host (standard-library Python, one HTTP port, runs `fleet probe --json` and `fleet scrape` per home on an interval and serves one page), a `prometheus.yml` with one job per host and the admitter as a second job, scrape intervals that match the figures' freshness (30 s for the host, 60 s per home), a `up`-style gauge per home so an unreadable home shows as such |
| `guides/grafana.md` | import the default dashboard, point it at the Prometheus datasource, the rows it has, how to add a host, how to alert on the three signals most worth an alert (an agent's context near its compact point, a host over its load line, the queue's oldest wait) |
| `reference/metrics.md` | generated from the release's `fleet scrape` and `fleet queue --metrics` output, the only source of names and types: every family with its type, labels, unit and help line, the agent families first, the fleet families second, the exporter's meta gauges last |
| `examples/observability/exporter.py` | the exporter above; standard library only; reads the envelope's `fields`, never its `lines` |
| `examples/observability/prometheus.yml` | two jobs, placeholders for host names and ports |
| `examples/observability/dashboard.json` | the default Grafana dashboard, datasource uid as a variable, hosts and homes as template variables |
| `examples/observability/queries.md` | the general queries below, each with one line on what it answers |

Metric families the docs explain, as released; the generated reference page is the authority for every name and type.

- Agent gauges (`dockingbird_agent_` prefix): `info` (model, effort, state as labels), `turns`, `turn_running`,
  `last_turn` (state as a label), `last_turn_timestamp_seconds`, `context_used_tokens`, `context_window_tokens`,
  `compact_at_tokens`, `compactions`, `changed_paths`, `untracked_paths`, `changing`, `screen_held`,
  `sign_in_retry`, `token_failed`, `bus_losses`, `api_retries`, `model_tokens` (labels `model`, `type` in input,
  output, cache_read, cache_creation), `model_cost_usd` (label `model`), and the last result's `result_input_tokens`,
  `result_output_tokens`, `result_cache_read_tokens`, `result_cache_creation_tokens`,
  `result_reasoning_output_tokens`, `result_cost_usd`, `result_duration_seconds`, `result_turns`.
- Fleet families (`fleet_` prefix, from the admitter): `queue_depth` by priority, `reserved_millicores` and
  `reserved_mib` per host, `headroom_millicores` and `headroom_mib` per host, `gate_red`, `host_stale`,
  `interrupted`, `holds` by reason, `agent_cap`, and the counters `admissions_total`, `starts_total`,
  `queue_wait_seconds_total` per host and `agent_seconds_total` and `agent_idle_seconds_total` per role and host.
- Host figures from the probe, exported by the example exporter: cores, load against the load line, idle cores,
  free memory, swap, Docker's CPUs and memory, containers running, and per kind of process its CPU and memory.

General queries the dashboard and the queries page ship (every one works on any installation; none names a host):

| Question | Query shape |
|---|---|
| How full is each agent's context? | `dockingbird_agent_context_used_tokens / dockingbird_agent_context_window_tokens` by `agent` |
| Which agents are near their compact point? | `dockingbird_agent_context_used_tokens / dockingbird_agent_compact_at_tokens > 0.9` |
| How many agents are in each state? | `count by (state) (dockingbird_agent_info)` |
| What has each model cost so far? | `sum by (model) (dockingbird_agent_model_cost_usd)` |
| What did each model cost in the last hour? | `sum by (model) (delta(dockingbird_agent_model_cost_usd[1h]))` |
| Token throughput by type, per second | `sum by (type) (deriv(dockingbird_agent_model_tokens[15m]))` |
| Turns in the last hour per agent | `delta(dockingbird_agent_turns[1h])` |
| Agents whose sign-in is failing | `dockingbird_agent_sign_in_retry > 0 or dockingbird_agent_token_failed > 0` |
| Agents silent for over an hour | `time() - dockingbird_agent_last_turn_timestamp_seconds > 3600` |
| Queue depth by priority | `fleet_queue_depth` |
| Mean queue wait per host | `rate(fleet_queue_wait_seconds_total[1h]) / rate(fleet_admissions_total[1h])` |
| Headroom per host | `fleet_headroom_millicores`, `fleet_headroom_mib` |
| Idle share per role | `rate(fleet_agent_idle_seconds_total[1h]) / rate(fleet_agent_seconds_total[1h])` |
| Homes the exporter could not read | the exporter's `up`-style gauge `== 0` |

The agent families are gauges. `model_cost_usd` and `model_tokens` count from the start of an agent's process (Claude)
or thread (Codex) and drop to zero when it restarts, so a window query takes `delta()` or `deriv()` on a gauge and reads
such a drop as a negative change. `rate()` and `increase()` apply only to the `_total` counters.

The default dashboard's rows, top to bottom: fleet (queue depth, headroom per host, holds by reason, oldest wait);
hosts (load against the line, memory, containers); agents (a table of every agent with state, model, context fill,
last turn age, cost); cost (cumulative per model, the change over the last hour); health (sign-in retries, token
failures, bus losses, API retries, unreadable homes).

Out of the docs: the publisher's own Grafana and Prometheus deployment, its hosts, its recording rules, any
cAdvisor or node exporter wiring, a VM of the publisher's, and any figure the product keeps for its own tests.

## J. Fleet scheduling and the control plane

Two features share the word "fleet". The fleet scheduler is a pool of hosts on an organisation's PostgreSQL store that
queues swarms and admits each where it fits. The control plane is a home of its own that other computers join, so an
agent on one computer can message an agent on another. A team uses either alone or both together. Each gets its own
concept page, reference rows and cookbooks. One guide, `team-fleet.md`, installs both, `fleet-scheduler.md` runs the
pool, and a swarm's own commands are on `guides/swarms.md`.

| Page | Status | Covers | Commands and files |
|---|---|---|---|
| `concepts/fleet-scheduler.md` | new | the pool and its hosts (cores, memory, a load line, a rank, an agent cap, a power setting for a stopped VM); a workload (a swarm or a lease) with a priority P0 to P3, a reservation and an age; the gate (green or red per host); admission by priority then age; holds and why a workload waits; the worker and the admitter as the two long-running services; what a host's sample is and how often it is published (30 s) | none |
| `concepts/control-plane.md` | new | one control plane home and the computers that join it; the hub on its TCP port, on loopback until served to the private network; a bundle per computer, shown once; a member's agents get a fleet name (label, dash, name) and a fleet inbox; what the control plane keeps (a public key and a token digest per computer) and what it never holds | none |
| `guides/team-fleet.md` | split, marked "for teams" | the install path of both features: the store on PostgreSQL 18, the admin role, `org create` for the schemas, the store's projects, roles, people and members, one login role per worker and per person, `org login` on each computer as its kind, the linked checkout per home with a `fleet-link` agent; the worker and the admitter as services, with the unit text in the form `serve --unit` prints (a launchd property list on a Mac, a systemd user unit on Linux) and the `repoint` line `fleet update` runs; the control plane: initialise it with the hub's address on the private network, serve the port (section H), add a computer and paste its bundle into `node join` on that computer's home, status, remove and rejoin a computer, turn it off, what happens after a restart (the first `cp status` starts it again, members reconnect); the update order (the admin's `org create` first, the control plane next, then members and workers; `NODE_VERSION_MISMATCH` until they match); the five conditions for a member in a cloud; the limits (label length, name length, the overview's row cap, the bundle size, the call timeout) | `org login`, `org create`, `org status`, `org projects`, `org roles`, `org people`, `org members`, `fleet worker --host`, `fleet admitter`, `start --as fleet-link`, `cp init --hub-address`, `cp token --host --platform`, `node join`, `node leave`, `cp status`, `cp status --json`, `cp remove`, `cp off`, `status` |
| `guides/fleet-scheduler.md` | split, "for teams" | run work on the pool once `team-fleet.md` is done: add hosts with their cores, memory, load line, rank, agent cap and power setting; a host's policy, drain, undrain and removal; the queue, why a workload waits, its ledger; the controls (hold, release, pause, resume, cancel, done, set priority); a check run under a lease; `fleet update` across the pool in rank order | `fleet hosts add --os --cores --memory --line --rank --agent-cap --power`, `fleet hosts policy`, `fleet hosts drain`, `fleet hosts undrain`, `fleet hosts remove`, `fleet queue`, `fleet why`, `fleet ledger`, `fleet hold`, `fleet release`, `fleet pause`, `fleet resume`, `fleet cancel`, `fleet done`, `fleet set --priority`, `fleet run --cores --memory --bound`, `fleet update --release --host` |
| `reference/fleet-tools.md` | new | the ten fleet tools an agent on a joined home gets beside its bus tools: `fleet_send`, `fleet_inbox`, `fleet_read`, `fleet_ack`, `fleet_wait`, `fleet_thread`, `fleet_withdraw`, `fleet_artifact_put`, `fleet_artifact_get`, `fleet_whoami`; each with its arguments and who it can reach (a fleet agent by fleet name, an agent of the control plane's home, or the operator) | none |
| `reference/files/fleet-store.md` | new | the store's three schemas (fleet, org, work) by purpose, the role groups (`fleet_admin`, `fleet_worker`, `fleet_submitter_<project>`), the one migration order rule (control plane and workers after the admin's `org create`), the older-workers table | none |

Messages the pages end with: the fleet domain of the catalogue holds 210 entries (fleet, swarm, control plane, node,
work queue); the guide pages list the ones their steps meet, the scheduler's refusals first (a definition's check, a
login of the wrong kind, a host not in the pool), then the control plane's (a label in use, a bundle too large, a
version mismatch, a name too long).

## K. Practices the set adopts, and the evidence for each

A web review of developer documentation research and the best-regarded developer docs (2026-11-04) found measured
support for three practices and convention with strong precedent for the rest. The set adopts the fifteen below. Each
row says what the evidence is, so a later reader knows which rules to keep when they cost something.

| # | Practice | Evidence | How this set applies it |
|---|---|---|---|
| 1 | Complete, copy-and-paste examples with real output and no placeholders | Study. Meng, Steinhardt and Schubert (2018, 2020): developers scan a page for the code first, and placeholders blocked reuse; a follow-up found fewer errors and faster work from guideline-optimised docs. Postman 2020 (n above 13,500): missing docs is the top obstacle at 54.3%, better examples the top request at 66.4%. SlashData 2023 (n 16,831): examples 41%, accuracy 43%. | Rule 2 above: every step has its done line. Examples name `example-org/example-app`, never a bracketed placeholder. |
| 2 | Docs accurate at every release | Study. SlashData 2023: accurate and up to date is the first property asked of docs (43%). DORA 2023: documentation quality raises team performance by about 25% and amplifies other practices. GitBook's State of Docs 2026 (n 1,131): 30% name keeping docs in sync as their biggest problem. | The export runs from the product repository at each release; the planned onboarding check will run the documents' commands; the search build fails on a dead link or an unknown message id. |
| 3 | A quickstart that ends in a visible result inside 15 minutes | Convention. Cloudflare's style guide requires each product to have an Overview and a Get started that "state and show the working outcome". Sequin moved tutorials first after watching readers. | The quickstart ends with an agent's commit on the reader's branch; the first start's 5-minute build is stated up front. |
| 4 | A pointer to the page index on every page | Vendor report. Mintlify, 2,400 agent runs on 20 sites: failed requests per task fell from 2.23 on HTML to 0.11 on Markdown with an `llms.txt` link, with 26 to 60% fewer tokens. Ahrefs (137,210 domains): crawlers never probe for the file, so the link has to be on the page. | `llms.txt` at the root; a one-line pointer to it at the top of every page; `docs/manifest.json` for tools (section F). |
| 5 | Clean Markdown at a stable URL | Vendor reports. Cloudflare: one post at 16,180 tokens as HTML and 3,150 as Markdown. Mintlify: 83.7% of agent requests use a machine route. | The repository is Markdown; the hosted site serves each page's `.md` twin at the same path and answers `Accept: text/markdown`. |
| 6 | No content behind JavaScript, a click, a tab or a login | Independent tests. Anthropic's fetch tool returns an empty shell for client-rendered pages; Claude Code truncates near 100 KB; tabs flatten to headings and lose their commands (Chainlink, one SDK page); an unclosed code fence swallows the rest of a page. | No tabs: the Mac and Linux variants sit under their own headings; every page under 100 KB (the catalogue is split by domain for the site); a fence lint in CI. |
| 7 | Stable message ids, one catalogue entry each, the id printed with the message | Convention with precedent. Stripe (`doc_url` per error), Microsoft Entra (`error_uri`, lookup by code), PostgreSQL (SQLSTATE classes), Rust (`rustc --explain E0382`), Google AIP-193 (a constant `reason` beside mutable text). | Already the product's shape: 1,164 ids, `--verbose` shows the id, `--json` carries it, the compatibility promise covers it. Section C adds the index and the narrative pages. |
| 8 | Error text that names the cause, the fix and the next step | Guidance from support data. Google's error-message course lists the seven failures seen in support (vague, imprecise, unknown next step); clig.dev: "make errors into documentation". | Every catalogue entry has a "When:" line, a next step and an exit status. Guide pages end with the ids they may meet. |
| 9 | Search that matches flags and ids as typed | Convention. Pagefind strips punctuation unless told to keep characters; it indexes code blocks and matches word starts. Blume's guide: build a query test list from support questions and assert the top URL. | Section F: a BM25 index with `commands`, `flags`, `ids` and `tools` as boosted fields and a tokenizer that keeps `-` and `_`; a 30-query regression list in CI that opens with eleven tested queries; the Pagefind tier keeps `-` and `_` too. |
| 10 | Content kinds kept apart | Convention with adopter reports. Diátaxis (tutorial, how-to, reference, explanation): Canonical, Django and Sequin report it helped; Pigweed found literal page splits fragmented. Vale ships a 20-rule lint for it. | Section A's four folders. The split of the operator guide happens one section at a time, each with its link kept. |
| 11 | Prerequisites and a time estimate at the top of each procedure | Convention. Google's Technical Writing Two, Docker's front matter, Cloudflare: an agent "cannot begin a setup it is not equipped to reach". | Each guide opens with its prerequisites and the time its longest step takes. |
| 12 | An `AGENTS.md` with exact set-up, test and verify commands | Convention. The format is used by more than 60,000 open-source projects. | The template ships; the set-up prompt (section D) tells the agent to read it. |
| 13 | A changelog per release with deprecations flagged | Convention. Keep a Changelog: one section per version, deprecations named; Docusaurus: version docs only on a breaking change, under ten versions. | `docs/release-notes/<tag>.md` per release; the compatibility promise names removals one release ahead; no versioned doc trees until a breaking change. |
| 14 | A copy button that copies only the command | Reported failures. A leading `$` in a copy block breaks paste in every shell and names a variable in PowerShell (12 such lines on one NVIDIA page). | No prompt characters in command blocks; `console` fences only for transcripts. |
| 15 | A feedback and edit path on every page, triaged | Vendor reports. Kubeflow: feedback counts are low against page views and skew negative; Mintlify: 61% of its agent-drafted doc PRs merged. GitBook 2026: one in three assistant questions could not be answered from the docs. | "Edit this page" and "Report a problem" links to this repository's issues; zero-result search queries and unanswered agent questions logged as the to-write list. |

Three practices are left out. Versioned documentation trees cost maintenance and no breaking change exists yet.
Marketing copy has no study behind it, and the reference pages stay neutral by rule. Screenshots age with every
release, while a command and its printed line do not.

## Build order

1. Before the export runs again, its keep list gains the seven paths section A names as authored in this repository.
2. Fix the pages listed under "Fixes the pages need before the repository goes public" at the source, the hosts file
   page's three keys among them, so the next export is clean (one pull request).
3. Before the first public export, decide the support channel and write `SUPPORT.md` (five lines), and decide `harbor`
   (section A).
4. Write `llms.txt`, `docs/manifest.json`, the search build and the CI workflow (section F, tiers 1 and 2), and the
   onboarding check that runs the quickstart's commands against a fresh install. From here on every later page is
   findable the day it lands, and a command that drifts fails a check.
5. The getting-started pages, `concepts/sync-model.md`, `guides/trust-and-repo-settings.md`, `guides/daily-loop.md`
   with its new sections, the licensing guide and the two narrative troubleshooting pages for install and licence
   refusals (the three gaps and the eleven half-documented journey steps).
6. The other concepts pages with their diagrams, and the glossary.
7. The rest of the guide split of the operator guide, one section per pull request, with the generated command
   reference.
8. The fleet pages with their cookbooks (section J), the networking and integration guides (section H) and the
   observability set with the exporter, the Prometheus file, the dashboard and the queries page (section I).
9. The cookbooks marked priority 2, the FAQ, the reference pages for files, the embeddings tier.
10. Pending decisions: `LICENSE`, the legal pages, the GUI channel, the hosted store. Each is a page or a paragraph
    already named above; it ships when its decision lands.
