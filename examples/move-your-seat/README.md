---
title: Move your seat to a new laptop
summary: Free the old computer's link, activate the new one, and read what status shows on each.
audience: first-day
commands:
  - license activations
  - license activations --release
  - license activate
  - license status --refresh
  - license deactivate
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Move your seat to a new laptop

This cookbook moves a seat from an old computer to a new laptop. A seat is one person, who may link up to three computers, so you free one link and take it on the new laptop. Each step ends with the line it prints when it worked.

## Before you start

- Dockingbird is installed on the new laptop. Check with `dockingbird --version`. If it is not, follow [recover from a failed install](../recover-from-a-failed-install/README.md).
- You have the license key from the purchase email. Both `activate` and `activations` ask for it, hidden.
- You saved what you want from the old computer: results, configs and `hosts.toml`. The [backup guide](../../docs/guides/backup-and-restore.md) lists them.

## 1. Give the seat back from the old laptop

Skip this step when the old laptop is lost or wiped, and go to step 2.

```bash
dockingbird license deactivate
```

The step is done when the product prints this line.

```text
This computer no longer uses a seat of the license.
```

`dockingbird clean --all` does the same and also removes everything Dockingbird made on that computer. When the license server does not answer, it prints [LICENSE_SEAT_STILL_HELD](../../docs/troubleshooting.md#license_seat_still_held) and exits 0. The seat is then still held. Free it in step 2 or step 3.

## 2. Activate the new laptop

```bash
dockingbird license activate --label new-laptop
```

The `--label` value names this computer in the list. A label takes letters, digits, `-` and `.`. The step is done when the product prints the activation line.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
  Computers linked: 3 of 3 (1 seat, 3 computers each)
```

If the line appears, go to step 4. If every computer is linked, the command prints [LICENSE_SEATS_FULL](../../docs/troubleshooting.md#license_seats_full) and exits 1.

```text
Every computer this license admits is linked, so this one can't join.
Free one: dockingbird license activations --release ID
```

Under those lines it names each linked computer, the one seen longest ago first, with its id.

## 3. Free the old laptop

Read the ids again when you need to.

```bash
dockingbird license activations
```

The command asks for the key and prints one line for each linked computer.

```text
{label}: activated {activated}, last seen {seen}, id {id}
```

Pick the old laptop by its label and the day it was last seen. Then free its seat.

```bash
dockingbird license activations --release ID
```

The step is done when the product prints this line and lists the computers that remain.

```text
The seat of activation {id} is free again.
```

A seat that nobody frees stops counting by itself after 90 days. Run `dockingbird license activate --label new-laptop` again on the new laptop.

## 4. Check the status on the new laptop

```bash
dockingbird license status --refresh
```

The `--refresh` flag checks in with the license server first. The step is done when the screen shows the license and this computer's label.

```text
Licensed: {plan}, {seats:seat|seats}, {term}.
  This computer: new-laptop
```

## 5. Check the old laptop, if it still runs

```bash
dockingbird license status --refresh
```

On a computer whose seat was freed from another one, the screen shows this and exits 0.

```text
This computer's seat was freed from another computer.
Activate it again: dockingbird license activate
```

No action is needed. To clear the old laptop for good, run `dockingbird clean --all` on it, which removes what Dockingbird made there.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [LICENSE_KEY_IN_ARGV](../../docs/troubleshooting.md#license_key_in_argv) | The key was typed after the command. Run the command alone. |
| [LICENSE_KEY_INVALID](../../docs/troubleshooting.md#license_key_invalid) | The server does not know the key. Copy it again. |
| [LICENSE_SEATS_FULL](../../docs/troubleshooting.md#license_seats_full) | Free a computer, as in step 3. |
| [LICENSE_OPTION_INVALID](../../docs/troubleshooting.md#license_option_invalid) | A `--label` or `--release` value has a character it does not take. |
| [LICENSE_AUTHORITY_UNAVAILABLE](../../docs/troubleshooting.md#license_authority_unavailable) | The license server was out of reach. Nothing changed. |
| [LICENSE_SEAT_STILL_HELD](../../docs/troubleshooting.md#license_seat_still_held) | `clean --all` could not reach the server. Free the seat as in step 3. |

The whole license story is on the [licensing guide](../../docs/guides/licensing.md).
