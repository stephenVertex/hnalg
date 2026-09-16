"""Static agent-facing usage guide for :mod:`hnalg`."""

PRIME_GUIDE = """# hnalg
Search Hacker News stories and comments through the Algolia API.

Usage:
  hnalg prime
  hnalg QUERY [OPTIONS]

Options:
  -n, --limit N   Maximum results (default: 20).
  --author USER   Restrict results to one HN user.
  --story         Search only stories.
  --comment       Search only comments.
  --ask-hn        Search only Ask HN posts.
  --show-hn       Search only Show HN posts.
  --json          Print the raw Algolia JSON response.
  -h, --help      Show CLI help.

Conventions and gotchas:
  - Search requires a non-empty QUERY; quote multi-word queries.
  - Filters may be combined and narrow the result set.
  - Default output is human-readable. Comment HTML is stripped and text over
    280 characters is truncated; use --json when the raw response is needed.
  - Searches contact hn.algolia.com. The prime guide and help are local and do
    not require network access.
  - --comment searches all indexed HN comments. Before quoting, verify the
    exact text and its specific HN thread; missing text can reflect flagged or
    removed items or API omissions.
"""


def get_prime_guide() -> str:
    """Return hnalg's deterministic, newline-terminated prime guide."""
    return PRIME_GUIDE
