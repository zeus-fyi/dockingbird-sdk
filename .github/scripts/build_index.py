#!/usr/bin/env python3
"""Build the docs' search files, manifest, llms.txt and troubleshooting index pages, from anywhere in the repo.

Reads README.md, the .md files under docs/ (not docs/plan/), examples/*/README.md and templates/*.md, with front matter
(title, summary, audience, commands; the catalogue docs/troubleshooting.md uses CATALOGUE_META). Writes a page per
domain, docs/troubleshooting/<domain>.md (per id: the id, its "When:" line's first sentence, a link; NATIVE_ left out),
docs/manifest.json and llms.txt in PAGE_GROUPS order, search/chunks.jsonl (chunks cut at H2, H3 and about CAP words;
one per catalogue entry, headed by its domain) and search/index.json.gz (BM25 term counts per chunk and field; flags
and commands count only where a bash block shows them). One line per failed check names the page: broken or missing
front matter, a link to a missing file, an unclosed code fence, a catalogue link whose anchor or text is no id, a
backticked UPPER_SNAKE name one edit off an id. Every output is written anyway, so the query check still runs; then
it exits 1 and CI commits nothing. Output is deterministic (sorted keys, gzip with no timestamp). Standard library only.
"""
import csv
import functools
import gzip
import hashlib
import importlib.util
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = "docs/troubleshooting.md"
CAP = 400
SCHEMA = 1
WALK = ("README.md", "docs/", "examples/*/README.md", "templates/*.md")  # a folder: every .md file under it
EXCLUDE = ("docs/plan/",)  # planning notes: no front matter, and they quote every regression query
GENERATED = {"llms.txt", "docs/manifest.json", "search/chunks.jsonl", "search/index.json.gz", "search/search.py"}
CATALOGUE_META = {"title": "Troubleshooting", "audience": "daily", "commands": [], "summary": "Every message "
                  "Dockingbird prints, by id: when it appears, its text, the next step it gives and its exit status."}
SKIP_PREFIXES = ("NATIVE",)
BLOCKQUOTE = "> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt)."

# (slug, title, audience, what its ids are about, the id prefixes it holds)
DOMAINS = (
    ("install", "install, Docker, licensing and the command line", "first-day",
     "installing, Docker, the license and typing a command", ("LICENSE DOCKER BUILD IMAGE SETUP SETTING SETTINGS "
     "DOCKINGBIRD LOGS UNKNOWN UNEXPECTED OPTION OPTIONS MISSING HELP NOT INTERNAL NATIVE COORDINATOR")),
    ("homes", "homes, checkouts and toolchains", "daily", ("Dockingbird homes, your checkout and its branches, "
     "init, toolchains, project rules and trust"), ("HOME HOMES REPO REPOS BRANCH DETACHED EMPTY LINK TREE SUBMODULE "
     "WORKTREE INIT TOOL TOOLCHAIN DEPS ENV RULES TRUST TRUSTED NOTHING PROJECT")),
    ("agents", "agents, status, sync and clean", "daily", "starting agents, their status, sync, stop and clean",
     ("START AGENT AGENTS NAME NAMES CODEX COPY BOTH ENDED SESSION STOP STOPPED STEP STATUS DETAIL NEEDS EGRESS "
      "ACCEPT SYNC CLEAN CHANGE COMMIT SHARE ALSO OTHERS AS MORE SET")),
    ("bus", "the bus", "daily", "tasks on the bus: send, wait, the inbox, read, questions and results",
     ("SEND SENT INBOX READ RESULTS QUESTION QUESTIONS ANSWER ANSWERED SEARCH RELAY WITHDRAWN WAIT WAITING "
      "INSTRUCTION INSTRUCTIONS DELIVERY TURN BODY")),
    ("connections", "configs, connections and host resources", "daily", ("your own commands, connections, served "
     "resources, browsers and watch"), ("CONFIG CONNECT CONNECTION CONNECTED REVOKE SERVE BROWSER WATCH MANUAL FILE "
     "LOCAL PLAN HARNESS")),
    ("fleet", "the fleet, swarms and the work queue", "team-admin", ("hosts, the fleet scheduler, the control plane, "
     "swarms and the work queue"), "FLEET CP NODE RPC NATS MODE REMOTE SWARM INSPECT WORK"),
    ("benchmarks", "benchmark jobs", "daily", "Harbor benchmark jobs", "HARBOR"),
    ("sign-ins", "sign-ins and the org store", "daily", "signing in, API keys, signing out and the org login",
     "SIGNIN LOGIN LOGOUT API KEY DEVICE BASE SIGNED ORG"),
    ("updates", "updates", "daily", "checking for and installing updates, pins and the switch to a new version",
     "UPDATE VERSION SWITCH STATE PIN"),
    ("gui-and-mcp", "the GUI, the MCP server and shell completion", "integrator",
     "the GUI, the MCP server and shell completion", "GUI UI COMPLETION MCP"),
)
DOMAIN_OF = {prefix: domain[0] for domain in DOMAINS for prefix in domain[4].split()}
DOMAIN_TITLES = {domain[0]: domain[1][:1].upper() + domain[1][1:] for domain in DOMAINS}
DOMAIN_NOTES = {"gui-and-mcp": "The Dockingbird GUI is not yet available to customers."}


