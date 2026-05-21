# Makefile for cookieplone-codesyntax tests

.PHONY: test test-local

# Run tests using the cookieplone environment (requires cookieplone to be in ~/dev/cookieplone)
test:
	@echo "Running tests using cookieplone venv..."
	@/home/erral/dev/cookieplone/.venv/bin/pytest tests/test_template.py

# Run tests pointing to a local upstream checkout to save time/bandwidth
test-local:
	@echo "Running tests with local upstream checkout..."
	@/home/erral/dev/cookieplone/.venv/bin/pytest --cookieplone-upstream-dir=/home/erral/dev/cookieplone-templates tests/test_template.py
