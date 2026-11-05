---
title: License refused
summary: Each way a license command or a license check can stop you, in the order you meet it, with what the screen shows and the fix.
audience: first-day
commands:
  - license activate
  - license activations --release
  - license status --refresh
  - license trial
  - update
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# License refused

This page tells each license failure as a story. The stories are a key that is not taken, seats that are full, a computer that was freed, a trial already used and a term that is over. Each part gives the message id, what the screen shows and the fix. The commands behind it are on the [licensing guide](../guides/licensing.md). A start refused for a license, `LICENSE_REFUSED`, is not yet available.

## Before you start

- Dockingbird is installed. Check with `dockingbird --version`.
- You know which license key this computer should use. It is in the purchase email.
- `dockingbird license status` runs. It reads the license file on this computer and works offline.

## 1. The key is not taken

You run `dockingbird license activate` and paste the key. Two messages stop it before the server counts a seat.

[LICENSE_KEY_IN_ARGV](../troubleshooting.md#license_key_in_argv) exits 2 when the key follows the command on the line. Nothing ran. Run `dockingbird license activate` with no argument and paste the key when it asks.

[LICENSE_KEY_INVALID](../troubleshooting.md#license_key_invalid) exits 1 when the server does not know the key or the text is not a key. The key is never shown, so check what you pasted.

```text
{publisher} doesn't know that license key; nothing changed.
Check it, then: dockingbird license activate
```

Copy the key again from the purchase email and run the command again.

## 2. Seats are full

The license admits its seats times three computers, and every one is linked. The third computer of a one-seat license succeeds. A fourth one gets [LICENSE_SEATS_FULL](../troubleshooting.md#license_seats_full) and exit 1.

```text
Every computer this license admits is linked, so this one can't join.
Free one: dockingbird license activations --release ID
```

Under those lines the command names each linked computer, the one seen longest ago first, with its id. Pick the computer you no longer use and free it.

```bash
dockingbird license activations --release ID
```

The fix worked when the product prints [LICENSE_ACTIVATION_RELEASED](../troubleshooting.md#license_activation_released) and lists the rest.

```text
The seat of activation {id} is free again.
```

Run `dockingbird license activate` again on this computer. It prints `This computer is activated:` and the count of linked computers. The [seat cookbook](../../examples/move-your-seat/README.md) walks the same fix with a new laptop.

## 3. A computer that was freed

Say you freed the seat of your old laptop from your new one. The old laptop still has its license file until it checks in. When it runs `dockingbird license status --refresh`, the screen shows the state under [LICENSE_SHOWN](../troubleshooting.md#license_shown) and exits 0.

```text
This computer's seat was freed from another computer.
Activate it again: dockingbird license activate
```

Run `dockingbird license activate` on that laptop only if you want it back on the license. If the other computers hold every link by then, that command meets step 2 and `LICENSE_SEATS_FULL`.

Two other status lines have the same fix. `The license file here is another computer's.` appears when the file came from a different computer, and its next step is `Activate this one: dockingbird license activate`. `The license file here can't be read.` appears when the file is damaged, and its next step is `Activate it again: dockingbird license activate`.

## 4. A trial already used

A trial starts with `dockingbird license trial`. It is allowed once per computer.

```text
This computer has had its trial already.
Activate it with a key: dockingbird license activate
```

That is [LICENSE_TRIAL_USED](../troubleshooting.md#license_trial_used), exit 1. Activate with a key. A trial cannot install from the release index and cannot update. An index install on a trial computer meets [LICENSE_UPDATE_NEEDS_LICENSE](../troubleshooting.md#license_update_needs_license) at `dockingbird update`. It exits 1 and changes nothing.

```text
Updating Dockingbird needs this computer's license: its release index
lets in only an activated computer. Nothing changed.
Activate it: dockingbird license activate
```

## 5. The term is over

The term is the period the license names. Before it ends, an agent start prints one line from [LICENSE_NOTE](../troubleshooting.md#license_note) and the agent starts.

```text
Your Dockingbird license ends {until}; renew it to keep starting new agents.
```

After it ends, `dockingbird license status` prints this.

```text
The license's term ended.
Renew it, then: dockingbird license status --refresh
```

The installed version keeps working. New releases need a renewed license. Renew, then run `dockingbird license status --refresh` to read the new term. The grace period after a term ends is the length the license names.

## 6. The server or the license program is out of reach

[LICENSE_AUTHORITY_UNAVAILABLE](../troubleshooting.md#license_authority_unavailable) exits 1 when the license server cannot be reached. Nothing changed. Get online and run the command again. An offline `status` without `--refresh` still works.

```text
Dockingbird couldn't reach the license server, so nothing changed.
Try again later.
```

The license program is a small file Dockingbird downloads on the first `dockingbird license` command. Three ids mean it is missing or damaged, and each prints its fix.

- [LICENSE_CLIENT_UNAVAILABLE](../troubleshooting.md#license_client_unavailable): the download failed. Run `dockingbird license status`, which downloads it again.
- [LICENSE_CLIENT_DAMAGED](../troubleshooting.md#license_client_damaged): the program did not answer as expected. Run `dockingbird update`.
- [LICENSE_CLIENT_DIGEST_MISMATCH](../troubleshooting.md#license_client_digest_mismatch): the download is not the one this version expects, so it was not kept. Run `dockingbird update`.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [LICENSE_KEY_IN_ARGV](../troubleshooting.md#license_key_in_argv) | Paste the key when asked. |
| [LICENSE_KEY_INVALID](../troubleshooting.md#license_key_invalid) | Copy the key again. |
| [LICENSE_SEATS_FULL](../troubleshooting.md#license_seats_full) | Free a computer. |
| [LICENSE_ACTIVATION_RELEASED](../troubleshooting.md#license_activation_released) | Informs only, exit 0. |
| [LICENSE_SHOWN](../troubleshooting.md#license_shown) | The state of the license, exit 0. |
| [LICENSE_TRIAL_USED](../troubleshooting.md#license_trial_used) | Activate with a key. |
| [LICENSE_UPDATE_NEEDS_LICENSE](../troubleshooting.md#license_update_needs_license) | Activate, then update. |
| [LICENSE_NOTE](../troubleshooting.md#license_note) | The agent starts; read `dockingbird license status`. |
| [LICENSE_AUTHORITY_UNAVAILABLE](../troubleshooting.md#license_authority_unavailable) | Get online. |
| [LICENSE_CLIENT_UNAVAILABLE](../troubleshooting.md#license_client_unavailable) | Run `dockingbird license status`. |
| [LICENSE_CLIENT_DAMAGED](../troubleshooting.md#license_client_damaged) | Run `dockingbird update`. |
| [LICENSE_CLIENT_DIGEST_MISMATCH](../troubleshooting.md#license_client_digest_mismatch) | Run `dockingbird update`. |

The page before this one is [install fails](install-fails.md). The one after is [the first start stops](first-start-stops.md).
