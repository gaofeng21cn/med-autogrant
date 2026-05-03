.PHONY: test test-fast test-line-budget test-family test-meta test-cli-smoke test-structure test-full

test: test-fast

test-fast:
	uv run pytest -q -m "not meta"

test-line-budget:
	uv run python scripts/line_budget.py

test-family:
	uv run pytest tests/test_repository_hygiene.py tests/test_test_command_surfaces.py tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q

test-meta:
	uv run pytest -q -m meta

test-cli-smoke:
	uv run pytest tests/test_cli_validate_workspace.py tests/test_local_runtime.py tests/test_hermes_runtime.py tests/test_product_entry.py -q

test-structure:
	make test-line-budget
	./scripts/run-structural-quality-gate.sh

test-full:
	uv run pytest -q
