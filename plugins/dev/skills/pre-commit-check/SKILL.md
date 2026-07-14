---
name: pre-commit-check
description: Run project checks before committing. Use when the user asks to commit changes or prepare a commit.
---

## Steps

1. Run linting: `ruff check --fix . && ruff format .`
2. Run the test suite: `pytest`
3. If either step fails, show the errors and stop — do not commit
4. Stage the changes and create the commit following conventional commits format
