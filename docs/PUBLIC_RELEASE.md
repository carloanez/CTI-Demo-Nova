# Public release v1.0.0

Prepared on 2026-10-30 for https://github.com/carloanez/CTI-Demo-Nova.

## Included

- Runnable Jupyter workflow and Python source with MSTICPy extraction, Sigma-to-SQLite detection tests, Nova SDK scans and optional OpenAI API drafting.
- Eight fictional reports, 3,000 synthetic enterprise events, enrichment records and a 120-case Nova teaching set.
- Original teaching rules, clearly labeled replay fixtures, expected results and an executed instructor notebook. Instructor files contain spoilers and should be withheld when adapting the material into an assessment.
- The current 22-slide conference deck, self-contained browser slides, presenter notes, original cover artwork, supplied logos and direct-link QR codes.
- Test suite, dependency locks, wheel hash manifest, Docker definitions and a generic Proxmox deployment handoff.

## Distribution

The Git repository contains the main teaching materials. The release asset `CTI_Demo_Nova_v1.0.0_offline.tar.gz` adds the 182 Linux amd64 / CPython 3.12 dependency wheels. Extract it into a fresh directory and follow README.md. Verify the adjacent `SHA256SUMS` before extracting. The archive has a single `cti-notebook-workflow/` top-level directory.

Local credentials, deployment inventories and evidence, backups, recordings, private business notes, obsolete decks, virtual environments and caches are excluded. Private commercial-pilot references were removed from the public presenter materials, and the executed notebook's local machine path was replaced with `<LOCAL_PROJECT>`.

The corpus and rules are synthetic teaching materials. Metrics describe only the authored fixtures. Commercial NovaHunting access and proprietary rule packs are outside this release. Third-party software retains its own license, and company logos remain the property of their respective owners. See [primary references](../references/PRIMARY_SOURCES.md) and [artwork sources](../slides/assets/ARTWORK_AND_SOURCES.md).

## Validation

The public copy is checked for corpus integrity, the network-disabled test suite, offline replay, pinned wheel hashes and dependency closure, embedded presentation assets and scannable QR payloads. See BUILD_VERIFICATION.md for the recorded checks and runtime acceptance that remains environment-specific.

Public-release preparation does not establish a new Linux, Docker, live OpenAI API or Proxmox acceptance result. The generic guide specifies those checks for the deployment target.
