# Skill Workshop

A demo repository for the "Master Your Skills" blog series on developers.redhat.com.

## Structure

| Path | Description |
|------|-------------|
| `plugins/dev/skills/` | Skill definitions (SKILL.md files) |
| `plugins/dev/skills/*/evals/` | Promptfoo eval configs per skill |
| `fixtures/consumer/` | Fixture directory for eval runs |
| `.github/workflows/` | CI workflow for running evals |

## Running evals

```bash
cd plugins/dev/skills/security-review/evals
npx promptfoo eval
```

## Conventions

- Skills use tool-neutral language (say "Run the command" not "Use the Bash tool")
- Evals use read-only tools where possible (`append_allowed_tools: ['Read', 'Grep', 'Glob']`)
- Scenario-based evals test skill logic without executing side effects
