# OpenAI API integration

The only live inference provider is OpenAI. There is no Ollama, local model, or alternative-provider route.

## Configuration

Use CPython 3.12 and the locked OpenAI SDK. Set `AI_MODE=openai` and `OPENAI_MODEL=gpt-4.1-mini` or another model available to the user's project that supports Responses Structured Outputs. The exact model is configurable so the deployment does not assume account entitlement.

Supply `OPENAI_API_KEY` through the process environment or `OPENAI_API_KEY_FILE` through a file accessible to the instructor process. Keys must not appear in `.ipynb`, slides, fixture files, outputs, logs, or an archive. Do not print the environment when troubleshooting. For Docker, mount `secrets/openai_api_key` using `compose.openai.yml`; use mode 0600 and the owner needed for UID 1000.

## Request contract

1. Retrieve from the 24 public synthetic passages only. Ground-truth labels never enter retrieval.
2. Scan every candidate passage with the actual Nova SDK. Withhold matching chunks and preserve their source files.
3. Send at most 12 selected passages to `client.responses.create` with explicit instructions treating passages as data.
4. Request a strict JSON Schema with fields for summary, findings, intelligence gaps, and detection hypotheses. No tools are supplied.
5. Use `store=False`, `max_output_tokens=1800`, a 40-second client timeout, and at most one SDK retry. A retry can add latency or billable work.
6. Reject incomplete or empty responses. Parse locally through Pydantic and reject unknown source IDs or quotes not present in their cited source.
7. Keep provenance: mode, model, response ID, usage, capture time, and context hash. Never claim that structural or citation validation proves factual correctness.

The API is not given endpoint telemetry directly in this version. It summarizes the selected report and analyst-note passages. The deterministic analyst brief links to separate event, mapping, and detection outputs. A future extension can supply bounded event extracts with the same citation validation scheme.

## Live acceptance check

On the deployed guest, after the key is configured:

```bash
docker compose -f compose.yml -f compose.openai.yml exec lab python -m cti_lab.cli ai --mode openai
```

Check that `outputs/ai_draft.json` says `LIVE OPENAI RESPONSES API`, contains a real response ID and usage, and passed source/quote validation. Review all findings manually. A mocked test response ID is not evidence of a live call.

To keep a rehearsal record, copy this output to an instructor-only file named `live_rehearsal.json`. The packaging script excludes `live_*` files. The included replay fixture is authored and remains labeled as such even after a live call. Do not relabel it as recorded AI output. Live cache replay is not implemented in v1.

## Offline rehearsal

Use `AI_MODE=replay` or `--mode replay`. The notebook displays `INSTRUCTOR-AUTHORED FIXTURE, NOT AN OPENAI RESPONSE`. Disconnect outbound networking and run all notebook cells. The independent test suite blocks Python sockets and verifies the API request contract through a mock.

## Error handling

- Missing key: select replay explicitly or configure the secret.
- Authentication/model access error: verify project key and configured model in the user's account. Do not expose the key.
- Rate limit or timeout: retain the error, use the replay path on stage, and retry the live check later with consent to its cost.
- Refusal/incomplete response: do not parse partial JSON as a completed finding.
- Invalid citation: preserve the failed draft for private review if appropriate and reject it from the final brief.

Primary documentation, reviewed 2026-10-29:

- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/docs/guides/migrate-to-responses
