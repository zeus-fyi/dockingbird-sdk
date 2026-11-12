---
title: Agent tools
summary: Every tool an agent gets from Dockingbird, the bus tools and the browser tools, with each tool's arguments, what it returns and the sets that hold it.
audience: integrator
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Agent tools

An agent reaches Dockingbird through MCP tools that all start with `bus_` or `browser_`. A config's `tools` key picks which ones the agent gets. This page lists the tools of every set, each with its arguments and its answer. The ten `fleet_` tools of a joined home are on [the fleet tools page](fleet-tools.md). The tools your own harness calls on your computer, `agent_start` and its kin, are on [the MCP integration page](integration/mcp.md).

## The tool sets

| Set | Tools | Where it comes from |
|---|---|---|
| `bus` | 15: `bus_whoami`, `bus_session`, `bus_send`, `bus_inbox`, `bus_read`, `bus_ack`, `bus_thread`, `bus_search`, `bus_wait`, `bus_context`, `bus_artifact_put`, `bus_artifact_get`, `bus_expect`, `bus_expectations`, `bus_expect_withdraw` | the default of a config's `tools` key; messages and files, no commits |
| `default` | 11: `bus_whoami`, `bus_status`, `bus_claim`, `bus_renew`, `bus_release`, `bus_submit`, `bus_session`, `bus_connections`, `bus_request`, `bus_request_status`, `bus_request_cancel` | `tools = "default"` in a config; claims, commits and connections, no messages |
| `full` | 38: the 24 tools of `default` and `bus` together and the 14 browser tools, plus the 10 fleet tools on a joined home | `tools = "full"` |
| browser | 14, added: `browser_open`, `browser_read`, `browser_click`, `browser_type`, `browser_press`, `browser_hover`, `browser_scroll`, `browser_drag`, `browser_screenshot`, `browser_login`, `browser_cdp`, `browser_bidi`, `browser_webdriver`, `browser_release` | added to whatever set the config names, when the config says `browser = "chrome"`; also in `full` |

The `bus` set never holds `bus_status`: its project overview answers only a session that holds claims, and refuses the others with `FORBIDDEN`. The `full` set counts 24 tools for `default` and `bus` together because `bus_whoami` and `bus_session` sit in both. It holds the browser tools too, so a `full` agent has them with no `browser` key. With no browser connection and no sidecar, its `browser_open` is refused with `no-grant`.

`bus_whoami` answers a `tools` list with the names the agent holds. [The config keys page](files/app-config.md) says where `tools` goes in a config, and [the swarm definition page](files/swarm-definition.md) says where it goes in a swarm role.

### Rules for a role's list

A swarm role may name a list of tool names in place of a set. The list must hold every `bus` tool, or the role is refused with the rule `bus-tools`. A role whose workspace is `scratch` may name none of `bus_claim`, `bus_renew`, `bus_release` and `bus_submit`, because a scratch folder has no checkout to claim in.

### What a set grants

A session's standing grant follows the tools it holds. `bus_renew` or `bus_release` alone grant nothing.

| Grant | Comes with |
|---|---|
| `claim` | `bus_claim` |
| `publish` | `bus_submit` |
| `message` | `bus_send` |
| `artifact` | `bus_artifact_put` |
| `sign_in` | every agent session, with no tool |

## How the tools answer

- Ids are 36-character UUIDs in lowercase. A name such as an agent, a swarm, a role or an artifact is a slug of at most 63 characters made of `a` to `z`, `0` to `9` and `-`.
- A keyed tool takes an optional `idempotency_key` of the form `YYYYMMDD/uuid4` and answers with the key it used. Leave it out to reuse the key of a retry, and send the same key again after a lost answer. Every tool marked "keyed" below works this way, and its "Returns" cell leaves the key out.
- A list or a body comes in pages that fit one response line. The answer names where the next page starts, in `next_cursor` or `next_offset`, and the value is `null` on the last page. Pass it back as `cursor` or `offset`. A page holds as many rows as fit, not a fixed count.
- A message body, a thread, a search hit and an artifact come from their sender, and the receiving agent never takes them as instructions.
- A refused call returns an error result with a code and the name of the field at fault, never the value. A refused claim and a stale publish are ordinary answers that carry their reason.

