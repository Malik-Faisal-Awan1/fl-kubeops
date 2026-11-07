# Only targets that really work are defined here. Add a target only when it works.
.PHONY: docs docs-check test-tools hooks

docs:
	python3 tools/docs.py --write

docs-check:
	python3 tools/docs.py --check

test-tools:
	python3 -m unittest discover -s tools -p "test_*.py" -v

hooks:
	git config core.hooksPath .githooks
	@echo "pre-commit hook enabled (runs tools/docs.py --write on every commit)"
