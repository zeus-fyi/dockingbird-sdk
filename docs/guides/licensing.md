---
title: Licensing
summary: Activate a computer, read its status, list and free seats, move a seat to a new laptop, give a seat back, start a trial, and read each license message.
audience: first-day
commands:
  - license activate
  - license status --refresh
  - license activations --release
  - license deactivate
  - license trial
  - clean --all
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Licensing

Take a seat, read it, free it, move it to a new laptop, give it back. Each of those is one command under dockingbird license, and each is below with the line it prints when it worked. After them come the trial, the offline behavior and a table of every license message. This release does not enforce licensing, so no start is refused for a license. A refused start and its grace periods are not yet available.

## Before you start

- Dockingbird is installed. Check with `dockingbird --version`, which prints a version. If it is not, see [install fails](../troubleshooting/install-fails.md).
- You have the license key from your purchase email. Dockingbird never prints it back.
- The computer can reach the license server. The first `dockingbird license` command downloads a small license program from it, so an offline first run stops with `LICENSE_AUTHORITY_UNAVAILABLE`.

## What a seat is

A seat is one person. That person may link up to three computers to it, for example a laptop, a desktop and a cloud VM. A license with 10 seats admits 30 computers.

A second Dockingbird home on the same computer shares that computer's link. Agents, containers and repos are never counted. A computer rebuilt with a new identifier counts as a new computer each time. That covers a re-imaged VM, a cloud instance recreated on each deploy, and a container or CI runner with no machine id.

Licensing only concerns a new agent's start. `sync`, `stop`, `clean`, `status`, `results`, `read`, `inbox`, `update` and every running agent never wait on it, so your work always comes back.

## Activate a computer

```bash
dockingbird license activate
```

The command asks for the key with the input hidden. Without a terminal it reads the key from standard input, so a clipboard works on a Mac.

```bash
pbpaste | dockingbird license activate
```

A key typed as an argument is refused with exit 2 before anything runs. That keeps it out of your shell history and out of `ps`. The refusal is `LICENSE_KEY_IN_ARGV`.

The step is done when the product prints this line, then the terms line and a count of linked computers.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
You use Dockingbird under its terms: {link}
  Computers linked: 4 of 30 (10 seats, 3 computers each)
```

Two options help a scripted install. `--label TEXT` names this computer in the list, and its default is the hostname. `--accept-terms VERSION` accepts that version of the agreement without a prompt. Activating again on a linked computer keeps its link.

## Read the status

```bash
dockingbird license status
```

This reads the license file on the computer and uses no network. It shows the state, the plan, the seats and the end of the term. Then it shows how many computers one seat may link, this computer's label, the end of its lease and the last check-in.

```bash
dockingbird license status --refresh
```

With `--refresh` the command checks in with the license server first. Use it after you renew a license, after you free a seat from another computer, and after coming back online.

`dockingbird status` shows the license state in one line once the computer has a license file. With `--json`, status prints its values as fields a script can read.

## List the computers on a seat

```bash
dockingbird license activations
```

The command asks for the key, as `activate` does, and prints the count line and one line per linked computer. The list holds at most 80 computers, those seen longest ago first. When there are more, a line above it says how many it shows.

```text
{label}: activated {activated}, last seen {seen}, id {id}
Free a seat: dockingbird license activations --release ID
```

## Free a seat with --release

```bash
dockingbird license activations --release ID
```

The list above gives each computer an id. Pass the id of the computer you want to free. The product prints this line when it worked, then lists the computers that remain.

```text
The seat of activation {id} is free again.
```

Use this for a laptop that was lost or wiped. A seat that nobody frees stops counting after 90 days.

## Move a seat to a new laptop

You change laptops, and the license already links three computers. The seat moves in four steps. The [cookbook](../../examples/move-your-seat/README.md) shows each one with its output.

1. On the old laptop, if you still have it, run `dockingbird license deactivate`. Skip this step when the old laptop is lost.
2. On the new laptop, install Dockingbird as the [install guide](../getting-started/install.md) describes.
3. Run `dockingbird license activate` on the new laptop. With the old link still held, it prints `LICENSE_SEATS_FULL` and names every linked computer with its id.
4. Free the old laptop with `dockingbird license activations --release ID`, then run `dockingbird license activate` again.

Run `dockingbird license status --refresh` on the new laptop to confirm. If the old laptop is still on, the same command there prints `This computer's seat was freed from another computer.` and the next step `dockingbird license activate`.

## Give a seat back

```bash
dockingbird license deactivate
```

This frees the seat this computer holds and removes its license file. It is done when the product prints this line.

```text
This computer no longer uses a seat of the license.
```

`dockingbird clean --all` gives the seat back first, then removes everything Dockingbird made. When the license server does not answer, `clean --all` still finishes and prints `LICENSE_SEAT_STILL_HELD`. Free that seat from another computer with `dockingbird license activations`. Run one of these two commands before you destroy a computer, a VM or a runner.

## Start a trial

```bash
dockingbird license trial
```

A trial needs no key and is allowed once per computer. The step is done when the product prints this line.

```text
The trial started on this computer: {plan}, {term}.
```

