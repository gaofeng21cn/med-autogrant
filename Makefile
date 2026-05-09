.PHONY: test test-fast test-line-budget test-family test-meta test-cli-smoke test-regression test-proof test-structure test-full

test: test-fast

test-fast:
	$(MAKE) test-line-budget
	$(MAKE) test-cli-smoke
	uv run pytest -q -m "not meta and not regression and not proof"

test-line-budget:
	uv run python scripts/line_budget.py

test-family:
	uv run pytest tests/test_repository_hygiene.py tests/test_test_command_surfaces.py tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q

test-meta:
	uv run pytest -q -m meta

test-cli-smoke:
	uv run pytest -q -m smoke

test-regression:
	uv run pytest -q -m "regression and not proof"

test-proof:
	uv run --extra proof pytest -q -m proof

test-structure:
	make test-line-budget
	./scripts/run-structural-quality-gate.sh

test-full:
	uv run pytest -q -m "not proof"
	$(MAKE) test-proof
