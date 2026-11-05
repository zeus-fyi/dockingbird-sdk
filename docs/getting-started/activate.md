---
title: Activate
summary: Give this computer its seat with a license key, or start a trial, and read the result.
audience: first-day
commands:
  - dockingbird license activate
  - dockingbird license trial
  - dockingbird license status
  - dockingbird license activations
  - dockingbird license deactivate
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Activate

This page gives this computer its seat with `dockingbird license activate`, or starts a trial, and shows how to read the result.

## Before you start

- `dockingbird --version` prints a line that starts with `dockingbird`. [Install](install.md) covers it.
- Your license key is in your purchase email. With no key, use the trial in step 3.

## What a seat is

A seat is one person, who may link up to three computers.
A laptop, a desktop and a cloud VM are one seat.
A second Dockingbird home on the same computer, set with another `DOCKINGBIRD_HOME`, shares that computer.
Agents, containers and repos are never counted.
Licensing sends Zeusfyi nothing from a repo or an agent.

Refusing a start for a missing or ended license is not yet available.
In this release every start goes ahead, and a start prints one line when licensing has something to say.
Only a new agent's start ever concerns the license. `sync`, `stop`, `clean`, `status`, `update` and every running agent never stop for it.

## 1. Activate with a key

```bash
dockingbird license activate
```

Dockingbird asks for the key and does not show it.
Without a terminal it reads the key from standard input, so `pbpaste | dockingbird license activate` works too.
The key is never read from the command line.

Two options help a scripted install.
`--label TEXT` names this computer in the list of computers, by default its host name.
`--accept-terms VERSION` accepts the agreement's version.

Done when the command prints the activated line, with the count of linked computers under it.
Then it prints the line that names the terms.

```text
This computer is activated: {plan}, {seats}, {term}.
  Computers linked: 4 of 30 (10 seats, 3 computers each)
```

```text
You use Dockingbird under its terms: {link}
```

The link is the address of Zeusfyi's end-user license agreement.
Activating again on a computer that is already linked keeps its link.

## 2. Read the status

```bash
dockingbird license status
```

Done when the first line reads "Licensed: {plan}, {seats}, {term}."
Under it come how many computers one seat may link, this computer's label, the day the lease ends and the last check-in.
These come from the license file on this computer, with no network.
`dockingbird license status --refresh` checks in with Zeusfyi first.
`dockingbird status` also shows the state in one line once this computer has a license file.

## 3. Start a trial instead

```bash
dockingbird license trial
```

A trial needs no key, and each computer gets one.

Done when the command prints this line, then the terms line.

```text
The trial started on this computer: {plan}, {term}.
```

A second run prints "This computer has had its trial already." and names `dockingbird license activate`.
A trial has these limits.

- It cannot install from the index, which serves an active license only.
- It is not an activation. On an index install, `dockingbird update` answers "Updating Dockingbird needs this computer's license" until you activate with a key.

## 4. A key typed as a word

A key on the command line is refused, because your shell history and other programs can read it.
Nothing runs, and the exit status is 2.

```text
A license key never goes on the command line, where your shell
history and other programs can read it.
Paste it when asked: dockingbird license activate
```

## 5. Seats full, and freeing one

When every computer the license admits is linked, activation stops with exit 1.
It says "Every computer this license admits is linked, so this one can't join." and lists each linked computer with its id.
`dockingbird license activations` lists the computers, and `--release ID` frees one.

```bash
dockingbird license activations --release ID
```

Done when it prints "The seat of activation {id} is free again.", then lists the rest.
Run `dockingbird license activate` again and this computer joins.
`dockingbird license deactivate` gives this computer's own seat back and prints "This computer no longer uses a seat of the license."
`dockingbird clean --all` does the same first.

A computer rebuilt with a new identifier is a new computer each time.
A re-imaged VM, a cloud instance recreated on each deploy, and a container without a machine id are examples.
Run `dockingbird license deactivate` before you destroy one. An unreleased seat stops counting by itself after 90 days.

## Where Dockingbird keeps it

The license file is `license.json` in the Dockingbird home, readable by you alone.
It holds the license document, this computer's id and label, the last check-in, the terms accepted and the download token.
`dockingbird update` uses that token as the index's password, so an activated computer updates with no key.
The first `license` command also downloads Zeusfyi's license program, `zeusfyi-license`, into the `bin` folder of the home.
A computer offline, or an outage at Zeusfyi, interrupts nothing, because the license keeps working for its lease.

## When it fails

- Typing the key after the command name gives [`LICENSE_KEY_IN_ARGV`](../troubleshooting.md#license_key_in_argv) and exit 2. Nothing ran.
- A key the license server has never seen gives [`LICENSE_KEY_INVALID`](../troubleshooting.md#license_key_invalid). Copy it again from the email.
- When every computer of the license is linked, activation ends with [`LICENSE_SEATS_FULL`](../troubleshooting.md#license_seats_full). Free one with `--release ID` and retry.
- A second `license trial` on the same Mac gives [`LICENSE_TRIAL_USED`](../troubleshooting.md#license_trial_used), because each computer gets one trial.
- `update` on an index install with no activation stops with [`LICENSE_UPDATE_NEEDS_LICENSE`](../troubleshooting.md#license_update_needs_license).
- With the license server unreachable you get [`LICENSE_AUTHORITY_UNAVAILABLE`](../troubleshooting.md#license_authority_unavailable). Nothing changed, so retry once you are online.
- `clean --all` offline leaves the seat in use and prints [`LICENSE_SEAT_STILL_HELD`](../troubleshooting.md#license_seat_still_held). Free it from another Mac.
