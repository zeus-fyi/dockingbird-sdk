---
title: Sign agents in with a password vault
summary: Connect a gopass store so Dockingbird types a login's password and one-time code into an agent's browser, and the agent sees neither.
audience: daily
commands:
  - connect --vault
  - connect --browser
  - serve
  - connections
  - disconnect
---

# Sign agents in with a password vault

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

An agent that browses may need to sign in to a site. With a vault connection, the agent names a login, and Dockingbird types the stored password and the current one-time code into the page itself. This page makes the gopass store, connects it, and lends it a browser. The model behind it is on [connections.md](connections.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- You use a Mac with Google Chrome. Sign-ins work in Chrome only in this release, and Firefox and Safari requests are refused in words.
- The browser connection exists, or you make it in step 4. [mcp-and-services.md](mcp-and-services.md) covers lending Chrome.
- A passphrase for the store is ready. Dockingbird asks for it on your terminal, hidden, and keeps it inside Dockingbird the way it keeps a database password.

## Steps

1. Install gopass 1.17.4, the version Dockingbird's image carries. The release is `gopass-1.17.4-darwin-arm64.tar.gz` at `https://github.com/gopasspw/gopass/releases/tag/v1.17.4`. Check its checksum before you open the archive, then put the `gopass` program it holds on your `PATH`.

   ```bash
   shasum -a 256 gopass-1.17.4-darwin-arm64.tar.gz
   ```

   The step is done when the command prints this checksum.

   ```text
   b052f36631e619fa9391edeee581d1f3937c4c41d432aa4ba673b53401800c0f  gopass-1.17.4-darwin-arm64.tar.gz
   ```

2. Make the store once, in the `vaults/logins` folder of your Dockingbird home. That is `~/.local/share/dockingbird/vaults/logins` unless you set `DOCKINGBIRD_HOME`, and then it is the `vaults/logins` folder there. The command makes the store with an age identity under your passphrase. A bare `gopass init` fails, because it needs an identity first.

   ```bash
   export GOPASS_HOMEDIR=~/.local/share/dockingbird/vaults/logins
   export GOPASS_AGE_PASSWORD="<the passphrase>"
   gopass setup --crypto age --storage fs
   ```

   Keep the whole folder that `setup` made, including its `.config` and `.cache`, because the reads need them. The step is done when the folder exists and holds those two.

3. Insert each login, with the same two environment variables set. Type the password on the first line. For a site with two-factor sign-in, paste the `otpauth://totp/...` line from the enrolment page below it. An entry that holds a counter-based `otpauth://hotp/...` line is refused when it is used.

   ```bash
   gopass insert alice
   ```

   The step is done when `gopass ls` lists `alice`.

4. Connect the store. Each `--login` takes three words. The first is a slug such as `alice`, which is both the agent's word for the login and the store entry's name. The second is the site's origin, `https://host` or `https://host:port`. The third is the username. `--totp NAME` marks a login whose entry holds a code. `--store NAME` picks another folder under `vaults`.

   ```bash
   dockingbird connect logins --vault gopass --login alice https://site.example alice@site.example --totp alice
   dockingbird connect chrome --browser chrome
   ```

   Dockingbird checks each word and that the store is a real folder of yours there. It then asks for the passphrase and prints these lines.

   ```text
   Passphrase for the gopass store logins (hidden):
   Connected logins: a gopass vault with 1 login.
   Configs that name logins may sign in to those sites.
   Add it to a config: connections = ["logins"].
   ```

5. Name both connections in a config you add, then serve the browser. Until `serve` runs, an agent's sign-in request waits.

   ```toml
   command = "surf"
   workspace = "scratch"
   connections = ["logins", "chrome"]
   ```

   ```bash
   dockingbird config add surf.toml
   dockingbird serve chrome
   ```

   Each sign-in prints a line in the `serve` terminal. It names the agent, the site and the login, never the username, the password or the code. The step is done when one appears.

   ```text
   surf-1 signed in to https://site.example as alice for chrome: <how the typing went>
   ```

6. List what the vault holds. The listing names the logins and shows no site, username, password or code.

   ```bash
   dockingbird connections logins
   ```

   The step is done when the output holds this line.

   ```text
   logins: gopass vault, 1 login: alice
   ```

## What an agent can and cannot do

The agent asks for one sign-in at a time, by the login's name and the address of the sign-in page on that site. It names the password field, and a username or code field, by CSS selector. It is told success or a refusal in words. A refusal says the page is not on the login's site, the field is not a password field, the vault is unreadable, or the site did not accept the sign-in. It is never told the password, the code, or how long either is. The tab stays signed in until the browser session ends with the agent.

The agent cannot read, list, add or change a login or the store. It cannot sign in on your own Chrome profile. Sign-ins run only in a temporary profile, so Chrome's save-password offer and your Google account never see the password. While a sign-in is typed, its other browser commands are refused in words until it ends.

## Remove it

`dockingbird disconnect logins` removes the connection and the passphrase Dockingbird kept. The store stays yours to delete. `dockingbird clean --all` keeps your `vaults` folder whenever anything is in it, and prints this.

```text
Kept the stores of your vault connections: <path>
Delete that folder yourself if you no longer want them.
```

## When it fails

- [`CONNECT_VAULT_INVALID`](../troubleshooting.md#connect_vault_invalid) names the word refused before the passphrase was asked. Nothing was saved. The causes are a manager other than `gopass`, a store folder that is missing or a link, and a login name outside lowercase letters, digits and hyphens. An origin with a path after it, an empty username, a `--totp` that matches no login and a repeated name are refused too.
- [`CONNECT_VAULT_PASSPHRASE_SHORT`](../troubleshooting.md#connect_vault_passphrase_short) means the passphrase was empty or not text Dockingbird can keep. Type it at the question, or pipe it in.
- [`SERVE_BROWSER_LOGIN_REFUSED`](../troubleshooting.md#serve_browser_login_refused) reports a sign-in that was refused or not accepted, with the reason the agent was told.
- [`SERVE_VAULT_FOLDER_FAILED`](../troubleshooting.md#serve_vault_folder_failed) says Dockingbird could not make its `vaults` folder, or found a link or another user's folder there. Check the path and its disk.
- [`SERVE_BROWSER_MAC_ONLY`](../troubleshooting.md#serve_browser_mac_only) means the computer is not a Mac, so no browser can be lent.