def paths(folder, names, suffix=""):
    return [f"{folder}{name}{suffix}" for name in names.split()]


# (llms.txt section, folders whose unlisted pages go at the section's end, its pages in reading order)
PAGE_GROUPS = (
    ("Start here", ("docs/getting-started/",), ["README.md", "docs/quickstart.md"] + paths(
        "docs/getting-started/", "prerequisites.md install.md activate.md first-run.md choose-a-topology.md")
     + ["docs/agent-setup-prompt.md", "docs/faq.md"]),
    ("Concepts", ("docs/concepts/",), paths("docs/concepts/", "architecture.md glossary.md agents-and-the-bus.md "
     "sync-model.md claude-code-and-codex.md swarms-and-roles.md fleet-and-hosts.md fleet-scheduler.md "
     "control-plane.md licensing-model.md hosting-paradigms.md security-model.md observability.md")),
    ("Guides", ("docs/guides/",), paths("docs/guides/", "daily-loop.md delegating-tasks.md connections.md "
     "your-own-commands.md toolchains.md trust-and-repo-settings.md sign-in-and-api-keys.md egress-and-network.md "
     "hosts.md licensing.md updates.md mcp-server.md clean-and-uninstall.md backup-and-restore.md "
     "data-and-privacy.md networking.md tailscale.md other-networks.md cloud-vms.md github.md mcp-and-services.md "
     "databases.md secrets-vault.md swarms.md work-queue.md team-fleet.md fleet-scheduler.md metrics.md "
     "prometheus.md grafana.md harbor.md gui.md")),
    ("Cookbooks and examples", ("examples/",), paths("examples/", (
        "one-mac recover-from-a-failed-install move-your-seat database-without-the-password your-own-review-command "
        "two-macs-ssh cloud-vm-gcloud lock-tool-versions restrict-egress update-with-agents-running "
        "before-you-replace-a-computer team-fleet swarm-from-a-role-library join-a-computer-to-a-control-plane "
        "uninstall-completely fleet-on-a-tailnet host-behind-a-bastion observability test-suite-under-a-lease "
        "change-a-running-swarm"), "/README.md")),
    ("Templates", ("templates/",), ["templates/AGENTS.md"]),
    ("Troubleshooting", ("docs/troubleshooting/",), paths("docs/troubleshooting/", "install-fails.md "
     "licence-refused.md first-start-stops.md") + [f"docs/troubleshooting/{d[0]}.md" for d in DOMAINS] + [CATALOGUE]),
    ("Reference", ("docs/reference/",), paths("docs/reference/", "commands.md integration/exit-codes.md "
     "integration/json.md integration/mcp.md integration/compatibility.md files/hosts-file.md files/org-file.md "
     "files/swarm-definition.md files/app-config.md files/roles-and-connections.md files/project-file.md "
     "files/home-layout.md files/fleet-store.md environment-variables.md limits.md ports-and-hosts.md metrics.md "
     "fleet-tools.md") + ["docs/search.md"]),
    ("Optional", ("docs/release-notes/", "docs/legal/", "docs/"), ["docs/operator-guide.md",
     "docs/release-notes/next.md", "docs/legal/eula.md", "docs/legal/privacy.md"]),
)

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
INLINE = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"!?\[([^\]]*)\]\(\s*<?([^)\s>]*)>?(?:\s+\"[^\"]*\")?\s*\)")
REF_DEF = re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)")
BOLD_RUNIN = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)?\*{2}[^*]+\*{2}")
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`(\[\"'])")
UPPER = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+(?![A-Za-z0-9_])")
TOOL = re.compile(r"(?<![A-Za-z0-9_])(?:agent|fleet)_[a-z0-9_]*[a-z0-9](?![A-Za-z0-9_])")
COMMAND_WORD = re.compile(r"[a-z][a-z-]*[a-z]")
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
BOILERPLATE = re.compile(r"^> Part of the Dockingbird customer docs\.")
SHELL_SPLIT = re.compile(r"&&|\|\||[;|]")

_spec = importlib.util.spec_from_file_location("docs_search", Path(__file__).with_name("search.py"))
_spec.loader.exec_module(S := importlib.util.module_from_spec(_spec))
dumps = functools.partial(json.dumps, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def yaml_scalar(raw):
    raw = raw.strip()
    if raw.startswith('"'):
        return json.loads(raw)
    if raw.startswith("'"):
        if len(raw) < 2 or not raw.endswith("'"):
            raise ValueError(f"a quote is never closed: {raw}")
        return raw[1:-1].replace("''", "'")
    return re.split(r"\s+#", raw, maxsplit=1)[0].strip()


def parse_front_matter(text):
    """(meta, body): meta is None for a page without front matter; ValueError for one this parser cannot read."""
    if not text.startswith("---\n"):
        return None, text
    lines = text.split("\n")
    if "---" not in lines[1:]:
        raise ValueError("the front matter opens with --- and never closes")
    end, meta, key = lines.index("---", 1), {}, None
    for n, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"\s*-\s+(.*)$", line)
        if item and key is not None and isinstance(meta[key], list):
            meta[key].append(yaml_scalar(item.group(1)))
            continue
        pair = re.match(r"([A-Za-z_][\w-]*):(?:\s+(.*))?$", line)
        if not pair:
            raise ValueError(f"front matter line {n} is neither 'key: value' nor '- item': {line.strip()}")
        key, raw = pair.group(1), (pair.group(2) or "").strip()
        if raw.startswith("[") and not raw.endswith("]"):
            raise ValueError(f"front matter line {n}: a [list] must close on its own line")
        inner = raw[1:-1].strip() if raw.startswith("[") else None
        meta[key] = ([] if raw == "" or inner == "" else yaml_scalar(raw) if inner is None
                     else [yaml_scalar(i) for i in next(csv.reader([inner], skipinitialspace=True))])
    return meta, "\n".join(lines[end + 1:])


def meta_errors(meta):
    errors = [f"front matter lacks a {key}" for key in ("title", "summary")
              if not isinstance(meta.get(key), str) or not meta[key].strip()]
    if meta.get("audience") not in S.AUDIENCES:
        errors.append(f"front matter audience {meta.get('audience')!r} is not one of {', '.join(S.AUDIENCES)}")
    if not isinstance(meta.get("commands"), list) or not all(isinstance(c, str) for c in meta["commands"]):
        errors.append("front matter commands is not a list of strings")
    return errors


def code_mask(lines):
    """Per line, False or its fenced block's language word ("code" if none); and the index of a fence left open."""
    mask, fence, opened, word = [], None, None, False
    for n, line in enumerate(lines):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence, opened, word = match.group(1), n, (line[match.end():].split() or ["code"])[0].lower()
            mask.append(word if match else False)
            continue
        mask.append(word)
        closing = match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence)
        if closing and not line[match.end():].strip():
            fence = None
    return mask, opened if fence is not None else None


def first_sentence(text):
    """The text up to its first period followed by a space or its end; a period inside `code` does not count."""
    end = re.search(r"\.(?=\s|$)", INLINE.sub(lambda m: "x" * len(m.group(0)), text))
    return text[:end.end()] if end else text


def slug(text, seen):
    """The anchor GitHub gives a heading, with -1, -2 for a repeat on the same page."""
    text = re.sub(r"<[^>]+>", "", LINK.sub(r"\1", text)).strip().lower()
    base = re.sub(r"[^\w\- ]", "", text).replace(" ", "-")
    seen[base] += 1
    return base if seen[base] == 1 else f"{base}-{seen[base] - 1}"


def sections(lines, mask, title):
    """A page cut at its H1, H2 and H3 headings: dicts of heading path, anchor, lines and code mask."""
    out, seen, h1, h2 = [], Counter(), None, None
    current = {"path": [title], "anchor": "", "lines": [], "mask": []}
    for line, code in zip(lines, mask):
        match = None if code else HEADING.match(line)
        if match:
            level, text = len(match.group(1)), match.group(2)
            anchor = slug(text, seen)
            if level <= 3:
                out.append(current)
                h1, h2 = (text, None) if level == 1 else (h1, text) if level == 2 else (h1, h2)
                path = [h1 or title] + ([h2] if h2 and level > 1 else []) + ([text] if level == 3 else [])
                current = {"path": path, "anchor": anchor, "lines": [], "mask": []}
                continue
        if not BOILERPLATE.match(line):
            current["lines"].append(line)
            current["mask"].append(code)
    return [section for section in out + [current] if "".join(section["lines"]).strip()]


def blocks(lines, mask):
    """Paragraphs, items opened by a bold run-in heading, and whole fenced blocks, as text."""
    out, current, in_code = [], [], False
    for line, code in zip(lines, mask):
        if code != in_code or (not code and (not line.strip() or BOLD_RUNIN.match(line))):
            if current:
                out.append("\n".join(current))
            current, in_code = [], code
        if code or line.strip():
            current.append(line)
    return out + (["\n".join(current)] if current else [])


def split_unit(text):
    """A unit over CAP words, cut at line breaks, else at sentence breaks, else every CAP words."""
    lines = [line for line in text.split("\n") if line.strip()]
    if len(lines) > 1:
        return lines
    parts = SENTENCE.split(text)
    if len(parts) > 1:
        return parts
    words = text.split()
    return [" ".join(words[i:i + CAP]) for i in range(0, len(words), CAP)]


def pack(units):
    """Units packed in order into groups of at most CAP words."""
    groups, current, size, stack = [], [], 0, list(reversed(units))
    while stack:
        unit = stack.pop()
        words = len(unit.split())
        if words > CAP:
            stack.extend(reversed(split_unit(unit)))
            continue
        if current and size + words > CAP:
            groups.append(current)
            current, size = [], 0
        current.append(unit)
        size += words
    return groups + ([current] if current else [])


def command(span):
    """`dockingbird --json license activations --release ID` gives "dockingbird license activations"."""
    words = span.split()
    while words and ASSIGNMENT.match(words[0]):
        words = words[1:]
    if not words or words[0] != "dockingbird":
        return None
    i, found = 1, []
    while i < len(words) and words[i].startswith("-"):
        i += 2 if words[i] == "--home" else 1
    while i < len(words) and len(found) < 3 and COMMAND_WORD.fullmatch(words[i]):
        found.append(words[i])
        i += 1
    return " ".join(["dockingbird"] + found) if found else None


def make_chunk(page, section, text, part, ids, entry):
    """One chunk with its fields and its term counts per field; a catalogue entry is headed by its domain."""
    path = [DOMAIN_TITLES[entry["domain"]], entry["id"]] if entry else section["path"]
    heading, lines = " > ".join(path), text.split("\n")
    mask = code_mask(lines)[0]
    shell = [piece for line, word in zip(lines, mask) if word == "bash" and not FENCE.match(line)
             for piece in SHELL_SPLIT.split(line)]  # flags and commands count where a bash block shows them
    commands = [found for found in map(command, shell) if found]
    named = ([entry["id"]] if entry else []) + [name for name in UPPER.findall(text) if name in ids]
    tools, flags = TOOL.findall(text), [t for t in S.tokenize(" ".join(shell)) if t.startswith("--")]
    terms = {"body": S.tokenize(text), "heading": S.tokenize(heading), "flags": flags,
             "ids": [t for name in named for t in S.split_name(name)],
             "commands": [t for found in commands for t in [found] + found.split()[1:2]],
             "tools": [t for name in tools for t in S.split_name(name)]}
    lead = entry["when"] if entry else next((line.strip() for line, code in zip(lines, mask)
                                             if not code and line.strip()[:1] not in ("", "|", "#")), "")
    chunk = {"chunk_id": hashlib.sha1(f"{page['path']}\n{heading}\n{part}".encode()).hexdigest()[:16],
             "path": page["path"], "heading": heading, "anchor": section["anchor"], "text": text,
             "commands": sorted(set(commands)), "flags": sorted(set(flags)), "ids": sorted(set(named)),
             "tools": sorted(set(tools)), "audience": page["meta"].get("audience", ""),
             "summary": first_sentence(lead)}
    if entry:
        chunk.update({key: entry[key] for key in ("id", "when", "exit_status", "domain")})
    return chunk, {field: Counter(tokens) for field, tokens in terms.items() if tokens}


def catalogue_entries(text):
    """The catalogue's `### ID` entries: id, "When:" line, exit status and domain; and the errors."""
    lines, entries, errors = text.split("\n"), [], []
    for section in sections(lines, code_mask(lines)[0], "Troubleshooting"):
        if len(section["path"]) != 3:
            continue
        name, body = section["path"][2], "\n".join(section["lines"])
        when = re.search(r"^When: (.+?)(?:\n\n|\Z)", body, re.DOTALL | re.MULTILINE)
        status = re.search(r"^Exit status: (.+?)\.?$", body, re.MULTILINE)
        domain = DOMAIN_OF.get(name.split("_")[0])
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name) or not when or not status or not domain:
            errors.append(f"{CATALOGUE}: {name} lacks an id, a When:, an Exit status: or a prefix in DOMAINS")
            continue
        entries.append({"id": name, "when": " ".join(when.group(1).split()), "exit_status": status.group(1),
                        "domain": domain})
    return entries, errors


