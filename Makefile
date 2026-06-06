PYTHON_CLEAN := ./scripts/run-python-clean.sh
PYTEST_CLEAN := ./scripts/run-pytest-clean.sh

.PHONY: test test-fast test-line-budget test-line-budget-strict test-generated-aggregate-sources test-family test-meta test-cli-smoke test-regression test-proof test-structure test-structure-strict test-full

test: test-fast

test-fast:
	$(MAKE) test-line-budget
	$(MAKE) test-cli-smoke
	$(PYTEST_CLEAN) -q -m "not meta and not regression and not proof"

test-line-budget:
	$(PYTHON_CLEAN) scripts/line_budget.py

test-line-budget-strict:
	$(PYTHON_CLEAN) scripts/line_budget.py --strict

test-generated-aggregate-sources:
	$(PYTHON_CLEAN) scripts/check_generated_aggregate_sources.py

test-family:
	$(PYTEST_CLEAN) tests/test_repository_hygiene.py tests/test_test_command_surfaces.py tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q -m "not proof"

test-meta:
	./scripts/repo-hygiene.sh --fix
	./scripts/repo-hygiene.sh
	$(MAKE) test-generated-aggregate-sources
	$(PYTEST_CLEAN) -q -m meta

test-cli-smoke:
	$(PYTEST_CLEAN) -q -m smoke

test-regression:
	$(PYTEST_CLEAN) -q -m "regression and not proof"

test-proof:
	MAG_CLEAN_RUNNER_UV_EXTRA=proof $(PYTEST_CLEAN) -q -m proof

test-structure:
	make test-line-budget
	./scripts/run-structural-quality-gate.sh --advisory

test-structure-strict:
	make test-line-budget-strict
	./scripts/run-structural-quality-gate.sh --strict

test-full:
	$(PYTEST_CLEAN) -q -m "not proof"
	$(MAKE) test-proof
