# Dockingbird docs for coding agents

This repository holds the customer docs of Dockingbird, which runs Claude Code and Codex agents in containers on a git
repo. Read this file when a person points you here with a question about Dockingbird or a task to do with it.

## Steps for every question

A task to set up Dockingbird on a computer has its own procedure: the block in
[docs/agent-setup-prompt.md](docs/agent-setup-prompt.md). Every other question takes these six steps, in order.

1. Read [llms.txt](llms.txt), the list of every page in reading order with a one-line summary each.
   Done when you hold the paths of one to three pages whose summaries match the question.
2. Search the sections with the question as the person typed it, or with the line or the message id on their screen:
   `python3 search/search.py "my second laptop can't activate"`. A section that holds the whole phrase ranks first,
   then exact tokens: an id, a command, a flag.
   Done when the first result names a page and a heading: for that question,
   `docs/guides/licensing.md#move-a-seat-to-a-new-laptop`.
3. Open the one page the search named, at that heading, and read the section whole.
   Done when the commands that answer the question and their done lines are in front of you.
4. Read that page's "When it fails" list.
   Done when you know each message id its steps can print and the catalogue entry of each.
5. Run the cookbook that matches the task, when `examples/` holds one: its commands in order, as the page shows them.
   Done when the done line of every step has printed on screen.
6. Report each command you ran, the done line it printed, and the message id of any step that stopped.
   Done when the person can repeat every step from your report alone.

## Where each question goes

The first words of each row name the question. Open the first page, then the others when it sends you there.

| Question | Open first | Then |
|---|---|---|
| Install and licensing: the key, a seat, a trial | [install](docs/getting-started/install.md) | [activate](docs/getting-started/activate.md), [licensing](docs/guides/licensing.md), [install fails](docs/troubleshooting/install-fails.md) |
| First run and the daily loop: init, the first start, status, sync, stop | [first run](docs/getting-started/first-run.md) | [daily loop](docs/guides/daily-loop.md), [sync model](docs/concepts/sync-model.md) |
| Delegating a task: start, wait, inbox, read, send, results | [delegating tasks](docs/guides/delegating-tasks.md) | [delegate_and_wait.py](examples/tasks/delegate_and_wait.py) |
| Connections: a GitHub repo, a folder, a database, an MCP server, a program, a browser | [connections](docs/guides/connections.md) | [databases](docs/guides/databases.md), [GitHub](docs/guides/github.md) |
| Second computer: a host over ssh, or a cloud VM | [hosts](docs/guides/hosts.md) | [two Macs](examples/two-macs-ssh/README.md), [cloud VM](examples/cloud-vm-gcloud/README.md) |
| Team fleet and the control plane | [team fleet](docs/guides/team-fleet.md) | [fleet scheduler](docs/guides/fleet-scheduler.md), [swarms](docs/guides/swarms.md), [control plane](docs/concepts/control-plane.md) |
| Metrics | [metrics](docs/guides/metrics.md) | [Prometheus](docs/guides/prometheus.md), [metrics reference](docs/reference/metrics.md) |
| Updates | [updates](docs/guides/updates.md) | [update with agents running](examples/update-with-agents-running/README.md) |
| Message id on screen | `docs/troubleshooting.md#` followed by the id in lower case | the id's domain index in `docs/troubleshooting/`, such as [install](docs/troubleshooting/install.md) |
| `--json` or MCP integration | [the envelope](docs/reference/integration/json.md) | [exit codes](docs/reference/integration/exit-codes.md), [MCP tools](docs/reference/integration/mcp.md), [MCP server](docs/guides/mcp-server.md) |

A command's arguments are on its help screen, `dockingbird <command> -h`, and in
[docs/reference/commands.md](docs/reference/commands.md).

## Words these docs use

| Word | Meaning |
|---|---|
| done line | The exact line Dockingbird prints when a step worked. Every step of every guide and cookbook names one. |
| message id | The upper-case name of one message, such as `LICENSE_SEATS_FULL`. `--verbose` prints it in brackets, `--json` carries it as `id`, and its entry is `docs/troubleshooting.md#license_seats_full`. |
| cookbook | One task from start to end, in `examples/<name>/README.md`, each command followed by its done line. |
| home | The folder `DOCKINGBIRD_HOME`, `~/.local/share/dockingbird` by default, with the containers, volumes and image that belong to it. |
| the bus | The messages that carry tasks, questions, answers and files between a person and the agents. `start`, `send`, `wait`, `inbox`, `read` and `results` move them. |

## Rules for every step

1. A step is done when its done line is on screen. A step that printed something else is not done.
2. A failing step stops at its message id. Open the id's entry, read its "Next step:", and report both before you try
   anything else.
3. A start from your own shell uses `dockingbird start "the task"`. The agent then works on the bus and needs no
   screen. `dockingbird claude` and `dockingbird codex` open the tool's screen in a person's terminal.
4. A script reads the `--json` envelope's `id`, `fields` and `exit_code`. The words in `lines` change between releases.
5. The owner of the computer runs the install line and `dockingbird license activate`, and pastes the license key at
   the hidden prompt. The key stays out of every command line, file, chat and report, so never ask for it.
6. The owner signs each tool in at their own terminal with `dockingbird login claude` or `dockingbird login codex`.
   A sign-in shows a link and asks for a code.
7. `dockingbird clean --all` removes everything Dockingbird made, the home's files among them, and gives the seat
   back. It runs on the owner's word, as does `dockingbird license deactivate`.