def domain_page(domain, entries):
    """The index page of one domain, and how many ids it lists."""
    name, title, audience, about, _ = domain
    listed = [e for e in entries if e["domain"] == name and not e["id"].startswith(SKIP_PREFIXES)]
    heading = f"Troubleshooting index: {title}"
    summary = f"The {len(listed)} message ids about {about}, each with when it appears."
    out = ["---", f"title: {json.dumps(heading)}", f"summary: {json.dumps(summary)}", f"audience: {audience}",
           "commands: []", "---", "", BLOCKQUOTE, "", f"# {heading}", "",
           ("Find a message id below to see when Dockingbird prints that message. Add `--verbose` to a command and "
            "every message also shows its id. With `--json`, each envelope carries the id as its `id` key. Each id "
            "links to its entry in the [catalogue](../troubleshooting.md): the message text, the next step and the "
            f"exit status. This page holds the {len(listed)} ids about {about}.")]
    out += (["", DOMAIN_NOTES[name]] if name in DOMAIN_NOTES else []) + ["", "| Id | When it appears |", "|---|---|"]
    out += [f"| [`{e['id']}`](../troubleshooting.md#{e['id'].lower()}) | {when} |"
            for e in listed for when in [first_sentence(e["when"]).replace("|", "\\|")]]
    return "\n".join(out) + "\n", len(listed)


