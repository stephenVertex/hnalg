import unittest

from hnalg.prime import get_prime_guide


EXPECTED_PRIME_GUIDE = """# hnalg
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


class PrimeGuideTests(unittest.TestCase):
    def test_guide_matches_snapshot(self) -> None:
        self.assertEqual(get_prime_guide(), EXPECTED_PRIME_GUIDE)

    def test_guide_is_stable_plain_text_with_one_trailing_newline(self) -> None:
        guide = get_prime_guide()

        self.assertEqual(guide, get_prime_guide())
        self.assertTrue(guide.isascii())
        self.assertTrue(guide.endswith("\n"))
        self.assertFalse(guide.endswith("\n\n"))
        self.assertNotIn("\x1b", guide)

    def test_guide_covers_both_forms_and_every_cli_option(self) -> None:
        guide = get_prime_guide()
        required_surface = (
            "hnalg prime",
            "hnalg QUERY [OPTIONS]",
            "-n, --limit",
            "--author",
            "--story",
            "--comment",
            "--ask-hn",
            "--show-hn",
            "--json",
            "-h, --help",
        )

        for command_or_option in required_surface:
            with self.subTest(command_or_option=command_or_option):
                self.assertIn(command_or_option, guide)

    def test_guide_covers_required_conventions_and_gotchas(self) -> None:
        guide = " ".join(get_prime_guide().split())
        required_topics = (
            "requires a non-empty QUERY",
            "default: 20",
            "Filters may be combined",
            "Default output is human-readable",
            "raw Algolia JSON response",
            "hn.algolia.com",
            "do not require network access",
            "searches all indexed HN comments",
            "verify the exact text and its specific HN thread",
        )

        for topic in required_topics:
            with self.subTest(topic=topic):
                self.assertIn(topic, guide)


if __name__ == "__main__":
    unittest.main()
