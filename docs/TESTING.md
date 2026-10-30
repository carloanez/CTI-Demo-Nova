# Test scope and expected outcomes

## Commands

```bash
python -m pytest
python scripts/offline_run.py
python scripts/execute_notebook.py
python -m cti_lab.cli verify-corpus
```

The pytest configuration enables `pytest-socket --disable-socket`. A test explicitly confirms that socket creation fails. `offline_run.py` applies that same restriction to the complete replay pipeline. The notebook execution command needs local Jupyter kernel communication and therefore is separate from the socket-blocked test process.

## Coverage

- Corpus sizes, stable unique event IDs, SHA256 hashes and syntactically valid notebook cells.
- Actual MSTICPy DataFrame extraction of defanged indicators with source preservation.
- Field-aware correlation with negative controls for IP-prefix and domain-substring collisions.
- Actual Sigma parsing, SQLite conversion, and SQL execution, including exact expected event IDs.
- A mutated Sigma rule must change query results, demonstrating that tests use the YAML artifact.
- Approved-change tuning and the rotated-domain blind spot.
- Actual Nova SDK matching and the separately evaluated application policy.
- Isolation of complete template families between development and held-out Nova cases.
- Withholding the poisoned passages from retrieval and excluding instructor labels.
- Replay provenance, Pydantic schema, unknown-citation and fabricated-quote rejection.
- Mocked OpenAI request parameters, incomplete/refusal behavior, timeouts, and missing-key failure.

## Fixture results

| Rule | TP | FP | FN | Interpretation |
|---|---:|---:|---:|---|
| Infrastructure | 5 | 0 | 5 | Changed destination evades the known-domain rule |
| PowerShell broad | 7 | 2 | 0 | Approved maintenance is a false positive |
| PowerShell tuned | 7 | 0 | 0 | Narrow change join suppresses those two events |
| Log-clear invocation | 2 | 0 | 0 | Matches command invocation, not success |

The Nova development split has 70 cases: 30 attacks, 20 ordinary cases, and 20 security quotations. Raw pattern matching yields TP 30 / FP 20 / FN 0. The application policy yields TP 30 / FP 0 / FN 0 using the exercise's trusted quotation metadata.

The held-out split has 50 cases: 10 attacks in a distinct paraphrase family, 20 ordinary cases, and 20 quotations. The keyword rules miss all ten attacks. This deliberate gap must remain visible. The application policy is not a semantic injection classifier and the context metadata must not be attacker-controlled.

These results describe this authored corpus only. Do not present them as Nova efficacy measurements, public NovaHunting benchmarks, or expected production precision/recall.

## Deployment acceptance

Run the same suite on Linux amd64 after installation, execute every notebook cell in replay, verify the local Jupyter login, then perform one real OpenAI smoke call only after configuring the user's key. Record container image ID/digest, OS, architecture, Python/library versions and test outputs. Docker image execution and the real API call require target acceptance; unit mocks cannot establish either.
