.PHONY: test test-fast test-meta test-cli-smoke test-full

test: test-fast

test-fast:
	uv run pytest -q -m "not meta"

test-meta:
	uv run pytest -q -m meta

test-cli-smoke:
	uv run pytest tests/test_cli_validate_workspace.py tests/test_local_runtime.py tests/test_hermes_runtime.py tests/test_product_entry.py -q

test-full:
	uv run pytest -q