def link_errors(page, lines, mask, ids):
    """Links to missing files, links into the catalogue that name no id, and backticked names one typo off an id."""
    errors, base = [], (ROOT / page).parent
    for line, code in zip(lines, mask):
        if code:
            continue
        bare = INLINE.sub(lambda m, line=line: m.group(0) if "](" in line[m.end():m.end() + 2] else "", line)
        links = [(m.group(1), m.group(2)) for m in LINK.finditer(bare)]
        links += [("", m.group(1)) for m in [REF_DEF.match(bare)] if m]
        for text, target in links:
            if not target or target.startswith("#") or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            file_part, _, anchor = target.partition("#")
            file_part = unquote(file_part.split("?")[0])
            resolved = ((ROOT / file_part.lstrip("/")) if file_part.startswith("/") else base / file_part).resolve()
            name = text.strip("` ")
            if not resolved.is_relative_to(ROOT) or not (resolved.exists() or
                                                          resolved.relative_to(ROOT).as_posix() in GENERATED):
                errors.append(f"{page}: links to {target}, a file that does not exist in this repository")
            elif resolved == ROOT / CATALOGUE and anchor and (anchor.upper() not in ids or
                                                             (UPPER.fullmatch(name) and name != anchor.upper())):
                errors.append(f"{page}: links to {target} as {text or 'a reference'}, which is no catalogue id")
        for name in sorted({span.strip() for span in INLINE.findall(line)} - ids):
            near = min((S.distance(name, i, 1), i) for i in ids) if UPPER.fullmatch(name) else (2, None)
            if near[0] <= 1:
                errors.append(f"{page}: names {name}, which is no catalogue id (did it mean {near[1]}?)")
    return errors


