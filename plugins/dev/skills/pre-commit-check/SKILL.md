---
name: pre-commit-check
description: Run project checks before committing. Use when the user asks to commit changes, prepare a commit, or push code.
---

## Steps

1. Run linting: `npm run lint:fix`
2. Run the test suite: `npm test`
3. If either step fails, show the errors and stop — do not commit
4. Stage the changes and create the commit following conventional commits format
