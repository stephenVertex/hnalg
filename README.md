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

## Network troubleshooting

Searches require HTTPS access to `hn.algolia.com`. Temporary DNS failures are
retried twice with a short backoff. If a DNS error persists, check your network,
VPN, or DNS resolver; `nslookup hn.algolia.com` can help confirm whether the
hostname resolves. Other network failures are reported without DNS retries.
