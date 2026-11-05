#!/usr/bin/env python3
"""Search the Dockingbird docs from a clone, offline, with the standard library only.

    python3 search/search.py "seats full" [--audience first-day] [--top 10] [--index PATH]

It reads search/index.json.gz (BM25 term counts) and search/chunks.jsonl (the sections' text), both written by
.github/scripts/build_index.py, and prints the best sections: for each, the page path with the section's anchor, the
score, the heading path and the section's first line. Python 3.9 or later. The ranking rules, in the order they apply:

1. Spelling. A query word missing from the index becomes the nearest index word within two edits (one edit for a
   word of three to five characters; none for a shorter word or a word with a digit), and the output says so.
2. Phrase first. A query of three words or more that a section holds whole puts that section above every section
   that does not. The test folds case, drops Markdown marks and lets a {placeholder} of a message match any one word
   ({n:noun|nouns} matches a number with its noun). Among such sections the catalogue's entries come first, so a line
   copied from the screen lands on its entry.
3. The catalogue. When the query names a message id, the catalogue's entries rank over the other pages; otherwise
   under them. A query names an id when one of its words is an id, or when two or more of its words joined by "_"
   spell an id whole or without its first part: "seats full" names LICENSE_SEATS_FULL.
4. BM25 per field, each field's score multiplied by its boost and summed: ids, commands, flags and tools 5, headings 2,
   the text 1. "-" and "_" stay inside a word, and ids and tool names are also indexed split at "_". A command is
   indexed whole and by its subcommand, the word after "dockingbird", so "sync" matches "dockingbird sync" and
   "install" does not match "dockingbird mcp install". --audience doubles the score of sections for that reader.
5. Ties go to page order in docs/manifest.json, then to the section's place on its page. A long section cut into
   several chunks is listed once, at its best chunk.

It exits 0 when it prints a result, 1 when nothing matches and 2 when the arguments or the index files are wrong.
The workflow copies this file to search/search.py on every run; build_index.py imports its tokenizer from here.
"""
from __future__ import annotations

import gzip
import json
import math
import re
import sys
from pathlib import Path

AUDIENCES = ("first-day", "daily", "integrator", "team-admin")
BOOSTS = {"body": 1.0, "heading": 2.0, "ids": 5.0, "commands": 5.0, "flags": 5.0, "tools": 5.0}
AUDIENCE_BOOST = 2.0
K1, B = 1.2, 0.75
PHRASE_MIN_WORDS = 3
FIRST_LINE_CHARS = 160
SCHEMA = 1
USAGE = 'usage: search.py "words" [--audience first-day|daily|integrator|team-admin] [--top N] [--index PATH]'

TOKEN = re.compile(r"-{0,2}[a-z0-9][a-z0-9_-]*")
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
PLACEHOLDER = re.compile(r"\{[^{}\s]*\}")
COUNT_PLACEHOLDER = re.compile(r"(.*)\{[^{}:\s]*:([^{}\s]*\|[^{}\s]*)\}(.*)")


def tokenize(text):
    """Lower-case words. "-" and "_" stay inside a word, and a leading "-" or "--" stays on a flag."""
    return [m.group().rstrip("-_") for m in TOKEN.finditer(text.lower())]


def split_name(name):
    """An id or a tool name, whole and split at "_": license_seats_full, license, seats, full."""
    name = name.lower()
    return [name] + [part for part in name.split("_") if part]


def command_grams(words):
    """The whole commands a query spells: "dockingbird license activations" adds two grams."""
    grams = []
    for i, word in enumerate(words):
        if word == "dockingbird":
            grams.extend(" ".join(words[i:j]) for j in range(i + 2, min(i + 4, len(words)) + 1))
    return grams


def fold(text):
    """Text as the phrase test reads it: case folded, link targets, backticks and asterisks dropped."""
    text = LINK.sub(r"\1", text).replace("`", "").replace("*", "").replace("’", "'")
    return " ".join(text.lower().split())


def pattern_words(text):
    """A folded section as words; a word holding a {placeholder} becomes a regular expression."""
    out = []
    for word in text.split():
        count = COUNT_PLACEHOLDER.fullmatch(word)
        if count:
            nouns = "|".join(re.escape(noun) for noun in count.group(2).split("|"))
            out.append(("rx", re.compile(re.escape(count.group(1)) + r"\S+")))
            out.append(("rx", re.compile("(?:" + nouns + ")" + re.escape(count.group(3)))))
        elif PLACEHOLDER.search(word):
            out.append(("rx", re.compile(r"\S+".join(re.escape(p) for p in PLACEHOLDER.split(word)))))
        else:
            out.append(("lit", word))
    return out


