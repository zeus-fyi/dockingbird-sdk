---
title: Delegating tasks
summary: Hand an agent a task on the bus, wait for it, read its messages, answer its questions, send more work and save its files.
audience: daily
commands:
  - start
  - wait
  - inbox
  - read
  - questions
  - answer
  - send
  - results
  - search
  - set
  - stop
  - claude -p
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Delegating tasks

Give an agent a task, then do something else. The agent runs in its own container on a copy of your branch, with no terminal of its own. It tells you what it did in messages, and they wait in your inbox until you read them. All the commands below speak as one client of yours, the host client, so a question from any agent shows up in one inbox and your replies carry your name.

## Before you start

- Dockingbird is set up and Docker Desktop is running. `dockingbird status` prints a first line such as `Dockingbird 0.15.3, signed in to Claude and Codex`.
- The tool you delegate to has a sign-in or a saved API key. An agent without a terminal cannot sign in, so `start` refuses a tool that has neither (`SIGNIN_NEEDED`). Fix it with [sign-in and API keys](sign-in-and-api-keys.md).
- You stand in a git repository with a commit. The agent starts from your last commit.

## 1. Hand over the task

```bash
dockingbird start "Fix the failing test"
```

The command prints a line for each step it waits on, then returns once the agent runs, about half a minute later. It runs Claude unless you add `--harness codex`. `--task -` reads the task from standard input, and `--file PATH` attaches a text file (repeatable). Done when it prints the agent, the thread and the way to follow it.

```text
claude-1 started on myapp (main).
Thread <id>. Watch: dockingbird wait claude-1
```

Message id `AGENT_STARTED_BUS`. Without a task the agent starts idle and says `Send it a task: dockingbird send claude-1 TEXT` (`AGENT_STARTED_IDLE`). `--cpus 2` and `--memory 4g` limit the agent's container. `--as NAME` names the agent. A name whose agent ended picks up where it left off.

## 2. Wait for it

```bash
dockingbird wait claude-1
```

`wait` returns at once with a message from the agent that you have not seen yet. Otherwise it waits for the next one, 25 seconds by default, or the `--seconds N` you give. Each message is told once. Done when it prints the kind, the sender and the subject.

```text
status from claude-1: turn 1
Read it: dockingbird read 1
```

Message id `WAIT_DELIVERY`. After each turn an agent sends a status message with its final text at priority P3, the lowest. An error comes at once at P1, so it sorts before every summary, task and question. When time runs out, `wait` says so and counts what waits (`WAIT_TIMED_OUT`).

```text
Nothing new in 45 s. 2 messages wait in your inbox: dockingbird inbox
```

## 3. Read the inbox

```bash
dockingbird inbox
```

Messages sort by priority, from P0 down to P3, and the newest comes first inside a priority. You see one page at a time. Each message gets a row number the first time you see it, and it keeps that number while it waits. Reading or answering other messages never renumbers it. The numbers start again at 1 once the inbox is empty. A row looks like this.

```text
  1  claude-1  status  P3  turn 1  2 min ago
```

When nothing waits, the line is `Nothing is waiting in your inbox.` (`INBOX_EMPTY`).

| Option | What it shows |
|---|---|
| `--priority P1` | Only messages of that priority, `P0` to `P3` |
| `--questions` | Only the questions your agents asked |
| `--page 2` | The second page of 20 |
| `--all` | Every row |
| `dockingbird inbox claude-2` | What other agents and you sent that agent, with no row numbers |
| `--clear` | Marks the notices of stopped agents read and closes their open questions; nothing is deleted |

## 4. Read a message

```bash
dockingbird read 1
```

Done when the header line prints, followed by the whole body and the files it names.

```text
status from claude-1, P3: turn 1
```

Message id `READ_HEADER`. Reading marks the message read. A notice that needs no answer then leaves your inbox, unless you add `--keep`, which shows it and leaves it unread.

Looking for an old message? `dockingbird search "closed issues"` lists the newest messages, in every thread of your agents, whose subject or body holds all the words. It prints no body. Take the row's sender and subject, then use `read` for what came to you.

## 5. Answer a question

A question an agent asks you leads `dockingbird status` until you answer it. List the open ones, then answer one.

```bash
dockingbird questions
dockingbird answer 3 --option 2
dockingbird answer 3 "Use Vue."
```

`questions` prints one page, oldest first, with each row's agent, kind, first line, choices and age. `dockingbird questions 3` shows one whole. When none waits, the line is `No agent is waiting for your answer.` (`QUESTIONS_EMPTY`). `answer` takes an option number or your own words and prints the answer it recorded.

```text
claude-1's question 3 answered by you: Use Vue.
```