def load_page(path, ids):
    """A page's metadata, title, lines and code mask; and its errors."""
    text, errors = (ROOT / path).read_text(encoding="utf-8"), []
    try:
        meta, body = parse_front_matter(text)
    except ValueError as error:
        meta, body = None, text
        errors.append(f"{path}: {error}")
    if meta is None:
        meta = dict(CATALOGUE_META) if path == CATALOGUE else {}
        errors += [] if errors or meta else [f"{path}: no front matter (title, summary, audience, commands)"]
    else:
        errors += [f"{path}: {error}" for error in meta_errors(meta)]
    lines, offset = body.split("\n"), text[:len(text) - len(body)].count("\n")
    mask, opened = code_mask(lines)
    if opened is not None:
        errors.append(f"{path}: the code fence opened at line {opened + offset + 1} is never closed")
    errors += link_errors(path, lines, mask, ids) if path != CATALOGUE else []
    h1 = next((m.group(2) for line, code in zip(lines, mask) if not code
               for m in [HEADING.match(line)] if m and len(m.group(1)) == 1), None)
    title = meta["title"] if isinstance(meta.get("title"), str) and meta["title"].strip() else h1 or path
    return {"path": path, "meta": meta, "title": title, "lines": lines, "mask": mask}, errors


def page_chunks(page, ids, entries):
    """A page's chunks in order: the catalogue one per entry, every other page by section and size."""
    out, seen = [], Counter()
    for section in sections(page["lines"], page["mask"], page["title"]):
        entry = entries.get(section["path"][-1]) if page["path"] == CATALOGUE and len(section["path"]) == 3 else None
        groups = [["\n".join(section["lines"]).strip()]] if entry else pack(blocks(section["lines"], section["mask"]))
        seen[tuple(section["path"])] += 1
        out += [make_chunk(page, section, "\n\n".join(group), f"{seen[tuple(section['path'])]}.{part}", ids, entry)
                for part, group in enumerate(groups)]
    return out


