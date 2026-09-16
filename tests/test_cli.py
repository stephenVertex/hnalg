import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from hnalg import main
from hnalg.prime import get_prime_guide


class CliDispatchTests(unittest.TestCase):
    def test_help_discovers_prime_and_preserves_search_options(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch("hnalg.search") as search,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
            self.assertRaises(SystemExit) as stopped,
        ):
            main(["--help"])

        self.assertEqual(stopped.exception.code, 0)
        self.assertIn("hnalg prime", stdout.getvalue())
        self.assertIn("--limit", stdout.getvalue())
        self.assertIn("query", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")
        search.assert_not_called()

    def test_prime_prints_guide_and_exits_successfully_without_searching(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch("hnalg.search") as search,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            exit_code = main(["prime"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), get_prime_guide())
        self.assertEqual(stderr.getvalue(), "")
        search.assert_not_called()

    def test_non_prime_query_still_uses_search_path(self) -> None:
        stdout = io.StringIO()

        with (
            patch("hnalg.search", return_value={"hits": []}) as search,
            redirect_stdout(stdout),
        ):
            exit_code = main(["prime numbers", "--limit", "3"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "no results found\n")
        search.assert_called_once_with("prime numbers", tags=None, hits_per_page=3)


if __name__ == "__main__":
    unittest.main()
