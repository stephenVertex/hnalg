# hnalg

HackerNews Algolia search CLI.

## Usage

Before using hnalg in a session, agents should run `hnalg prime`; they should
run it again after context compaction. It prints a compact, local guide to
hnalg's command surface and key conventions; it does not run a search or
contact Algolia.

```bash
hnalg prime
hnalg "rust async"
hnalg python --limit 5
hnalg "linux kernel" --story
hnalg "hiring" --author patio11
hnalg "show hn" --show-hn
```