def order_pages(found):
    """Pages in reading order (PAGE_GROUPS, then each group's unlisted pages by path), their groups, the unlisted."""
    keys, unlisted = {}, []
    for path in found:
        for g, (_, folders, listed) in enumerate(PAGE_GROUPS):
            if path in listed or path.startswith(folders):
                keys[path] = (g, listed.index(path) if path in listed else len(listed), path)
                unlisted += [] if path in listed else [path]
                break
    return sorted(found, key=keys.get), {path: keys[path][0] for path in found}, unlisted


def write(path, data):
    (target := ROOT / path).parent.mkdir(parents=True, exist_ok=True)
    return target.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)


def llms_txt(pages, group_of):
    """The llms.txt file: the README's title and summary, then one line per page under its section."""
    readme = next((page for page in pages if page["path"] == "README.md"), None)
    out = [f"# {readme['title'] if readme else 'Dockingbird'}", ""]
    out += [f"> {readme['meta']['summary']}", ""] if readme and readme["meta"].get("summary") else []
    out.append("These are the customer docs, one line per page in reading order. Search them from a clone with "
               "`python3 search/search.py \"your words\"` ([how the search ranks](docs/search.md)). "
               "[docs/manifest.json](docs/manifest.json) lists the same pages with their audience, commands and "
               "message ids.")
    section = None
    for page in pages:
        if PAGE_GROUPS[group_of[page["path"]]][0] != section:
            section = PAGE_GROUPS[group_of[page["path"]]][0]
            out += ["", f"## {section}", ""]
        summary = page["meta"].get("summary", "")
        out.append(f"- [{page['title']}]({page['path']})" + (f": {summary}" if summary else ""))
    return "\n".join(out) + "\n"


