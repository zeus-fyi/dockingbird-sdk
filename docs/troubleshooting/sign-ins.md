---
title: "Troubleshooting index: sign-ins and the org store"
summary: "The 91 message ids about signing in, API keys, signing out and the org login, each with when it appears."
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Troubleshooting index: sign-ins and the org store

Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the exit status. This page holds the 91 ids about signing in, API keys, signing out and the org login.

## Agents: starting

| Id | When it appears |
|---|---|
| [`SIGNIN_FIRST_TIME`](../troubleshooting.md#signin_first_time) | An agent starts and the tool isn't signed in yet (and no API key is saved for it). The line says what its sign-in screen will ask; you do it only once. |

## Sign-ins

| Id | When it appears |
|---|---|
| [`SIGNIN_NEEDED`](../troubleshooting.md#signin_needed) | The tool isn't signed in. Either there was no terminal to sign in on, or its sign-in screen showed and didn't finish (you quit, or never used the link). The message gives both routes: a sign-in or an API key. |
| [`SIGNIN_START`](../troubleshooting.md#signin_start) | You ran `dockingbird login claude` or `login codex`: the tool's own sign-in screen follows, and the line says what it will ask. |
| [`SIGNIN_DONE`](../troubleshooting.md#signin_done) | The sign-in finished, and Dockingbird keeps it. |
| [`SIGNIN_DONE_KEY_REMOVED`](../troubleshooting.md#signin_done_key_removed) | The sign-in finished. You had an API key saved for the tool, and the last login wins, so the key was removed. |
| [`DEVICE_AUTH_DISABLED`](../troubleshooting.md#device_auth_disabled) | Codex's sign-in didn't finish. Codex signs in with a device code, which ChatGPT's security settings can turn off; the message says where, and gives the API key route. |
| [`SIGNED_OUT`](../troubleshooting.md#signed_out) | You ran `dockingbird logout`: the tool's sign-in and any saved key are gone. When Dockingbird followed this computer's own login of the tool, it stops following it; the login on this computer is unchanged, and `dockingbird login claude --here` (or `codex`) uses it again. |
| [`LOGOUT_NOT_SIGNED_IN`](../troubleshooting.md#logout_not_signed_in) | You ran `dockingbird logout` for a tool that had no sign-in and no saved key. |
| [`LOGOUT_AGENTS_RUNNING`](../troubleshooting.md#logout_agents_running) | You ran `dockingbird logout` while an agent of that tool is running. Signing out would pull its sign-in away, so it waits for you to stop the agent. |
| [`LOGOUT_FAILED`](../troubleshooting.md#logout_failed) | Signing out didn't finish, or the saved API key couldn't be removed. Running the command again usually works. |
| [`LOGIN_AGENTS_RUNNING`](../troubleshooting.md#login_agents_running) | You ran `dockingbird login` for a tool while one of its agents is running: a Claude agent keeps Claude's sign-in fresh, and a Codex agent could put its own sign-in back, so stop it first. |
| [`LOGIN_NEEDS_TERMINAL`](../troubleshooting.md#login_needs_terminal) | You ran `dockingbird login` without a terminal, as in a script. The tool's sign-in needs one; an API key doesn't. |
| [`SIGNIN_FAILED`](../troubleshooting.md#signin_failed) | The tool's sign-in failed or didn't finish. Nothing changed; the message gives the API key route too. |
| [`SIGNIN_NOT_SAVED`](../troubleshooting.md#signin_not_saved) | The sign-in finished, but Dockingbird couldn't keep it. Running `login` again usually works. |
| [`KEY_NOT_REMOVED`](../troubleshooting.md#key_not_removed) | The sign-in finished, but your saved API key couldn't be removed, so the key is still what the tool uses. |
| [`API_KEY_NOT_SAVED`](../troubleshooting.md#api_key_not_saved) | You ran `dockingbird login ... --api-key`, and Dockingbird couldn't save the key. Nothing changed. When removing what an earlier save left took longer than Dockingbird waits, usually because the computer was busy, the message says so; the next run removes it first again. |
| [`API_KEY_TIMED_OUT`](../troubleshooting.md#api_key_timed_out) | You ran `dockingbird login ... --api-key`, and saving the key took longer than Dockingbird waits, usually because the computer was busy, so it may or may not be saved. When Docker couldn't remove the step's container, the message names it. |
| [`API_KEY_PROMPT`](../troubleshooting.md#api_key_prompt) | `dockingbird login ... --api-key` asks for the key. What you paste isn't shown. |
| [`API_KEY_SAVED`](../troubleshooting.md#api_key_saved) | Dockingbird saved your API key. The tool uses it from now on, in place of any sign-in. |
| [`API_KEY_INVALID`](../troubleshooting.md#api_key_invalid) | The API key you pasted was empty or had spaces or control characters, or you pressed Ctrl-C at the question. Nothing was saved. |
| [`BASE_URL_INVALID`](../troubleshooting.md#base_url_invalid) | You gave `--base-url` something that isn't an `https://` address. Nothing changed. |
| [`BASE_URL_UNSUPPORTED`](../troubleshooting.md#base_url_unsupported) | You gave `--base-url` for a tool that can't use one. Both tools can today, so you shouldn't see this. |
| [`LOGIN_TOKEN_ON_STDIN`](../troubleshooting.md#login_token_on_stdin) | You ran `dockingbird login claude --oauth-token -` or `dockingbird login codex --auth-json -` without piping the value in: it is read from standard input only, never from a terminal, a file or your Mac's own sign-ins. |
| [`LOGIN_IMPORT_INVALID`](../troubleshooting.md#login_import_invalid) | The token or file you piped in was refused, before anything ran or by the sign-in store's own parser: a token must be one line of printable ASCII within the key's size bound, and a Codex auth.json a Codex sign-in within the sign-in store's size bound. Nothing changed. |
| [`LOGIN_IMPORT_FAILED`](../troubleshooting.md#login_import_failed) | Dockingbird could not keep the piped token or file for another reason than its content (the store was busy, unreadable or could not be written, or Docker gave no answer); nothing changed. |
| [`LOGIN_IMPORTED`](../troubleshooting.md#login_imported) | The piped token or file is in Dockingbird's store, and the tool uses it from now on. The last login wins, so a saved API key goes with it; the line says so only when there was one. |
| [`LOGIN_IMPORT_FORM`](../troubleshooting.md#login_import_form) | You gave `login` an import form of the other tool, or two forms at once (`--here` is one of them). |
| [`LOGIN_HERE_DONE`](../troubleshooting.md#login_here_done) | You ran `dockingbird login claude --here` (or `codex`): Dockingbird keeps a copy of the login this computer's Claude Code or Codex uses, without its refresh token, and follows it from then on. Run it again any time; when nothing changed it says so. |
| [`LOGIN_HERE_ADOPTED`](../troubleshooting.md#login_here_adopted) | The first start of a tool Dockingbird had no sign-in or key for found the tool's login on this computer and uses it from now on, as `dockingbird login claude --here` would. `dockingbird logout` stops that. |
| [`LOGIN_HERE_NOT_FOUND`](../troubleshooting.md#login_here_not_found) | You ran `dockingbird login claude --here` (or `codex`), and this computer has no login of that tool: sign in with Claude Code or Codex here first, or sign in for Dockingbird only with `dockingbird login claude`. When `~/.claude/settings.json` was skipped on the way (a link, or a file others may write, say), the message names it and the rule, since that file may hold your only Claude login: make it a plain file of yours (not a link) that only you can write, readable and under 64 KiB, then run it again. Nothing changed. |
| [`LOGIN_HERE_EXPIRED`](../troubleshooting.md#login_here_expired) | You ran `dockingbird login claude --here`, and the login on this computer has expired. Claude Code renews it when you use it here; Dockingbird never does. Nothing changed. |
| [`LOGIN_HERE_UNAVAILABLE`](../troubleshooting.md#login_here_unavailable) | You ran `dockingbird login claude --here` (or `codex`), and the login on this computer couldn't be read: the Keychain refused or didn't answer in time (macOS may be asking you to allow it), the login file is a link or readable by others, the login has nothing Dockingbird can use, or the shell's `HOME` isn't your home folder (Dockingbird reads your login only from a shell whose `HOME` is your own). Nothing changed. |
| [`LOGIN_HERE_BLOCKED`](../troubleshooting.md#login_here_blocked) | You ran `dockingbird login claude --here` while an agent still keeps Dockingbird's own Claude sign-in fresh. Stop the agent, or sign that sign-in out with `dockingbird logout claude`, then run it again. Nothing changed. |
| [`LOGIN_HERE_GATEWAY_NOT_HTTPS`](../troubleshooting.md#login_here_gateway_not_https) | You ran `dockingbird login claude --here`, and Claude Code on this computer signs in with the token set in `~/.claude/settings.json` (its `env` block) through a gateway set there whose address isn't `https://`. Dockingbird sends a token only to an `https://` gateway: point Claude Code at the gateway's `https://` address, then run it again. A first start adopts nothing from such a login, and `status` says so after a change the watcher saw. Nothing changed. The one plain address Dockingbird follows is this computer's own (`http://127.0.0.1:59471`, say, a proxy on this Mac), which agents reach as `host.docker.internal`. |
| [`LOGIN_HERE_GATEWAY_UNREACHABLE`](../troubleshooting.md#login_here_gateway_unreachable) | You ran `dockingbird login claude --here` on a computer that isn't a Mac, and Claude Code here signs in with the token set in `~/.claude/settings.json` (its `env` block) through a gateway on this computer itself (`127.0.0.1`, `localhost` or `[::1]`), which agents reach only through Docker Desktop on a Mac, as `host.docker.internal`. Point Claude Code at an `https://` address agents can reach, then run it again. A first start adopts nothing from such a login, and `status` says so after a change the watcher saw. Nothing changed. |
| [`LOGIN_HERE_SETTINGS_SKIPPED`](../troubleshooting.md#login_here_settings_skipped) | You ran `dockingbird login claude --here`, or an agent's first start took this computer's Claude login, and `~/.claude/settings.json` isn't a file Dockingbird reads (a link, as dotfiles setups make; another user's; one the group or others may write; a very large one; or one that can't be read): Dockingbird skipped it, took no token and no gateway from it, and read the login from the Keychain or Claude's login file instead. `status` says so while that lasts. Make it a plain file of yours (not a link) that only you can write, readable and under 64 KiB, for a token or a gateway set there to count. |

## Status

| Id | When it appears |
|---|---|
| [`LOGIN_HERE_GATEWAY_UNFOLLOWED`](../troubleshooting.md#login_here_gateway_unfollowed) | `~/.claude/settings.json` sets a gateway in its `env` block with no token beside it, so Claude's login here is the Keychain's or its login file's, and that gateway isn't one Dockingbird follows with such a login: only a gateway on this Mac itself (`127.0.0.1`, `localhost` or `[::1]`) is, reached by the agents as `host.docker.internal`; a gateway elsewhere, or one on a Linux computer, is left to Claude Code here, and the agents call Anthropic directly. `dockingbird login claude --here`, a first start and `status` say it. To send the agents through that gateway too, give Claude Code here a token in the same `env` block (`claude setup-token`), which Dockingbird follows with its gateway. |

## dockingbird fleet update

| Id | When it appears |
|---|---|
| [`ORG_PROJECT_UNKNOWN`](../troubleshooting.md#org_project_unknown) | `dockingbird fleet` couldn't tell which project a swarm definition is for: no `.dockingbird/project.toml` in the checkout, no `project` in the definition, no `--project`, and none in the org pointer. |

## The org login

| Id | When it appears |
|---|---|
| [`ORG_SECRET_IN_ARGV`](../troubleshooting.md#org_secret_in_argv) | You typed `--password` after `dockingbird org`, where your shell history and other programs can read the password. Nothing ran; run `dockingbird org login` and type the password when asked, or pipe it in with `--password-stdin`. |
| [`ORG_LOGIN_NO_TERMINAL`](../troubleshooting.md#org_login_no_terminal) | You ran `dockingbird org login` from a script or a pipe, where there is no terminal to ask for the password on. Pipe the password in with `--password-stdin`. |
| [`ORG_SECRET_TOO_LONG`](../troubleshooting.md#org_secret_too_long) | The password you typed or piped into `dockingbird org login` is longer than any database password, which usually means a file was piped in by mistake. Nothing was saved. |
| [`ORG_SECRET_INVALID`](../troubleshooting.md#org_secret_invalid) | The password you typed or piped into `dockingbird org login` is empty, isn't UTF-8 text, or has a control character such as a line break inside it, which the password file can't keep. Nothing was saved. |
| [`ORG_PGPASS_UNSAFE`](../troubleshooting.md#org_pgpass_unsafe) | Your password file, `~/.pgpass` or the file `PGPASSFILE` names, is a link, isn't a regular file, belongs to another user, can be read by others, or is too large; or its folder isn't yours alone. Dockingbird writes and reads nothing there until it is a file only you can read and write (`chmod 600`). |
| [`ORG_CONFIG_INVALID`](../troubleshooting.md#org_config_invalid) | The org pointer, `~/.config/dockingbird/org.toml`, which `dockingbird org login` writes, has a key that is missing, unknown or wrong, isn't TOML, or isn't a file only you can read. The message names the key. Remove the file and log in again. |
| [`ORG_STORE_CHANGED`](../troubleshooting.md#org_store_changed) | You ran `dockingbird org login` for another org store than the one this computer already logs in to. Nothing changed; run it again with `--replace` to move to the new store, then log in each other kind again. |
| [`ORG_NOT_CONFIGURED`](../troubleshooting.md#org_not_configured) | This computer has no org login yet, so `dockingbird org status` and the fleet commands don't know which database to reach or as whom. Run `dockingbird org login` first. |
| [`ORG_ROLE_MISSING`](../troubleshooting.md#org_role_missing) | This computer is logged in to the org store, but not as the kind the command needs: `user` for your own commands, `worker` for `dockingbird fleet worker`, `admitter` for `dockingbird fleet admitter`. The message gives the login to run. |
| [`ORG_SECRET_MISSING`](../troubleshooting.md#org_secret_missing) | The org pointer names the role the command connects as, but your password file has no password for it at that database. Log in again; the message gives the command. |
| [`ORG_AS_REQUIRED`](../troubleshooting.md#org_as_required) | You ran `dockingbird org login` without `--as user`, `--as worker` or `--as admitter`. A role's name doesn't say which kind of login it is, so you name it. |
| [`ORG_OPTION_INVALID`](../troubleshooting.md#org_option_invalid) | You gave `dockingbird org login` a host, port, kind, role, database or project it can't record, or no `--role`. The message names the option. |
| [`ORG_PASSWORD_PROMPT`](../troubleshooting.md#org_password_prompt) | You ran `dockingbird org login` in a terminal: type the role's password; it isn't shown as you type it. |
| [`ORG_LOGIN_SAVED`](../troubleshooting.md#org_login_saved) | `dockingbird org login` saved the password in your password file and the store and role in the org pointer. `dockingbird org status` checks the connection. |
| [`ORG_FLEET_TOML_PASSWORD`](../troubleshooting.md#org_fleet_toml_password) | `dockingbird org login --from-fleet-toml` moved a home's `fleet.toml` login to the password file and the org pointer, and asks whether to take the password out of `fleet.toml`, or says it did or that it is still there. |
| [`ORG_STATUS`](../troubleshooting.md#org_status) | You ran `dockingbird org status`: the org store this computer logs in to, each kind's role and whether its password is saved (never the password itself), and whether the store answered your login. |
| [`ORG_LOGOUT_DONE`](../troubleshooting.md#org_logout_done) | You ran `dockingbird org logout`: the role's password line and its role in the org pointer are gone, or every kind's with no `--as`. |
| [`ORG_OPTION_NEEDED`](../troubleshooting.md#org_option_needed) | You ran a `dockingbird org` verb without an option it needs: `roles set` needs `--harness` and `--model`, `roles unset` `--harness`, `people add` `--account`, and `members add` and `remove` `--project`. Nothing ran. |
| [`ORG_OPTION_NOT_HERE`](../troubleshooting.md#org_option_not_here) | You gave a `dockingbird org` verb an option it doesn't take, such as `--name` to `projects remove`. Nothing ran; `dockingbird org -h` shows each verb's options. |
| [`ORG_ROLE_WORD_INVALID`](../troubleshooting.md#org_role_word_invalid) | You ran `dockingbird org roles set` with a ROLE that is no slug, or a model or an effort the harness doesn't take, or one that looks like a secret, which is never shown. Nothing was saved. |
| [`ORG_NOT_ADMIN`](../troubleshooting.md#org_not_admin) | You ran a `dockingbird org` verb that changes the store, and your org login is not an admin of it. Nothing changed: log in as an admin's role, or ask an admin to run it. |
| [`ORG_NOT_CREATED`](../troubleshooting.md#org_not_created) | You ran `dockingbird org projects`, `roles`, `people` or `members` on a store that isn't made yet. An admin makes it with `dockingbird org create`. |
| [`ORG_SLUG_INVALID`](../troubleshooting.md#org_slug_invalid) | You gave `dockingbird org` a project that can't be a slug: lowercase letters, digits and `-`, not starting with `-`, and short enough for the store to name the project's group role after it. Nothing ran. |
| [`ORG_PROJECT_EXISTS`](../troubleshooting.md#org_project_exists) | You ran `dockingbird org projects add` for a project the store has already. Nothing changed; `projects set` changes it. |
| [`ORG_PROJECT_NOT_FOUND`](../troubleshooting.md#org_project_not_found) | You named a project the org store doesn't have, in an org verb or as the admin queueing a swarm or a run with `dockingbird fleet`. Nothing changed; `dockingbird org projects` lists those it has, and `dockingbird init` registers a checkout's. |
| [`ORG_PROJECT_IN_USE`](../troubleshooting.md#org_project_in_use) | You ran `dockingbird org projects remove` for a project that fleet runs or members still name, so it stays. |
| [`ORG_ROLE_NOT_SET`](../troubleshooting.md#org_role_not_set) | You ran `dockingbird org roles unset` for a role and harness the store has no model for. Nothing changed. |
| [`ORG_ROLE_UNKNOWN`](../troubleshooting.md#org_role_unknown) | You ran `dockingbird org people add` for a login role the store doesn't have. An admin makes the role first, as the operator guide says. |
| [`ORG_PERSON_UNKNOWN`](../troubleshooting.md#org_person_unknown) | You ran `dockingbird org members add` for a role that isn't a person in the store yet. Add the person first with `dockingbird org people add`. |
| [`ORG_PERSON_EXISTS`](../troubleshooting.md#org_person_exists) | You ran `dockingbird org people add` for a person the store has already. Nothing changed. |
| [`ORG_PERSON_NOT_FOUND`](../troubleshooting.md#org_person_not_found) | You ran `dockingbird org people remove` for a role that isn't a person in the store. Nothing changed; `dockingbird org people` lists the persons. |
| [`ORG_PERSON_IN_USE`](../troubleshooting.md#org_person_in_use) | You ran `dockingbird org people remove` for a person who is still a member of a project, so the person stays. Remove the memberships first. |
| [`ORG_MEMBER_EXISTS`](../troubleshooting.md#org_member_exists) | You ran `dockingbird org members add` for a membership the store has already. Nothing changed. |
| [`ORG_MEMBER_UNKNOWN`](../troubleshooting.md#org_member_unknown) | You ran `dockingbird org members remove` for a membership the store doesn't have. Nothing changed. |
| [`ORG_CREATED`](../troubleshooting.md#org_created) | You ran `dockingbird org create`: the store is made, or brought up to this release, and the line names its version. |
| [`ORG_CURRENT`](../troubleshooting.md#org_current) | You ran `dockingbird org create` on a store that is already at this release's version. Nothing changed. |
| [`ORG_PROJECT_ROWS`](../troubleshooting.md#org_project_rows) | You ran `dockingbird org projects`: one line per project, with its name, repository, branch and the release `dockingbird init` last saw. |
| [`ORG_PROJECT_NONE`](../troubleshooting.md#org_project_none) | You ran `dockingbird org projects` on a store with no project yet. `dockingbird init` adds a repo's own; `dockingbird org projects add` adds any. |
| [`ORG_PROJECT_ADDED`](../troubleshooting.md#org_project_added) | You ran `dockingbird org projects add`: the project is in the store. |
| [`ORG_PROJECT_SET`](../troubleshooting.md#org_project_set) | You ran `dockingbird org projects set`: the values you gave are saved. |
| [`ORG_PROJECT_REMOVED`](../troubleshooting.md#org_project_removed) | You ran `dockingbird org projects remove`: the project is gone from the store. |
| [`ORG_ROLE_ROWS`](../troubleshooting.md#org_role_rows) | You ran `dockingbird org roles`: one line per agent role and harness, with the model and effort your organisation chose. |
| [`ORG_ROLE_NONE`](../troubleshooting.md#org_role_none) | You ran `dockingbird org roles` on a store with no role's model yet; a swarm's roles then name their own. |
| [`ORG_ROLE_SET`](../troubleshooting.md#org_role_set) | You ran `dockingbird org roles set`: the role's model, and effort if you gave one, are saved for that harness. |
| [`ORG_ROLE_UNSET`](../troubleshooting.md#org_role_unset) | You ran `dockingbird org roles unset`: the role has no model for that harness in the store now. |
| [`ORG_PERSON_ROWS`](../troubleshooting.md#org_person_rows) | You ran `dockingbird org people`: one line per person, with the account their licence is under. |
| [`ORG_PERSON_NONE`](../troubleshooting.md#org_person_none) | You ran `dockingbird org people` on a store with no person yet. |
| [`ORG_PERSON_ADDED`](../troubleshooting.md#org_person_added) | You ran `dockingbird org people add`: the person is in the store. |
| [`ORG_PERSON_REMOVED`](../troubleshooting.md#org_person_removed) | You ran `dockingbird org people remove`: the person is gone from the store; their login role stays. |
| [`ORG_MEMBER_ROWS`](../troubleshooting.md#org_member_rows) | You ran `dockingbird org members`: one line per person and project they are a member of. |
| [`ORG_MEMBER_NONE`](../troubleshooting.md#org_member_none) | You ran `dockingbird org members` and no one is a member of a project yet, or of the one you named. |
| [`ORG_MEMBER_ADDED`](../troubleshooting.md#org_member_added) | You ran `dockingbird org members add`: the person may now run the project's fleet work. |
| [`ORG_MEMBER_REMOVED`](../troubleshooting.md#org_member_removed) | You ran `dockingbird org members remove`: the person may no longer run the project's fleet work. |