Message id `ANSWERED`. An agent at a terminal shows its tool's own dialog on its screen, where you pick the answer with the arrow keys and Enter, and `answer` says so. A question an agent asked over the bus gets your answer as a reply it reads like any other.

## 6. Send more work

```bash
dockingbird send claude-1 "Yes, include the closed ones."
```

A plain message answers the agent's one open question, or is a new task when it asked none. Two open questions are refused (`SEND_AMBIGUOUS`): say which with `--reply-to ROW`, where ROW is the question's row in `dockingbird inbox`, not its number in `questions`. `--file PATH` attaches a text file. `dockingbird send claude-1 --withdraw 3` takes a message back. Done when the line names the kind, the agent and the message.

```text
Sent {kind} to claude-1 (message {value}).
```

Message id `SENT`. `{kind}` is the message kind and `{value}` identifies the message. An agent that has ended gets the message when you continue it with the command the line names.

## 7. Save its files

```bash
dockingbird results claude-1 --to ../handoff
```

`results` saves the files the agent attached in its task thread under `DOCKINGBIRD_HOME/results/claude-1/`. Each file is named by the first 16 hex digits of its SHA-256 and its name, readable only by you, and never overwritten. `--to DIR` also copies them into a folder of yours outside `DOCKINGBIRD_HOME`. Done when each saved file prints its type and path, and the copy line follows.

```text
The copy in {where} is yours, outside dockingbird clean.
```

Message ids `RESULTS_WRITTEN` and `RESULTS_COPY_OWN`. `{where}` is the folder you gave. The thread is the one the start opened, so a follow-up's files are saved too. An agent's "done" is its own report, never Dockingbird's check: read its results before you rely on them.

## 8. Change its model or effort

```bash
dockingbird set claude-1 --effort xhigh
```

The change applies from the agent's next turn, never to one in flight. Claude's levels are `low`, `medium`, `high`, `xhigh` and `max`. `--model NAME` and `--compact-at 600k` work the same way. Done when the line prints.

```text
claude-1: model {model}, effort xhigh; applies from its next turn.
See it: dockingbird status claude-1
```

Message id `SET_DONE`. A change lasts only while the agent runs.

## 9. Stop it

```bash
dockingbird stop claude-1
```

The agent stops. Its thread, its files and its results stay.

## One-shot answers

`dockingbird claude -p "Summarize the open TODOs"` and `dockingbird codex exec "Fix the tests"` resume or start an agent that takes exactly those arguments and print only the tool's answer on standard output. Dockingbird's own lines go to standard error. A script that pipes nothing into a one-shot closes its input with `< /dev/null`, or Codex waits for input that never ends. With `--json` before the tool's name, the final envelope is JSON, described in [the envelope](../reference/integration/json.md). An agent sends to another agent by name; to read what they sent each other, `dockingbird inbox claude-2`. The model is in [agents and the bus](../concepts/agents-and-the-bus.md).

## When it fails

- A start for a tool with no sign-in or key ends with [`SIGNIN_NEEDED`](../troubleshooting.md#signin_needed). Run `dockingbird login claude` first.
- When Dockingbird refuses the task after the agent is already running, [`AGENT_STARTED_TASK_REFUSED`](../troubleshooting.md#agent_started_task_refused) says the agent runs without it. Send it a task with `dockingbird send`, or stop it.
- Nothing arrived while `wait` ran: [`WAIT_TIMED_OUT`](../troubleshooting.md#wait_timed_out). Run `wait` again.
- [`INBOX_EMPTY`](../troubleshooting.md#inbox_empty) says no message waits for you, or none matches your `--priority` or `--questions`.
- Two open questions make a plain `send` ambiguous. [`SEND_AMBIGUOUS`](../troubleshooting.md#send_ambiguous) asks for `--reply-to` with the question's row in `dockingbird inbox`.
- Sending to an agent that runs at a terminal with no bus tools prints [`SEND_NOT_ON_BUS`](../troubleshooting.md#send_not_on_bus). Start one with `dockingbird start`.
- An agent with no attached files gives [`RESULTS_NONE`](../troubleshooting.md#results_none).
- When a file name in your folder is taken by something else, [`RESULTS_TAKEN`](../troubleshooting.md#results_taken) saves nothing there. Use another folder with `--to`.
- A `--to` folder that does not exist, or lies inside Dockingbird's own folder, prints [`RESULTS_TO_INVALID`](../troubleshooting.md#results_to_invalid).
- `dockingbird set` on an agent that has stopped prints [`SET_NOT_RUNNING`](../troubleshooting.md#set_not_running). Pick the agent up first.
