---
name: security-review
description: Review code changes for security vulnerabilities. Use when the user asks to check security, review for vulnerabilities, run a security scan, or audit code safety.
---

## Steps

1. Read the current diff or staged changes
2. Analyze the code for common security issues:
   - Command injection (unsanitized input in shell commands)
   - Hardcoded secrets (API keys, passwords, tokens in source code)
   - SQL injection (string concatenation in queries)
   - Path traversal (unsanitized user input in file paths)
   - Unsafe deserialization (pickle, yaml.load without SafeLoader)
3. For each issue found, report:
   - File and line number
   - Severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Description of the vulnerability
   - Suggested fix
4. If no issues are found, report a clean result
5. Output results as structured JSON with an `issues` array
