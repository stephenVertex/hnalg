#!/usr/bin/env python3
"""hnalg - HackerNews Algolia search CLI."""

import argparse
import html
import json
import re
import sys
import urllib.request
from urllib.parse import urlencode

API_URL = "https://hn.algolia.com/api/v1/search"


def search(query: str, tags: str | None = None, hits_per_page: int = 20) -> dict:
    """Search HN via Algolia."""
    params = {"query": query, "hitsPerPage": hits_per_page}
    if tags:
        params["tags"] = tags
    url = f"{API_URL}?{urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "hnalg/0.1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _strip_html(text: str) -> str:
    """Remove HTML tags and unescape entities."""
    plain = re.sub(r"<[^>]+>", "", text)
    return html.unescape(plain)


def _is_comment(hit: dict) -> bool:
    return "comment" in hit.get("_tags", [])


def format_hit(hit: dict) -> str:
    """Pretty-print a single search hit."""
    is_comment = _is_comment(hit)
    title = hit.get("title") or hit.get("story_title") or "(untitled)"
    url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
    author = hit.get("author", "unknown")
    points = hit.get("points", 0)
    comments = hit.get("num_comments", 0)
    created = hit.get("created_at", "")

    if is_comment:
        raw = hit.get("comment_text", "")
        text = _strip_html(raw)
        # Truncate long comments
        if len(text) > 280:
            text = text[:277] + "..."
        parent = hit.get("story_title", "(untitled)")
        return (
            f"💬 Comment on: {parent}\n"
            f"  {text}\n"
            f"  {url}\n"
            f"  by {author} | {created}\n"
        )

    return f"{title}\n  {url}\n  {points} points | {comments} comments | by {author} | {created}\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="hnalg",
        description="Search Hacker News via the Algolia API",
    )
    parser.add_argument("query", nargs="?", default="", help="search query")
    parser.add_argument(
        "-n", "--limit", type=int, default=20, help="max results (default: 20)"
    )
    parser.add_argument(
        "--author", metavar="USER", help="filter by author"
    )
    parser.add_argument(
        "--story", action="store_true", help="search only stories"
    )
    parser.add_argument(
        "--comment", action="store_true", help="search only comments"
    )
    parser.add_argument(
        "--ask-hn", action="store_true", help="search Ask HN posts"
    )
    parser.add_argument(
        "--show-hn", action="store_true", help="search Show HN posts"
    )
    parser.add_argument(
        "--json", action="store_true", help="output raw JSON"
    )
    args = parser.parse_args()

    if not args.query:
        parser.error("a query is required")

    tags = []
    if args.story:
        tags.append("story")
    if args.comment:
        tags.append("comment")
    if args.ask_hn:
        tags.append("ask_hn")
    if args.show_hn:
        tags.append("show_hn")
    if args.author:
        tags.append(f"author_{args.author}")

    tags_str = ",".join(tags) if tags else None

    try:
        data = search(args.query, tags=tags_str, hits_per_page=args.limit)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    hits = data.get("hits", [])
    if not hits:
        print("no results found")
        return 0

    print(f"{data.get('nbHits', 0)} total | showing {len(hits)} result(s)\n")
    for hit in hits:
        print(format_hit(hit))

    return 0


if __name__ == "__main__":
    sys.exit(main())
