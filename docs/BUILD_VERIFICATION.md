# Assembly verification

Prepared on 2026-10-29 for a 60-minute session. This records package assembly, not deployment on the user's Proxmox server.

## Closing slide update v1.0.1

- Added the public GitHub repository QR code and a visible explanation that the repository provides the notebooks, slides and full demo bundle.
- Retained the three existing training/contact codes. All four codes decoded correctly from both their PNG assets and the final closing slide.
- The 22-slide deck retains its layout and timing. Slides 1 through 21 match the previous public renders. The revised closing slide and self-contained HTML version were reviewed for layout and readable links.
- The updated public PowerPoint passed package, layout, font and first-party import checks. The release archive was rebuilt with the revised slides, notes and checksums. Demo code, corpus, rules and dependencies are unchanged from v1.0.0.

## Public copy v1.0.0 checked on 2026-10-30

- All 22 pytest tests passed with sockets disabled, using the public source and corpus.
- The complete public replay pipeline ran successfully with sockets blocked and produced the expected detection and Nova metrics.
- All 182 Linux amd64 CPython 3.12 wheels passed hash, pin, tag and dependency-closure verification.
- The public PPTX passed package, layout and font checks, and first-party re-import, with zero findings. Its 22 slide renders match the previously reviewed deck byte-for-byte. The change is limited to removing private commercial-pilot references from the notes.
- The public presenter guide and browser slides were rebuilt from the cleaned slide source. A local output path was removed from the executed instructor notebook.
- Public text and embedded presentation XML were reviewed for credentials and private project context before publication. Local deployment evidence and private business files are outside the public copy.

The checks below document initial assembly. Environment-specific runtime acceptance remains separate.

## Verified locally

- CPython 3.12 isolated environment with MSTICPy 3.0.2, Nova Hunting 0.3.1, pySigma 2.0.1, SQLite backend 2.1.1, and OpenAI SDK 2.54.0.
- `pip check`: no broken requirements.
- 22 pytest tests passed with Python network sockets disabled.
- Complete replay pipeline passed with network socket creation disabled.
- All 12 notebook code cells executed without an error output in the separate instructor backup.
- Corpus regenerated and SHA256 integrity checks passed.
- Jupyter authenticated `/api/status` returned 200 on localhost; unauthenticated `/lab` redirected to login. The finite probe shut down its own process afterwards.
- Both base and live Compose definitions passed configuration parsing.
- The 182-wheel Linux amd64 CPython 3.12 kit passed SHA256, pin, compatible-tag (glibc <= 2.36), and base dependency-closure checks. This is metadata/availability verification, not Linux runtime execution.
- Python source compiled and shell launchers passed syntax checks.
- The current 22-slide HI Cyber Con PPTX passed structural/layout validation and first-party re-import with no findings. All 22 slide renders were visually reviewed. Twenty-two speaker-note parts and nine native editable tables are present.

## Conference slide revision

- Restyled the deck in the conference's ivory, black and burnt-orange direction, using original conceptual cover art generated with the built-in image generation tool.
- Added a DEFCON-style introduction with the original portrait, high-level bio facts, and the three unmodified supplied logos.
- Added direct-link QR codes for TCM Security, IgniteCyber Academy and Carlo's LinkedIn profile. All three were decoded independently both from their PNG assets and from the rendered 1280 × 720 closing slide.
- Verified that all eight image assets are embedded in the PPTX, and that presenter checkpoint references match slides 11 through 17.
- Reviewed the self-contained HTML cover, introduction and QR closing in Chrome. Its images are embedded data URIs, so it has no network dependency for presentation.
- Kept the requested 60-minute timing, reallocating introduction and Q&A time for the two added slides. The public conference site advertises 45-minute sessions; confirm the assigned slot before delivery.
- Demo code, notebook, corpus and dependency locks are unchanged in this revision. The execution checks above record the initial assembly verification. No new live OpenAI, Linux, Docker or Proxmox runtime acceptance is claimed.

## Target checks still required

- Linux amd64 runtime acceptance using the bundled wheelhouse or a built container image.
- Docker image build and execution. The assembly workstation had no running Docker daemon.
- A real OpenAI call with the user's key and available model. Tests verify the request contract with mocks; the offline fixture is authored, not a recorded API response.
- Actual Proxmox guest provisioning/deployment, persistent service, SSH tunnel, offline rehearsal, backup and rollback.

See CLAUDE_DEPLOYMENT.md for the exact target acceptance sequence. Do not turn these pending checks into completed claims.