def distance(a, b, limit):
    """Levenshtein distance, or limit + 1 as soon as it must exceed the limit."""
    if abs(len(a) - len(b)) > limit or len(set(a) ^ set(b)) > 2 * limit:
        return limit + 1
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (char_a != char_b)))
        if min(current) > limit:
            return limit + 1
        previous = current
    return previous[-1]


class Index:
    """The BM25 index of build_index.py joined with its chunks, with postings built at load."""

    def __init__(self, data, chunks):
        if data.get("schema") != SCHEMA:
            raise ValueError(f"index schema {data.get('schema')!r}; this search.py reads schema {SCHEMA}")
        if [c["chunk_id"] for c in data["chunks"]] != [c["chunk_id"] for c in chunks]:
            raise ValueError("index.json.gz and chunks.jsonl come from different builds; run build_index.py again")
        self.chunks = [chunk | entry for chunk, entry in zip(chunks, data["chunks"])]
        for chunk in self.chunks:
            chunk["first"] = next((line.strip() for line in chunk["text"].split("\n")
                                   if line.strip() and not line.lstrip().startswith(("```", "~~~"))), "")
        self.vocab = data["vocab"]
        self.df = data["df"]
        self.boosts = data["boosts"]
        self.k1, self.b = data["k1"], data["b"]
        self.term = {term: n for n, term in enumerate(self.vocab)}
        self.ids = set(data["ids"])
        self.id_forms = self.ids | {name.split("_", 1)[1] for name in self.ids if "_" in name}
        self.postings, self.lengths, totals = {}, [], {}
        for c, chunk in enumerate(self.chunks):
            self.lengths.append({field: sum(flat[1::2]) for field, flat in chunk["tf"].items()})
            for field, flat in chunk["tf"].items():
                totals.setdefault(field, []).append(self.lengths[c][field])
                for k in range(0, len(flat), 2):
                    self.postings.setdefault(flat[k], []).append((c, field, flat[k + 1]))
        self.average = {field: sum(lengths) / len(lengths) for field, lengths in totals.items()}
        self.folded = [None] * len(self.chunks)
        self.patterns = {}

    def pages(self):
        """Every (path, anchor) the index holds, and every path."""
        pairs = {(chunk["path"], chunk["anchor"]) for chunk in self.chunks}
        return pairs, {path for path, _ in pairs}

    def correct(self, words):
        """Each word missing from the index, replaced by its nearest index word, with a note per change."""
        out, notes = [], []
        for word in words:
            core = word.lstrip("-")
            if word in self.term or len(core) <= 2 or any(char.isdigit() for char in word):
                out.append(word)
                continue
            limit = 1 if len(core) <= 5 else 2
            best = None
            for n, term in enumerate(self.vocab):
                if " " not in term:
                    d = distance(word, term, limit)
                    if d <= limit and (best is None or (d, -self.df[n], term) < best):
                        best = (d, -self.df[n], term)
            if best:
                out.append(best[2])
                notes.append(f'spelling: "{word}" -> "{best[2]}"')
            else:
                out.append(word)
                notes.append(f'spelling: no index word within {limit} edit{"s" if limit > 1 else ""} of "{word}"')
        return out, notes

    def names_id(self, words):
        """True when a word is an id, or two or more words joined by "_" spell an id whole or without its prefix."""
        if any(word in self.ids for word in words):
            return True
        return len(words) >= 2 and "_".join(words) in self.id_forms

    def bm25(self, terms):
        scores = {}
        for term in terms:
            n = self.term.get(term)
            if n is None:
                continue
            idf = math.log(1 + (len(self.chunks) - self.df[n] + 0.5) / (self.df[n] + 0.5))
            for c, field, tf in self.postings.get(n, ()):
                norm = self.k1 * (1 - self.b + self.b * self.lengths[c][field] / self.average[field])
                scores[c] = scores.get(c, 0.0) + idf * self.boosts[field] * tf * (self.k1 + 1) / (tf + norm)
        return scores

    def holds(self, c, phrase):
        """True when section c holds the folded phrase whole, placeholders matching one word each."""
        if self.folded[c] is None:
            chunk = self.chunks[c]
            self.folded[c] = fold(chunk["heading"].split(" > ")[-1] + "\n" + chunk["text"])
        hay = self.folded[c]
        if phrase in hay:
            return True
        query = phrase.split()
        if "{" not in hay or sum(1 for word in query if word in hay) < 2:
            return False
        if c not in self.patterns:
            self.patterns[c] = pattern_words(hay)
        words, last = self.patterns[c], len(query) - 1
        for start in range(len(words) - last):
            literal = 0
            for i, q in enumerate(query):
                kind, p = words[start + i]
                if kind == "rx":
                    ok = p.fullmatch(q) is not None
                else:
                    ok = p.endswith(q) if i == 0 else p.startswith(q) if i == last else p == q
                    literal += ok
                if not ok:
                    break
            else:
                if literal >= 2:
                    return True
        return False

    def search(self, query, audience=None, top=10):
        """The top sections for a query, as dicts, and the spelling notes."""
        words, notes = self.correct(tokenize(query))
        scores = self.bm25(list(dict.fromkeys(words + command_grams(words))))
        phrases = []
        if len(query.split()) >= PHRASE_MIN_WORDS:
            phrases = list(dict.fromkeys([fold(query), " ".join(words)]))
        phrase_hits = {c for c in range(len(self.chunks)) for p in phrases if self.holds(c, p)}
        catalogue_first = self.names_id(words)
        ranked = []
        for c in set(scores) | phrase_hits:
            chunk = self.chunks[c]
            score = scores.get(c, 0.0) * (AUDIENCE_BOOST if audience and chunk["audience"] == audience else 1.0)
            phrase = c in phrase_hits
            catalogue_rank = 0 if chunk["catalogue"] == (phrase or catalogue_first) else 1
            ranked.append(((0 if phrase else 1, catalogue_rank, -score, chunk["order"][0], chunk["order"][1]),
                           c, score, phrase))
        ranked.sort()
        results, listed = [], set()
        for _, c, score, phrase in ranked:
            chunk = self.chunks[c]
            if (chunk["path"], chunk["anchor"]) in listed:
                continue  # a later chunk of a section already listed: one link per section
            listed.add((chunk["path"], chunk["anchor"]))
            results.append({"path": chunk["path"], "anchor": chunk["anchor"], "heading": chunk["heading"],
                            "score": score, "phrase": phrase, "first": chunk["first"]})
            if len(results) == top:
                break
        return results, notes


