# Skill Workshop

A hands-on repo for learning how to build, test, and ship AI agent skills.

## Structure

| Path | Description |
|------|-------------|
| `plugins/dev/skills/` | Skill definitions (SKILL.md files) |
| `plugins/dev/skills/*/evals/` | Promptfoo eval configs per skill |
| `fixtures/consumer/` | Fixture directory for eval runs |
| `.github/workflows/` | CI workflow for running evals |

## Running evals

```bash
npx promptfoo eval -c plugins/dev/skills/pre-commit-check/evals/promptfooconfig.yaml
npx promptfoo eval -c plugins/dev/skills/security-review/evals/trigger-tests.yaml
npx promptfoo eval -c plugins/dev/skills/security-review/evals/execution-tests.yaml
npx promptfoo eval -c plugins/dev/skills/pr-readiness/evals/promptfooconfig.yaml
```

## Conventions

- Skills use tool-neutral language (say "Run the command" not "Use the Bash tool")
- Evals use read-only tools where possible (`append_allowed_tools: ['Read', 'Grep', 'Glob']`)
- Scenario-based evals test skill logic without executing side effects
