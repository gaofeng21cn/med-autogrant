PYTHON_CLEAN := ./scripts/run-python-clean.sh
PYTEST_CLEAN := ./scripts/run-pytest-clean.sh

.PHONY: test test-fast test-line-budget test-line-budget-strict test-descriptor-contracts test-family test-meta test-cli-smoke test-smoke test-regression test-structure test-structure-strict test-full

test: test-fast

test-fast:
	$(MAKE) test-line-budget
	$(MAKE) test-cli-smoke
	$(PYTEST_CLEAN) -q -m "not meta and not regression"

test-line-budget:
	$(PYTHON_CLEAN) scripts/line_budget.py

test-line-budget-strict:
	$(MAKE) test-line-budget

test-descriptor-contracts:
	$(PYTHON_CLEAN) scripts/check_descriptor_contracts.py

test-family:
	$(MAKE) test-line-budget
	$(PYTEST_CLEAN) tests/test_repository_hygiene.py tests/test_test_command_surfaces.py tests/test_domain_entry.py -q

test-meta:
	./scripts/repo-hygiene.sh --fix
	./scripts/repo-hygiene.sh
	$(MAKE) test-descriptor-contracts
	$(PYTEST_CLEAN) -q -m meta

test-cli-smoke:
	$(PYTEST_CLEAN) -q -m smoke

test-smoke:
	$(MAKE) test-line-budget
	$(MAKE) test-cli-smoke

test-regression:
	$(PYTEST_CLEAN) -q -m regression

test-structure:
	$(MAKE) test-line-budget
	$(MAKE) test-descriptor-contracts

test-structure-strict:
	$(MAKE) test-line-budget-strict
	$(MAKE) test-descriptor-contracts

test-full:
	$(PYTEST_CLEAN) -q
