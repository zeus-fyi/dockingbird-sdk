#!/usr/bin/env python3
"""Run the docs' regression queries and fail when a query's expected page leaves the top 3.

    python3 .github/scripts/check_queries.py [--allow-missing]

Reads search/queries.txt: one query per line, a tab, then the page the query must find. A page is a path from the
repository root, such as docs/guides/licensing.md, or a path and an anchor, such as
docs/troubleshooting.md#license_seats_full, for one section. Pages joined by "|" pass when any one of them is in the
top 3. Blank lines and lines that start with "#" are skipped. Each query runs through search.py, beside this file,
on search/index.json.gz and search/chunks.jsonl, and prints one line: pass, FAIL or pending. A query is pending when
none of its pages is in the top 3 and one of them is not in the index yet. It exits 1 when a query fails, or is
pending without --allow-missing, and 2 when queries.txt or the index cannot be read. Standard library only.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUERIES = ROOT / "search" / "queries.txt"
INDEX = ROOT / "search" / "index.json.gz"
TOP = 3
SHOWN = 10

_spec = importlib.util.spec_from_file_location("docs_search", Path(__file__).with_name("search.py"))
search = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(search)


def read_queries(path):
    """(query, expected pages) per query line; ValueError naming the first line that is not query<TAB>pages."""
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        pages = [page.strip() for page in parts[-1].split("|") if page.strip()]
        if len(parts) != 2 or not parts[0].strip() or not pages:
            raise ValueError(f"{path.name} line {n} is not a query, a tab and a page: {line!r}")
        out.append((parts[0].strip(), pages))
    return out


def where(result):
    return result["path"] + ("#" + result["anchor"] if result["anchor"] else "")


def matches(result, page):
    path, _, anchor = page.partition("#")
    return result["path"] == path and (not anchor or result["anchor"] == anchor)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fail when a query's expected page leaves the top 3.")
    parser.add_argument("--allow-missing", action="store_true",
                        help="report a query whose page is not in the index yet as pending, and do not fail on it")
    args = parser.parse_args(argv)
    try:
        queries = read_queries(QUERIES)
        index = search.load(INDEX)
    except (OSError, ValueError) as error:
        print(f"check_queries.py: {error}; build the index with python3 .github/scripts/build_index.py",
              file=sys.stderr)
        return 2
    sections, paths = index.pages()
    counts = {"pass": 0, "FAIL": 0, "pending": 0}
    for query, pages in queries:
        results, _ = index.search(query, top=SHOWN)
        rank = next((n for n, result in enumerate(results, 1) if any(matches(result, p) for p in pages)), None)
        missing = [p for p in pages if (tuple(p.split("#", 1)) not in sections if "#" in p else p not in paths)]
        if rank is not None and rank <= TOP:
            status, detail = "pass", f"rank {rank}"
        elif missing:
            status, detail = "pending", "not in the index yet: " + ", ".join(missing)
        else:
            status = "FAIL"
            detail = (f"rank {rank}" if rank else f"not in the top {SHOWN}") + "; the top 3: " + ", ".join(
                where(result) for result in results[:TOP])
        counts[status] += 1
        print(f"{status:<7} {query} -> {' | '.join(pages)} ({detail})")
    print(f"queries={len(queries)} pass={counts['pass']} fail={counts['FAIL']} pending={counts['pending']}")
    return 1 if counts["FAIL"] or (counts["pending"] and not args.allow_missing) else 0


if __name__ == "__main__":
    sys.exit(main())
