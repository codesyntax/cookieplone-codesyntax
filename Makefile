# Makefile for cookieplone-codesyntax tests

.PHONY: test test-local

# Run tests using uv
test:
	@echo "Running tests using uv..."
	@uv run pytest tests/test_template.py

# Run tests pointing to a local upstream checkout (if available)
test-local:
	@echo "Running tests with local upstream checkout..."
	@uv run pytest --cookieplone-upstream-dir=../cookieplone-templates tests/test_template.py
