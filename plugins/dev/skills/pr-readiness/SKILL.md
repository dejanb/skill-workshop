---
name: pr-readiness
description: Check if the current branch is ready for a pull request. Use when the user asks to check PR readiness, verify the branch is ready, or prepare for a pull request.
---

## Steps

1. Count commits ahead of main: run `git rev-list --count origin/main..HEAD`
   - If zero commits, report "No commits to review" and stop

2. Discover available review skills:
   - Check for `security-review` skill
   - Check for `style-check` skill
   - List which skills are available and which are missing

3. Run each available review skill and collect results

4. Check if AGENTS.md contains a "## PR Checklist" section
   - If found, verify each checklist item against the current state

5. Produce aggregated results:
   - Overall status: PASS or FAIL
   - Commit count
   - Results from each review skill (or "SKIPPED" if skill not found)
   - Any PR checklist items that are not satisfied
