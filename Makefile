.PHONY: test replay corpus notebook check start live
PYTHON ?= python
test:
	$(PYTHON) -m pytest
replay:
	$(PYTHON) scripts/offline_run.py
corpus:
	$(PYTHON) scripts/build_corpus.py
notebook:
	$(PYTHON) scripts/execute_notebook.py
check:
	$(PYTHON) -m cti_lab.cli verify-corpus
	$(PYTHON) -m cti_lab.cli check
start:
	docker compose up -d --no-build
live:
	docker compose -f compose.yml -f compose.openai.yml up -d --no-build