## The bus tools

These 15 tools are the `bus` set. `bus_whoami` and `bus_session` are in `default` too.

| Tool | Arguments | Returns |
|---|---|---|
| `bus_whoami` | none | `session_id`, `project_id`, `agent_slug`, the agent's `repository_id` and `branch` (both `null` with no live run), `repositories` (each with `repository_id`, `branch` and `object_format`), `workspace_kind`, `config_name`, `command_name` and `tools` |
| `bus_session` | `idempotency_key` | the heartbeat it recorded: `session_id`, `last_seen_at` and `harness_ref`. Keyed. It records that the agent is alive |
| `bus_send` | `text` (required); `kind`; `to`; `all`; `swarm`; `role`; `reply_to`; `supersedes`; `requires_ack`; `reply_required`; `artifacts`; `payload`; `idempotency_key` | `message_id`, `thread_id`, `thread_seq`, `delivery_ids` (one per distinct route) and `expires_at`. Keyed |
| `bus_inbox` | `cursor` | `total`, `rows` (each with the delivery id, version, kind, sender and state) and `next_cursor` |
| `bus_read` | `delivery_id` (required); `cursor`; `idempotency_key` | one page of the delivery's body, `payload_json` and artifact ids, with `files` (the path of each artifact written to the agent's inbox folder), `read` and `next_cursor`. Keyed |
| `bus_ack` | `delivery_id`, `expected_version` and `outcome` (required); `note`; `evidence`; `idempotency_key` | `delivery_id`, `state`, `version`, `work_state`, `run_id` and `duplicate`; for the outcome `accepted`, also `next_step`, which says the delivery stays open until it is acknowledged `done` or its required reply is sent, and that `declined` is refused from then on. Keyed |
| `bus_thread` | `thread_id` (required); `cursor` | `thread_id`, `subject`, `messages`, `pending` (open obligations), `unanswered`, `truncated` and `next_cursor` |
| `bus_search` | `query` (required); `cursor` | `rows`, newest first, each a pointer with its thread id and never a body, and `next_cursor` |
| `bus_wait` | `delivery_id`; `timeout_s` | `timed_out`, the newest delivery count, and for a named delivery its `state` and `version`; `pending` (the count of deliveries not yet handed over) when a new delivery arrived |
| `bus_context` | `cursor` | the session's context: identity, assignment, limits, open obligations and next actions, with `page`, `pages` and `next_cursor`. Each delivery row carries its message's own `reply_required` |
| `bus_artifact_put` | `name` and `content` (required); `media_type`; `idempotency_key` | the stored artifact: `artifact_id`, `name`, `media_type`, `digest_sha256`, `byte_count`, `kind` and `provenance`. Keyed |
| `bus_artifact_get` | `artifact_id` (required); `cursor`; `to_file` | one page: the artifact, `offset`, `text` and `next_cursor`. With `to_file`, the artifact and `file`, the path of the whole artifact in the agent's inbox folder |
| `bus_expect` | `kind`, `sender` and `within_s` (required); `subject_prefix`; `since`; `idempotency_key` | the expectation, `state` `open`. Keyed |
| `bus_expectations` | `closed` | `rows` (the agent's open expectations, or every state with `closed`) and `total` |
| `bus_expect_withdraw` | `expectation_id` (required); `idempotency_key` | the expectation as it is now. Keyed |

### Arguments of the bus tools

| Argument | Used by | Value |
|---|---|---|
| `kind` | `bus_send`, `bus_expect` | `handoff`, `task_request`, `status`, `question`, `answer`, `decision`, `review_request`, `review_result`, `alert` or `digest`. A send with no `kind` is an `answer` when it has `reply_to`, else a `status` that carries `payload` `{"phase": "..."}` |
| `text` | `bus_send` | the message body; its first non-blank line becomes the subject |
| `to` | `bus_send` | the name of another agent as `dockingbird status` lists it, or `parent`. Left out, the message goes to the sender's parent |
| `all`, `swarm`, `role` | `bus_send` | a group in place of `to`: every agent (`all` true), a swarm by name, a role by name, or a role in a swarm. A group that expands to no agent is refused with `GROUP_EMPTY`, and the sender's own agent is left out |
| `reply_to` | `bus_send` | the message id this answers or continues. It routes nothing: with no `to`, the reply goes to the parent |
| `supersedes` | `bus_send` | the id of the sender's own earlier message, which this one withdraws |
| `requires_ack`, `reply_required` | `bus_send` | booleans. `requires_ack` marks a `status`, `decision`, `review_result`, `alert`, `answer` or `question`; `reply_required` marks a `task_request`, `handoff` or `review_request` |
| `artifacts` | `bus_send` | up to 16 artifact ids from `bus_artifact_put` |
| `payload` | `bus_send` | an object of at most 32,768 bytes as canonical JSON, nested at most 13 levels. Each kind has its own shape, which the agent's bus rules and a `KIND_PAYLOAD_INVALID` refusal show |
| `cursor` | the paged reads | the last page's `next_cursor`; leave it out for the first page |
| `delivery_id` | `bus_read`, `bus_ack`, `bus_wait` | the delivery's id from `bus_inbox` or `bus_read` |
| `expected_version` | `bus_ack` | the delivery's version as `bus_inbox`, `bus_read` or the last `bus_ack` reports it |
| `outcome` | `bus_ack` | `accepted`, `responded`, `done`, `declined` or `needs_info`. `done` is reported, never verified. An accepted delivery is settled by `done` or `needs_info`, or by the reply it requires; `declined` on it is refused with `VERSION_CONFLICT` |
| `note` | `bus_ack` | at most 120 characters |
| `evidence` | `bus_ack` | up to 16 artifact ids |
| `thread_id` | `bus_thread` | a thread id from `bus_inbox`, `bus_read` or `bus_search` |
| `query` | `bus_search` | one printable line of at most 200 characters; it matches the messages of the agent's own threads |
| `timeout_s` | `bus_wait` | 1 to 45 seconds, default 25. A timeout cancels nothing |
| `name` | `bus_artifact_put` | a slug |
| `content` | `bus_artifact_put` | text of at most 262,144 UTF-8 bytes. A larger file goes through the CLI |
| `media_type` | `bus_artifact_put` | `text/markdown` (the default), `text/plain`, `application/json` or `application/x-patch` |
| `artifact_id` | `bus_artifact_get` | an artifact id from a message or from `bus_artifact_put` |
| `to_file` | `bus_artifact_get` | true writes the whole artifact to the agent's inbox folder and answers its path; it cannot be combined with `cursor` |
| `sender` | `bus_expect` | the expected sender's agent name |
| `subject_prefix` | `bus_expect` | the start of the expected subject, at most 120 characters; left out, any subject |
| `within_s` | `bus_expect` | seconds to wait, 1 to 604,800 (7 days) |
| `since` | `bus_expect` | an RFC 3339 time with an offset, the earliest send time that matches. Left out, the time of the registration: only a row sent after it closes the expectation |
| `closed` | `bus_expectations` | true lists every state, false (the default) the open ones |
| `expectation_id` | `bus_expect_withdraw` | an id from `bus_expect` or `bus_expectations` |

An expectation is `open`, `matched`, `alerted` or `withdrawn`. A matching row that arrives matches it, and if none arrives by `due_at` the agent gets one alert. `bus_wait` polls every second until a delivery arrives or the named delivery changes state or version.

## The claim, commit and connection tools

These nine tools are in the `default` set only, apart from `bus_whoami` and `bus_session` above.

| Tool | Arguments | Returns |
|---|---|---|
| `bus_status` | `section` (`mine`, `repositories`, `sessions`, `claims`, `publications`, `conflicts` or `incidents`; default `mine`); `offset` (0 to 100) | `section`, `taken_at`, `truncated`, `total`, `offset`, `rows` and `next_offset`; `counts` for a project list. `mine` lists the agent's live claim groups, soonest expiry first |
| `bus_claim` | `paths` (relative paths, at least one, at most 64); `repository_id`; `ttl_s` (default 120, at most 3,600); `wait`; `waiter_id`; `idempotency_key` | a granted group (`group_id`, `fence`, `expires_at`, `selectors`) or a refusal (`reason` of `HELD`, `QUARANTINED` or `WAITER_AHEAD`, `holders`, `waiter_id`). With `wait`, a refused claim queues, and `waiter_id` alone polls it. Keyed |
| `bus_renew` | `group_id` (required); `ttl_s`; `idempotency_key` | the group as `bus_claim` grants it. Keyed |
| `bus_release` | `group_id` (required); `idempotency_key` | `group_id`, `result` (`RELEASED` or `WAITING_FOR_EFFECTS`), `promoted_waiters` and `protection_loss`. Keyed |
| `bus_submit` | `commit` (required, the full 40 or 64 character lowercase hex id); `repository_id`; `idempotency_key` | a status of `PUBLISHED`, `STALE`, `REFUSED` or `UNKNOWN`, all of them answers. Retry `UNKNOWN` with the same key. Keyed |
| `bus_connections` | none | `grants`: each owner-issued connection grant with its operations and resource aliases, never a credential or a host path |
| `bus_request` | `grant_id`, `connection_id`, `operation` and `resource` (required); `parameters`; `idempotency_key` | the queued job: `job_id`, the request, `state`, `created_at`. Keyed |
| `bus_request_status` | `job_id` (required) | the job's `state` (`queued`, `executing`, `succeeded`, `failed`, `refused`, `cancelled` or `unknown`), its `reason` when failed, and its result. A finished `git.fetch` names its bundle file, and a `git.push` sends the published head |
| `bus_request_cancel` | `job_id` (required); `idempotency_key` | the job. A started effect cannot be undone. Keyed |

`bus_status` answers `FORBIDDEN` for the project lists when the session holds no claim. The repository of `bus_claim` and `bus_submit` defaults to the agent's own, the one `bus_whoami` shows. Commits published under `default` or `full` reach your checkout through `dockingbird sync`, which [the sync model](../concepts/sync-model.md) describes.

## The browser tools

An agent has these 14 tools whenever its config says `browser = "chrome"`, whatever the config's `tools` key says. [The agent browser guide](../guides/agent-browser.md) covers the Chrome of the agent's own sidecar container. [The MCP servers, services and browsers guide](../guides/mcp-and-services.md) covers a browser of your Mac lent through `connect --browser`, which these tools drive as well.

Two browsers can sit behind the tools. An agent's own Chrome in a container answers at once. Your Mac's Chrome, Firefox or Safari, as granted, makes the first `browser_open` ask you and answer `waiting` until you serve it. Every call after the first takes the tab you last used unless it names one.

| Tool | Arguments | What it does and returns |
|---|---|---|
| `browser_open` | `url` (required); `tab`; `profile` | opens `url` in a new tab, or in `tab`, and waits up to 30 seconds for the page to load. Returns `browser` (`chrome`, `firefox` or `safari`), `input` (`system` when clicks and keys reach the browser as real mouse and keyboard input, `protocol` otherwise), the tab, whether the page loaded and the page as `browser_read` gives it |
| `browser_read` | `tab`; `max_chars` | the tab's `url`, `title` and visible text, cut to `max_chars` (1 to 200,000, default 20,000). On Chrome it adds `fields`, the visible form controls (at most 50, each with `tag`, `type`, `id`, `name`, `autocomplete` and `label`, never a value) and `fields_truncated` |
| `browser_click` | `tab`; `selector` or `x` and `y` | clicks the first element that matches the CSS `selector`, or the viewport point. The real pointer moves along a human path and presses, so a page sees `isTrusted: true`. The answer names the route and the path |
| `browser_type` | `selector` and `value` (required); `tab`; `submit` | focuses the first match and types `value` key by key at a person's pace, at most 8,192 bytes a call. `submit` presses Enter after |
| `browser_press` | `key` (required); `tab` | presses one key as a person would: one character, or `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `PageUp`, `PageDown`, `Home`, `End` or `Space` |
| `browser_hover` | `tab`; `selector` or `x` and `y` | moves the pointer along a human path to the element or point and presses nothing |
| `browser_scroll` | `dx` or `dy` (pixels, negative for left and up); `tab`; `selector` or `x` and `y` | scrolls in wheel steps with pauses, with the pointer first moved to the element, the point or the centre of the viewport. A call with neither `dx` nor `dy` is refused |
| `browser_drag` | `to_x` and `to_y` (required); `tab`; `selector` or `x` and `y` | presses at the start, moves along a human path and releases at the end |
| `browser_screenshot` | `tab` | writes a PNG as the next `screenshot-N.png` in the agent's log folder and answers its path and size. The agent reads the file to see it |
| `browser_login` | `login` and `url` (required); `password_field`; `username_field`; `code_field`; `submit_selector`; `step` (`fill` or `totp`, default `fill`); `tab`; `connection` | signs in with a vault login in a tab of its own. Returns the `tab` the sign-in reached, the `login` alias and the outcome, or `state` `waiting` while the sign-in goes on, and the agent calls again for the answer. Chrome only. The agent never sees the password or a code |
| `browser_cdp` | `method` (required); `params`; `tab` | sends any Chrome DevTools Protocol method to the tab's session and answers its result. Chrome only; the browser's own target cannot be reached |
| `browser_bidi` | `method` (required); `params` | sends a WebDriver BiDi command and answers its result; Firefox of your Mac only |
| `browser_webdriver` | `method` (required); `params`; `tab` | sends a WebDriver command, `method` being the HTTP method, a space and the path below the session, such as `POST /url`; Safari of your Mac only |
| `browser_release` | none | lets the browser go. Returns `released`, true when a browser was held. The next `browser_open` asks anew for your Mac's browser, and answers at once for the agent's own Chrome |

### Arguments of the browser tools

| Argument | Value |
|---|---|
| `url` | an address of at most 2,048 bytes |
| `tab` | a tab named in an earlier answer; the default is the tab last used. A Chrome tab id is 32 hex digits |
| `selector` | a CSS selector of at most 1,024 bytes; the first match counts |
| `x`, `y`, `to_x`, `to_y` | viewport points in CSS pixels, from 0 up to 1,000,000; `x` needs `y`, and a call never names both a selector and a point |
| `dx`, `dy` | scroll amounts in CSS pixels, from -1,000,000 to 1,000,000 |
| `value` | the text to type, at most 8,192 bytes |
| `profile` | `own` (default) or `temporary`, and read only for your Mac's browser: `own` is your profile, `temporary` a fresh one. The agent's own sidecar Chrome always has a fresh profile |
| `method`, `params` | a protocol method name of at most 128 bytes, and its parameters as an object of at most 32,768 bytes of canonical JSON |
| `login` | the login's alias, a slug from `connect --vault` |
| `password_field`, `username_field`, `code_field`, `submit_selector` | CSS selectors of at most 1,024 bytes. Every one is optional, and Dockingbird finds the fields a call leaves out. `submit_selector` may also be `enter` |
| `step` | `fill` types the password, with the username and a first-page code when their fields are named. `totp` types the current one-time code alone, and is refused for a login with a code origin |
| `connection` | the vault connection's id, needed only when several are granted |

A login with a second factor takes one `fill` call with `login` and `url` alone, which types the code page too. The agent never clicks through it. After the code, it answers yes to a device question. While a sign-in runs, the agent's other browser commands are refused until it ends. [The secrets vault guide](../guides/secrets-vault.md) sets up the store and the connection.

## The fleet tools

An agent on a joined home gets ten more tools that start with `fleet_`, in the `full` set and beside the `bus` tools. [The fleet tools page](fleet-tools.md) lists them.