def load(index_path, chunks_path=None):
    """The index and its chunks; chunks.jsonl is looked for beside the index unless named."""
    index_path = Path(index_path)
    with gzip.open(index_path, "rt", encoding="utf-8") as handle:
        data = json.load(handle)
    with open(chunks_path or index_path.with_name("chunks.jsonl"), encoding="utf-8") as handle:
        return Index(data, [json.loads(line) for line in handle if line.strip()])


def usage_error(message):
    """The usage line and the problem on stderr, and exit status 2."""
    print(f"{USAGE}\nsearch.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_args(argv):
    """Options anywhere; every other word is the query, so a query may start with "--" (search.py --release)."""
    options = {"--audience": None, "--top": "10", "--index": str(Path(__file__).resolve().with_name("index.json.gz"))}
    words, i = [], 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            print(__doc__)
            raise SystemExit(0)
        if arg in options:
            if i + 1 >= len(argv):
                usage_error(f"{arg} needs a value")
            options[arg] = argv[i + 1]
            i += 2
            continue
        words.append(arg)
        i += 1
    if not words:
        usage_error("give the words to search for")
    if options["--audience"] is not None and options["--audience"] not in AUDIENCES:
        usage_error(f"--audience is one of {', '.join(AUDIENCES)}")
    if not options["--top"].isdigit() or int(options["--top"]) < 1:
        usage_error("--top is a whole number of 1 or more")
    return " ".join(words), options["--audience"], int(options["--top"]), Path(options["--index"])


def main(argv=None):
    query, audience, top, index_path = parse_args(sys.argv[1:] if argv is None else argv)
    for needed in (index_path, index_path.with_name("chunks.jsonl")):
        if not needed.is_file():
            print(f"search.py: no {needed}; build it with python3 .github/scripts/build_index.py", file=sys.stderr)
            return 2
    try:
        index = load(index_path)
    except (OSError, ValueError) as error:
        print(f"search.py: {error}; build it again with python3 .github/scripts/build_index.py", file=sys.stderr)
        return 2
    results, notes = index.search(query, audience, top)
    for note in notes:
        print(note)
    if not results:
        print("no results")
        return 1
    for n, result in enumerate(results, 1):
        where = result["path"] + ("#" + result["anchor"] if result["anchor"] else "")
        first = result["first"]
        if len(first) > FIRST_LINE_CHARS:
            first = first[:FIRST_LINE_CHARS - 3].rstrip() + "..."
        print(f"{n}. {where}  score {result['score']:.2f}{' (phrase)' if result['phrase'] else ''}")
        print(f"   {result['heading']}")
        if first:
            print(f"   {first}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
