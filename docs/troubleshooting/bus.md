---
title: "Troubleshooting index: the bus"
summary: "The 78 message ids about tasks on the bus: send, wait, the inbox, read, questions and results, each with when it appears."
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: the bus

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 78 ids about tasks on the bus: send, wait, the inbox, read, questions and results.

| Id | When it appears |
|---|---|
| [`INSTRUCTIONS_UNREADABLE`](../troubleshooting.md#instructions_unreadable) | Your rules file for Claude or Codex (in Dockingbird's `instructions` folder) can't be read: it isn't a plain text file, is too large, or is a link. |
| [`INSTRUCTIONS_TIMED_OUT`](../troubleshooting.md#instructions_timed_out) | You started an agent, and saving your rules file for Claude or Codex for it took longer than Dockingbird waits, usually because the computer was busy. |
| [`QUESTION_DEFERRED_UNAVAILABLE`](../troubleshooting.md#question_deferred_unavailable) | An agent asked you a question while Dockingbird was restarting for an update, and Dockingbird couldn't record it in time. |
| [`DELIVERY_HELD_IN_SCREEN`](../troubleshooting.md#delivery_held_in_screen) | A message you or another agent sent has waited a while at the agent's screen: someone is typing in it, its tool hasn't started yet or is still working, or its screen is still drawing. |
| [`TURN_UNSIGNALLED`](../troubleshooting.md#turn_unsignalled) | A message you or another agent sent went into a Codex agent's screen, and no sign came that its work was done: nothing was drawn after it for the time a tool takes to show it took a message, or what was drawn then stopped for that long. |
| [`TURN_COMPLETION_UNSEEN`](../troubleshooting.md#turn_completion_unseen) | A message went into a Codex agent's screen and the agent took it: its screen showed it at work. |
| [`TURN_INTERRUPTED_BY_OWNER`](../troubleshooting.md#turn_interrupted_by_owner) | While an agent worked on a message, the owner pressed Esc or Ctrl-C in its screen, and the next thing it worked on was a line of the owner's own: one they sent while it worked, or right after the key. |
| [`TURN_DEADLINE_IN_OWNERS_TURN`](../troubleshooting.md#turn_deadline_in_owners_turn) | While an agent worked on a message, the owner pressed Esc or Ctrl-C in its screen, and the agent then worked on a turn of the owner's own there. |
| [`RELAY_START_FAILED`](../troubleshooting.md#relay_start_failed) | A command started Dockingbird while a connection exists, and Docker refused to start the small container that carries the connections' SSH traffic to their hosts. |
| [`INSTRUCTION_FILE_REFUSED`](../troubleshooting.md#instruction_file_refused) | You started an agent with `--agent-md` or `--claude-md` (or picked up one that started with it), and the file is missing, a link, not a regular file, larger than the limit, not UTF-8, or has a Dockingbird credential. |
| [`INSTRUCTION_FILE_UNREAD`](../troubleshooting.md#instruction_file_unread) | You started an agent with `--agent-md` or `--claude-md` where its tool would not read that file at startup: a scratch folder, Codex with `--claude-md`, a config's command whose repo settings don't load for Claude (its `repo_settings` is off, or the checkout isn't trusted), or Codex in a trusted checkout whose branch has `AGENTS.override.md`. |
| [`INSTRUCTION_FILE_CARRIED`](../troubleshooting.md#instruction_file_carried) | You picked up an agent with `--as`, and it started with `--agent-md` or `--claude-md`: an agent keeps its instruction files for its whole life, so this start reads the same file again from the same path. |
| [`INSTRUCTION_FILE_FIXED`](../troubleshooting.md#instruction_file_fixed) | You picked up or reconnected to an agent with `--as` and gave `--agent-md` or `--claude-md` another file than the one it started with, or a file it started without. |
| [`INSTRUCTION_FILE_SAVED`](../troubleshooting.md#instruction_file_saved) | A new agent's start found that an earlier agent had changed the AGENTS.md or CLAUDE.md that `--agent-md` or `--claude-md` gave it. |
| [`INBOX_ROW_UNKNOWN`](../troubleshooting.md#inbox_row_unknown) | You gave a row number no message in your inbox has now, or your inbox is empty. |
| [`INBOX_ROW_CONSUMED`](../troubleshooting.md#inbox_row_consumed) | You gave a row number of a message another reader of this home (a swarm's reader, the fleet engine or a plain `dockingbird read`) read since your inbox showed it, which took it out of the inbox. |
| [`INBOX_ROW_RESOLVED`](../troubleshooting.md#inbox_row_resolved) | You gave a row number of your inbox instead of an id. |
| [`DELIVERY_EXCEEDS_LINE`](../troubleshooting.md#delivery_exceeds_line) | An agent asked to read a message, and not even the shortest page of it fits in one answer of the agent's tools (they are given a most characters an answer may have). |
| [`SEND_AMBIGUOUS`](../troubleshooting.md#send_ambiguous) | You sent an agent a plain message while two or more of its questions to you are still unanswered, so Dockingbird can't tell which one it answers. |
| [`SEND_GROUP_CONFLICT`](../troubleshooting.md#send_group_conflict) | You ran `dockingbird send --all` with `--role` or `--swarm` too: `--all` already sends to every live agent, so Dockingbird can't tell which group you meant. |
| [`SEND_GROUP_NO_REPLY`](../troubleshooting.md#send_group_no_reply) | You sent to a group (`--all`, `--role` or `--swarm`) with `--reply-to` or `--kind answer`: an answer goes to the one agent that asked, never to a group. |
| [`SEND_REPLY_ANOTHER_AGENT`](../troubleshooting.md#send_reply_another_agent) | You replied with `--reply-to` to a message in your inbox that is another agent's question, not one of the agent you sent to: the words would have answered the other agent. |
| [`SEND_NOT_ON_BUS`](../troubleshooting.md#send_not_on_bus) | You sent a message to an agent that runs in a terminal without the bus's read tool: Dockingbird's default environment, or a config whose tool set lacks it. |
| [`SEND_PAYLOAD_INVALID`](../troubleshooting.md#send_payload_invalid) | `dockingbird send --kind KIND --payload JSON` with a payload larger than the bound: nothing was sent; give the kind's fields as one JSON object. |
| [`RESULTS_FULL`](../troubleshooting.md#results_full) | Saving an agent's results would take its results folder past its limit, so that file was not saved; `--to` saves into a folder of your own, whatever is already in it. |
| [`RESULTS_TAKEN`](../troubleshooting.md#results_taken) | Saving an agent's results found that file's name already taken in the folder by something else: a link, a folder, a file with other content, or the same name in other letter case. |
| [`RESULTS_COPY_OWN`](../troubleshooting.md#results_copy_own) | You copied an agent's results into a folder of your own with `--to`. |
| [`RESULTS_TO_INVALID`](../troubleshooting.md#results_to_invalid) | You gave `--to` a folder that doesn't exist, isn't a folder, or is inside Dockingbird's own folder. |
| [`SEND_TEXT_CONTROL`](../troubleshooting.md#send_text_control) | You sent a text with a control character a message can't carry, such as the escape in a terminal's colour codes, or a NUL. |
| [`INBOX_ROW`](../troubleshooting.md#inbox_row) | You ran `dockingbird inbox`: each row is one message waiting for you, in the inbox's order (priority, then age), with the number it got when you first saw it, here or from `dockingbird wait`; it keeps that number while it waits, and the numbers start at 1 again once your inbox is empty. |
| [`INBOX_EMPTY`](../troubleshooting.md#inbox_empty) | You ran `dockingbird inbox` and no message is waiting for you. |
| [`INBOX_MORE`](../troubleshooting.md#inbox_more) | Your inbox has more messages than one page shows. |
| [`SEARCH_ROW`](../troubleshooting.md#search_row) | You ran `dockingbird search TEXT`: one line per message whose subject or body has every word of TEXT, the newest first, in every thread of your agents: who sent it, its kind, its subject and how long ago. |
| [`SEARCH_EMPTY`](../troubleshooting.md#search_empty) | You ran `dockingbird search TEXT`, and no message has every word of TEXT. |
| [`SEARCH_MORE`](../troubleshooting.md#search_more) | You ran `dockingbird search TEXT`, and more messages have its words than one page shows. |
| [`INBOX_PAGE_MORE`](../troubleshooting.md#inbox_page_more) | You ran `dockingbird inbox --page N` and later pages hold more messages: how many, and the command that shows the next page, with the same `--priority` or `--questions` you gave. |
| [`INBOX_PAGE_EMPTY`](../troubleshooting.md#inbox_page_empty) | You ran `dockingbird inbox --page N` for a page past the last one: nothing is on it, and the message says how many pages your inbox (or the messages that match your `--priority` or `--questions`) fills. |
| [`INBOX_PAGE_ZERO`](../troubleshooting.md#inbox_page_zero) | You ran `dockingbird inbox --page 0`. |
| [`INBOX_SINCE_INVALID`](../troubleshooting.md#inbox_since_invalid) | You ran `dockingbird inbox --all --since TIME` with a TIME that isn't a date and time with its offset from UTC, such as `2026-11-07T00:00:00+00:00`. |
| [`INBOX_NAME_OPTION`](../troubleshooting.md#inbox_name_option) | You ran `dockingbird inbox NAME` with an option that only works on your own inbox: `--priority`, `--questions`, `--page` or `--clear`. |
| [`INBOX_SWARM_INVALID`](../troubleshooting.md#inbox_swarm_invalid) | You gave `dockingbird inbox` or `dockingbird read` a `--swarm` value with an item that isn't a swarm's name (lowercase letters, digits and `-`, up to 63 characters), or an empty one, as two commas in a row or one at the end make. |
| [`INBOX_ENGINE_INVALID`](../troubleshooting.md#inbox_engine_invalid) | You gave `dockingbird inbox` or `dockingbird read` an `--engine` value with an item that isn't a workload's id: a UUID in lower case, as `dockingbird swarm list --json` shows it. |
| [`INBOX_ROW_NOT_OWNED`](../troubleshooting.md#inbox_row_not_owned) | You read a message with `--swarm`, `--engine` or `--no-swarm`, and by this home's swarm record its sender is outside them: on a home that others share too, one of their agents sent it. |
| [`INBOX_CLEAR_UNSCOPED`](../troubleshooting.md#inbox_clear_unscoped) | You ran `dockingbird inbox --clear` with no `--swarm`, `--engine` or `--no-swarm` on a home whose swarm record has two or more swarms, such as a fleet engine home that others share: one clear would settle everyone's stopped agents' notices at once. |
| [`INBOX_ROWS_NOT_KEPT`](../troubleshooting.md#inbox_rows_not_kept) | Your inbox has so many open messages that their row numbers would take Dockingbird's `state.json` past the size it reads, so the numbers shown last for this command only. |
| [`INBOX_CLEARED_ROW`](../troubleshooting.md#inbox_cleared_row) | You ran `dockingbird inbox --clear`: one row for each item it cleared that an agent that has stopped left you, with the agent, the kind, `read` for a notice it marked read or `closed` for a question it closed, and the id that still reads it. |
| [`INBOX_CLEARED`](../troubleshooting.md#inbox_cleared) | You ran `dockingbird inbox --clear` and it cleared what agents that have stopped left you: their notices are marked read and their open questions closed. |
| [`INBOX_CLEAR_NOTHING`](../troubleshooting.md#inbox_clear_nothing) | You ran `dockingbird inbox --clear` and no agent that has stopped left a notice or an open question in your inbox, so nothing changed. |
| [`INBOX_CLEAR_LEFT`](../troubleshooting.md#inbox_clear_left) | You ran `dockingbird inbox --clear` and agents that have stopped left messages that ask you to act: a task, a review request or work handed over. |
| [`QUESTION_ROW`](../troubleshooting.md#question_row) | You ran `dockingbird questions`: each row is one question an agent is asking you, with the number it got when you first saw it (kept until it is answered), who asks, what kind of question it is, its text, its options numbered, and how long ago. |
| [`QUESTIONS_EMPTY`](../troubleshooting.md#questions_empty) | You ran `dockingbird questions` and no agent is waiting for an answer. |
| [`QUESTIONS_MORE`](../troubleshooting.md#questions_more) | More questions are open than one page shows; a question after the page gets its row once earlier ones are answered. |
| [`QUESTION_ROW_UNKNOWN`](../troubleshooting.md#question_row_unknown) | You gave `dockingbird questions` or `dockingbird answer` a row number no open question has: a question keeps its number until it is answered, and the id `dockingbird --json questions` shows always works. |
| [`QUESTION_NOT_OPEN`](../troubleshooting.md#question_not_open) | You gave `dockingbird answer` the id of a question that is no longer open, or `dockingbird send --reply-to` answered a question someone else had answered meanwhile, and nothing was sent. |
| [`QUESTION_HEADER`](../troubleshooting.md#question_header) | You ran `dockingbird questions ROW`: who asks, what kind of question it is and which tool; its text and options follow. |
| [`QUESTION_OPTION_ROW`](../troubleshooting.md#question_option_row) | One option of the question shown: its number, which `dockingbird answer --option N` takes, its label and, in the described form, what the tool says about it. |
| [`QUESTION_ANSWER_HINT`](../troubleshooting.md#question_answer_hint) | The last line of a question shown whole: the command that answers it, by an option's number or, in the typed form, in words. |
| [`ANSWERED`](../troubleshooting.md#answered) | You ran `dockingbird answer` and the answer was recorded for the agent. |
| [`ANSWER_NEEDS_ONE`](../troubleshooting.md#answer_needs_one) | You ran `dockingbird answer` without an option number or an answer, or with both; give one of them. |
| [`ANSWER_OPTION_UNKNOWN`](../troubleshooting.md#answer_option_unknown) | You picked an option number the question does not have; the line says how many options it has. |
| [`ANSWERED_NOT_SENT`](../troubleshooting.md#answered_not_sent) | You answered a Codex agent's turn end on the bus; the answer was recorded, but sending it as the agent's next turn failed (the line quotes why; the lost form: the docker call behind the send gave no answer, and `--verbose` shows its detail). |
| [`ANSWER_ONE_LINE`](../troubleshooting.md#answer_one_line) | You answered a question of an agent at a terminal with a text that has a line break, a tab or another control character; `dockingbird ui` types the answer into the tool's dialog, where a line break ends it early and a tab moves to another question, so write it on one line. |
| [`READ_HEADER`](../troubleshooting.md#read_header) | You ran `dockingbird read`: the message's kind, sender, priority and subject. |
| [`READ_BODY_LINE`](../troubleshooting.md#read_body_line) | You ran `dockingbird --json read`: each envelope carries a piece of the message's body, in order, so the agent's text never stands outside an envelope. |
| [`BODY_ARTIFACT_ROW`](../troubleshooting.md#body_artifact_row) | The message you read names a file an agent attached: its name, type, size and id. |
| [`SENT`](../troubleshooting.md#sent) | You ran `dockingbird send` and the message went; the line shows its id. |
| [`SENT_QUESTION_OPEN`](../troubleshooting.md#sent_question_open) | You ran `dockingbird send` and the agent has bus questions to you that are still open. |
| [`WITHDRAWN`](../troubleshooting.md#withdrawn) | You ran `dockingbird send --withdraw`: the message's deliveries that no agent had taken yet are withdrawn. |
| [`EXPECTED`](../troubleshooting.md#expected) | You ran `dockingbird expect KIND --from NAME --within SECONDS`: Dockingbird now watches for the message you expect. |
| [`EXPECTATIONS`](../troubleshooting.md#expectations) | You ran `dockingbird expect --list`: one line per expectation of yours, open ones, or every state with `--closed`, newest first. |
| [`EXPECTATION_WITHDRAWN`](../troubleshooting.md#expectation_withdrawn) | You ran `dockingbird expect --withdraw ID`: the open expectation is withdrawn and sends no alert. |
| [`WAIT_DELIVERY`](../troubleshooting.md#wait_delivery) | You ran `dockingbird wait` and a message you hadn't seen yet was waiting, or arrived while it waited, wherever it sorts in your inbox. |
| [`WAIT_TIMED_OUT`](../troubleshooting.md#wait_timed_out) | You ran `dockingbird wait` and no message you hadn't seen arrived before its time ran out. |
| [`WAIT_ENDED`](../troubleshooting.md#wait_ended) | You ran `dockingbird wait NAME` for an agent that has stopped, or it stopped while you waited, and its work is kept, so nothing new comes from it until it is continued with the command the line names. |
| [`RESULTS_WRITTEN`](../troubleshooting.md#results_written) | You ran `dockingbird results`: each line is one file it saved from the agent's task thread, with the file's type. |
| [`RESULTS_NONE`](../troubleshooting.md#results_none) | You ran `dockingbird results` and the agent's task thread has no attached files yet. |
| [`RESULTS_NO_THREAD`](../troubleshooting.md#results_no_thread) | You ran `dockingbird results` for an agent this Mac started without a task, or did not start, so no task thread is recorded for it. |
| [`WAITING_ENDED_ROW`](../troubleshooting.md#waiting_ended_row) | `dockingbird status` shows an agent that has ended while messages were still waiting for it, after the questions: how many wait, what the first of them is (its kind and subject; after `dockingbird stop` in the middle of a task, that is the task the agent was working on), and the command that continues the agent, which hands it them. |
