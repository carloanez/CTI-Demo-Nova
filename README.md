# CTI Demo Nova: From Threat Intelligence to Detection

## A Practical Notebook Workflow

Carlo Anez Mazurco · Cause-Finder / IgniteCyber Academy · 60 minutes

This is the complete local training package derived from the DEFCON34 MSTICPy demo. It contains an expanded synthetic case, real MSTICPy extraction, real Nova SDK scans, executable Sigma-to-SQLite tests, and bounded OpenAI API assistance. No local inference model is required or supported.

## Start here

- [PowerPoint slides](slides/Threat_Intelligence_to_Detection_HI_Cyber_Con_v2.pptx) and [self-contained offline browser deck](slides/Threat_Intelligence_to_Detection.html).
- Conference revision: 22 slides with matching cover art, Carlo's introduction, the three supplied logos, and direct-link QR codes for the GitHub demo, TCM Security, IgniteCyber Academy and LinkedIn.
- [Live notebook](notebooks/01_Threat_Intelligence_to_Detection.ipynb).
- [Presenter path and timing](docs/PRESENTER_GUIDE.md).
- [Proxmox deployment guide for Claude](docs/CLAUDE_DEPLOYMENT.md).
- [Test scope and expected outcomes](docs/TESTING.md).
- [Pre-executed replay notebook](instructor/executed_demo.ipynb).
- [Prepared synthetic output examples](outputs/).
- [Latest full offline kit and checksums](https://github.com/carloanez/CTI-Demo-Nova/releases/latest), including the Linux amd64 Python 3.12 wheels.

The requested 60-minute timing is retained. HI Cyber Con's public website advertises 45-minute sessions; confirm the assigned slot before presenting. Artwork provenance, the final generation prompt and QR destinations are documented in `slides/assets/ARTWORK_AND_SOURCES.md`.

![Conference-themed cover](slides/assets/hi-cyber-con-cover-art.png)

## Quick start from GitHub

Use CPython 3.12. These installation commands need internet. The tests and replay run without network access after dependencies are installed.

```bash
git clone https://github.com/carloanez/CTI-Demo-Nova.git
cd CTI-Demo-Nova
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
.venv/bin/python -m pip check
.venv/bin/python -m pytest
.venv/bin/python scripts/offline_run.py
```

The Git checkout includes source code, synthetic data, rules, notes, slides, tests and dependency manifests. Downloadable dependency wheels are distributed in the release archive rather than Git history. To build the offline wheelhouse yourself before a Docker build or disconnected deployment:

```bash
.venv/bin/python scripts/prepare_linux_wheels.py --download
.venv/bin/python scripts/verify_wheelhouse.py
```

The target is Linux amd64 with CPython 3.12. A fully disconnected deployment must stage its operating system, Python runtime and any Docker base/application images in advance. See the deployment guide and [public release notes](docs/PUBLIC_RELEASE.md).

## Online AI and offline execution

`openai` mode calls the hosted OpenAI Responses API. It needs internet, a valid API key, and access to the configured model. `replay` mode reads a clearly labeled **instructor-authored fixture**, not an actual recorded OpenAI response. Neither mode runs a local model. Live failures never silently switch to replay.

All extraction, enrichment, telemetry pivots, Sigma tests, Nova keyword scans, and report exports run offline after dependencies are installed. The release archive's wheelhouse targets **Linux amd64, CPython 3.12**. A disconnected machine still needs an OS, Python with venv/pip, and optionally Docker plus a staged base or application image. We do not claim to bootstrap an empty machine without those prerequisites.

## Native installation on Linux amd64

Run inside the extracted `cti-notebook-workflow` folder on an Ubuntu 24.04 guest with Python 3.12 and venv installed:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --no-index --find-links=wheelhouse -r requirements-linux-amd64.lock
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_wheelhouse.py
.venv/bin/python -m cti_lab.cli verify-corpus
.venv/bin/python -m pytest
.venv/bin/python scripts/offline_run.py
```

macOS/Windows users should install `requirements.lock` while connected instead of using the Linux wheelhouse. CPython 3.12 is the tested interpreter family. The shell launchers target Linux/macOS; on Windows use the equivalent `.venv\Scripts\python.exe` commands.

## Open the notebook

```bash
cp .env.example .env
.venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Put the generated value into `JUPYTER_TOKEN` in `.env`. Leave `AI_MODE=replay` for a disconnected rehearsal. Then:

```bash
chmod 600 .env
bash scripts/start_native.sh
```

Open `http://127.0.0.1:8888/lab` and enter the token. Use **Restart Kernel and Run All**. No source event command is executed by this workflow. The instructor fixture and ground truth are available to the notebook user, but only `data/sources.json` is eligible for AI retrieval.

## Live OpenAI mode

Set `AI_MODE=openai` and `OPENAI_MODEL` in `.env`. The default configurable model is `gpt-4.1-mini`; availability is checked at deployment, not assumed. Configure the API key using a shell environment variable or `OPENAI_API_KEY_FILE` pointing to a protected file outside the served notebook directory. Do not paste a key into the notebook or slides. The Docker live override uses `secrets/openai_api_key` as a mounted file. Anyone who can execute code in that instructor kernel can access its configured secret, so do not share the instructor kernel with attendees.

```bash
.venv/bin/python -m cti_lab.cli ai --mode openai
```

The request uses Structured Outputs, `store=False`, a bounded input and output budget, no model tools, and local source/quote checks. `store=False` does not by itself guarantee zero retention or change all account data policies. A quote can validate while the interpretation is wrong; human review is required. See `docs/OPENAI.md` for capture and verification.

## Docker

Build once on a connected or properly staged Linux amd64 host:

```bash
docker compose build
docker compose up -d --no-build
docker compose exec lab python -m pytest
docker compose exec lab python scripts/offline_run.py
```

The base profile uses an internal network, replay mode, a non-root user, and a loopback-only published port. Access a remote guest through an SSH tunnel. Live mode is explicit:

```bash
docker compose -f compose.yml -f compose.openai.yml up -d --no-build
```

Prepare the key file before enabling that override. Preserve the named notebook/output volumes when restarting. The image build and Docker networking must be acceptance-tested on the deployment guest; the build workstation did not have a running Docker daemon.

## Corpus and outputs

The deterministic seed is 340629. There are eight documents, 24 source passages, 3,000 enterprise events, 25 enrichment records, and 120 Nova cases. Documentation IP ranges and reserved `.invalid`/`.example` names replace the original demo's ordinary-looking domains. All rules in this bundle are original teaching rules, not a redistributed official Nova rule pack.

`scripts/build_corpus.py` regenerates canonical data and the unexecuted notebook. This overwrites those generated artifacts, so preserve any adaptations first. `scripts/execute_notebook.py` always uses replay and writes a separate instructor copy. `scripts/offline_run.py` recomputes exports with Python network sockets blocked. Do not regenerate the corpus immediately before a talk if you have modified the lesson.

## Limits and scope

- Fixture metrics are not production accuracy estimates or vendor benchmarks.
- Keyword rules deliberately miss a held-out paraphrase family.
- The quotation policy trusts application context and is not an automatic semantic classifier.
- ATT&CK mappings are a small reviewed set, not a complete heat map or full catalog snapshot.
- Proximity and Tracer are optional extensions; commercial NovaHunting is not included or required.
- Ground truth and instructor files should be withheld from students when used as an assessment. This is a single-instructor demo service, not a multi-user learning platform.

Third-party packages retain their own licenses. Wheel files include their package metadata and license material where provided. See `references/PRIMARY_SOURCES.md`.