A second trial on the same computer prints `LICENSE_TRIAL_USED`, and the next step is `dockingbird license activate` with a key. A trial cannot install from the release index and cannot update. `dockingbird update` on an index install needs an activation and says so with `LICENSE_UPDATE_NEEDS_LICENSE`.

## Offline behavior and day counts

`dockingbird license status` needs no network, so it works anywhere. A command that asks the license server, such as `--refresh`, `activations` or `deactivate`, prints `LICENSE_AUTHORITY_UNAVAILABLE` when the server is out of reach. It exits 1 and changes nothing.

Without a check-in the license keeps working for its lease, so an offline computer or an outage at the license server interrupts nothing. The status screen names the stage the computer is in.

| What status prints | What it means | What you run |
|---|---|---|
| `The license server hasn't answered lately; agents start while the lease lasts.` | The last check-in is old. The lease still holds. | `dockingbird license status --refresh` |
| `It ends soon: renew it to keep starting new agents after that.` | The term ends within the warning window. | Renew the license. |
| `The license's term ended.` | The term is over. The installed version keeps working. New releases need a renewed license. | Renew, then `dockingbird license status --refresh` |
| `The license server hasn't answered for too long.` | The offline gap passed the limit. | Get online, then `dockingbird license status --refresh` |

Four figures are each the term the license names. They are the warning window, the length of a lease, the offline limit and the grace after a term ends. The status screen prints the lease end as `Lease until` and the last check-in as `Last check-in`. The one fixed figure on a customer page is 90 days for a seat nobody released.

## What each message means

A message id also arrives as `id` in `--json` output. The links lead to the catalogue entry with the full text.

| Message id | What it means | Exit |
|---|---|---|
| `LICENSE_KEY_IN_ARGV` | The key was typed as an argument. Nothing ran. | 2 |
| `LICENSE_KEY_INVALID` | The license server does not know that key, or the text is not a key. | 1 |
| `LICENSE_SEATS_FULL` | Every computer the license admits is linked. Free one. | 1 |
| `LICENSE_TRIAL_USED` | This computer has had its trial. Activate with a key. | 1 |
| `LICENSE_UPDATE_NEEDS_LICENSE` | An index install updates only on an activated computer. | 1 |
| `LICENSE_AUTHORITY_UNAVAILABLE` | The license server was out of reach. Nothing changed. | 1 |
| `LICENSE_AUTHORITY_REFUSED` | The server refused for a reason with no wording of its own. | 1 |
| `LICENSE_PLATFORM_UNSUPPORTED` | The license program runs on Apple silicon Macs and arm64 Linux only. | 1 |
| `LICENSE_SEAT_STILL_HELD` | `clean --all` could not reach the server, so the seat is held. | 0 |
| `LICENSE_OPTION_INVALID` | A `--label`, `--accept-terms` or `--release` value has a character it does not take. | 2 |

Four more ids mean the license program is missing or damaged: `LICENSE_CLIENT_DAMAGED`, `LICENSE_CLIENT_UNAVAILABLE`, `LICENSE_CLIENT_DIGEST_MISMATCH` and `LICENSE_CLIENT_PATH_INVALID`. Each prints its next step. Run `dockingbird update` for the damaged and digest ids, `dockingbird license status` for the unavailable one, and unset the variable the message names for the path one.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [LICENSE_KEY_IN_ARGV](../troubleshooting.md#license_key_in_argv) | Paste the key when asked. |
| [LICENSE_KEY_INVALID](../troubleshooting.md#license_key_invalid) | Check the key from your purchase email. |
| [LICENSE_SEATS_FULL](../troubleshooting.md#license_seats_full) | Free a computer with `--release ID`. |
| [LICENSE_TRIAL_USED](../troubleshooting.md#license_trial_used) | Activate with a key. |
| [LICENSE_UPDATE_NEEDS_LICENSE](../troubleshooting.md#license_update_needs_license) | Activate, then update again. |
| [LICENSE_AUTHORITY_UNAVAILABLE](../troubleshooting.md#license_authority_unavailable) | Get online and run the command again. |
| [LICENSE_AUTHORITY_REFUSED](../troubleshooting.md#license_authority_refused) | Read the detail line the server returned. |
| [LICENSE_PLATFORM_UNSUPPORTED](../troubleshooting.md#license_platform_unsupported) | Use an Apple silicon Mac or arm64 Linux. |
| [LICENSE_SEAT_STILL_HELD](../troubleshooting.md#license_seat_still_held) | Free the seat from another computer. |
| [LICENSE_OPTION_INVALID](../troubleshooting.md#license_option_invalid) | Run `dockingbird license -h`. |
| [LICENSE_CLIENT_UNAVAILABLE](../troubleshooting.md#license_client_unavailable) | Run `dockingbird license status` to download the program again. |
| [LICENSE_CLIENT_DAMAGED](../troubleshooting.md#license_client_damaged) | Run `dockingbird update`. |

For the story of each refusal in the order a reader meets it, see [license refused](../troubleshooting/licence-refused.md). The idea behind seats is on the [licensing model](../concepts/licensing-model.md) page.
