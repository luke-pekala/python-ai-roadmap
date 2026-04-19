"""
Smart Summariser CLI — Module M
Usage:
    python summariser.py --file myfile.txt
    python summariser.py --url https://example.com/article
    python summariser.py --text "Paste text here"
    python summariser.py --file myfile.txt --format json
    python summariser.py --file myfile.txt --stream
"""
import argparse
import json
import sys
import httpx
from client import summarise


def fetch_url(url: str) -> str:
    """Download page text from a URL (plain text extraction)."""
    resp = httpx.get(url, follow_redirects=True, timeout=15)
    resp.raise_for_status()
    # Strip HTML tags roughly — good enough for demo purposes
    import re
    text = re.sub(r"<[^>]+>", " ", resp.text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:12000]  # cap at ~12k chars


def render(result: dict, fmt: str) -> None:
    """Print the summary in the requested format."""
    if fmt == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if fmt == "markdown":
        print(f"## Summary\n{result['summary']}\n")
        if result["key_points"]:
            print("## Key Points")
            for kp in result["key_points"]:
                print(f"- {kp}")
            print()
        if result["action_items"]:
            print("## Action Items")
            for ai in result["action_items"]:
                print(f"- [ ] {ai}")
            print()
        print(f"**TL;DR:** {result['tldr']}")
        return

    # plain (default)
    print("\nSUMMARY")
    print("=" * 60)
    print(result["summary"])
    if result["key_points"]:
        print("\nKEY POINTS")
        print("-" * 40)
        for kp in result["key_points"]:
            print(f"  • {kp}")
    if result["action_items"]:
        print("\nACTION ITEMS")
        print("-" * 40)
        for ai in result["action_items"]:
            print(f"  ☐ {ai}")
    print("\nTL;DR")
    print("-" * 40)
    print(f"  {result['tldr']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smart Summariser — powered by Claude"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", metavar="PATH", help="Path to a text file")
    source.add_argument("--url", metavar="URL", help="URL to summarise")
    source.add_argument("--text", metavar="TEXT", help="Raw text to summarise")

    parser.add_argument(
        "--format",
        choices=["plain", "markdown", "json"],
        default="plain",
        help="Output format (default: plain)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream the response token-by-token",
    )
    args = parser.parse_args()

    # ── Load source text ──────────────────────────────────────────────────
    if args.file:
        text = open(args.file, encoding="utf-8").read()
    elif args.url:
        print(f"Fetching {args.url} ...")
        text = fetch_url(args.url)
    else:
        text = args.text

    if not text.strip():
        sys.exit("Error: empty input.")

    # ── Call Claude ───────────────────────────────────────────────────────
    result = summarise(text, stream=args.stream)
    if result is not None:
        render(result, args.format)


if __name__ == "__main__":
    main()
