---
name: style-check
description: Check code follows project naming conventions and style rules. Use when the user asks to check style, review naming conventions, or verify code formatting.
---

## Steps

1. Read the current diff or staged changes
2. Check for naming convention violations:
   - Functions and variables should use snake_case (Python) or camelCase (JavaScript)
   - Classes should use PascalCase
   - Constants should use UPPER_SNAKE_CASE
3. Check for style issues:
   - Line length should not exceed 120 characters
   - Import ordering (stdlib, third-party, local)
   - Consistent use of quotes (single or double, per project convention)
4. Report any violations with file, line number, and suggested fix