def main():
    entries, errors = catalogue_entries((ROOT / CATALOGUE).read_text(encoding="utf-8"))
    ids, counts = {entry["id"] for entry in entries}, {}
    for domain in DOMAINS:
        text, counts[domain[0]] = domain_page(domain, entries)
        errors += [] if counts[domain[0]] else [f"{CATALOGUE}: domain {domain[0]} lists no id; drop it from DOMAINS"]
        write(f"docs/troubleshooting/{domain[0]}.md", text)
    found = sorted({p.relative_to(ROOT).as_posix() for pattern in WALK for p in (
        (ROOT / pattern).rglob("*.md") if pattern.endswith("/") else ROOT.glob(pattern)) if p.is_file()})
    ordered, group_of, unlisted = order_pages([path for path in found if not path.startswith(EXCLUDE)])
    loaded = [load_page(path, ids) for path in ordered]
    pages = [page for page, _ in loaded]
    errors += [error for _, page_errors in loaded for error in page_errors]
    by_id, chunks, counters = {entry["id"]: entry for entry in entries}, [], []
    for order, page in enumerate(pages):
        if page["path"].startswith("docs/troubleshooting/") and page["path"][21:-3] in DOMAIN_OF.values():
            continue  # an index page's lines repeat the catalogue's, whose entries are the better result
        for position, (chunk, counter) in enumerate(page_chunks(page, ids, by_id)):
            chunks.append(dict(chunk, order=[order, position]))
            counters.append(counter)
    manifest = [{"page": page["path"], "title": page["title"], "summary": page["meta"].get("summary", ""),
                 "audience": page["meta"].get("audience", ""), "commands": page["meta"].get("commands", []),
                 "ids": sorted(ids if page["path"] == CATALOGUE else
                               {n for line in page["lines"] for n in UPPER.findall(line)} & ids)} for page in pages]
    write("docs/manifest.json", '{"pages": [\n' + ",\n".join(map(dumps, manifest)) + f'\n], "schema": {SCHEMA}}}\n')
    write("llms.txt", llms_txt(pages, group_of))
    write("search/chunks.jsonl", "".join(dumps(chunk) + "\n" for chunk in chunks))
    vocab = sorted({term for counter in counters for field in counter.values() for term in field})
    number = {term: n for n, term in enumerate(vocab)}
    df = Counter(term for counter in counters for term in set().union(*counter.values()))
    index_chunks = [{"chunk_id": c["chunk_id"], "audience": c["audience"], "catalogue": c["path"] == CATALOGUE,
                     "order": c["order"], "tf": {field: [x for t, n in sorted(terms.items()) for x in (number[t], n)]
                                                 for field, terms in sorted(counter.items())}}
                    for c, counter in zip(chunks, counters)]
    index = {"schema": SCHEMA, "k1": S.K1, "b": S.B, "boosts": S.BOOSTS, "vocab": vocab, "chunks": index_chunks,
             "df": [df[term] for term in vocab], "ids": sorted(name.lower() for name in ids)}
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9) as handle:
        handle.write(dumps(index).encode("utf-8"))
    size = write("search/index.json.gz", buffer.getvalue())
    print(f"pages={len(pages)} chunks={len(chunks)} ids={len(ids)} index={size} bytes vocabulary={len(vocab)}")
    print("domain pages: " + " ".join(f"{name}={n}" for name, n in counts.items()))
    if unlisted:
        print("pages placed by folder, not listed in PAGE_GROUPS: " + " ".join(unlisted))
    for error in errors:
        print(f"error: {error}")
    print(f"errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
