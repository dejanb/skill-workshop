# Skill Workshop

A hands-on repo for learning how to build, test, and ship AI agent skills. Contains working skills, [promptfoo](https://www.promptfoo.dev/) eval configs, and fixture directories you can run yourself.

## Quick Start

```bash
git clone https://github.com/dejanb/skill-workshop.git
cd skill-workshop
npm install @anthropic-ai/claude-agent-sdk
npx promptfoo eval -c examples/01-first-trigger.yaml
```

## What's Inside

### Skills

Four skills in `plugins/dev/skills/`:

| Skill | Description |
|-------|-------------|
| `pre-commit-check` | Run lint, test, and type-check before committing |
| `security-review` | Review code changes for common security vulnerabilities |
| `style-check` | Check naming conventions and style rules |
| `pr-readiness` | Orchestration skill — count commits, discover review skills, aggregate results |

### Runnable Examples

Promptfoo eval configs in `examples/`, covering different testing patterns:

| File | What it tests |
|------|---------------|
| `01-first-trigger.yaml` | Single trigger test — does the skill activate? |
| `02-trigger-layers.yaml` | Positive, near-miss, and negative triggers |
| `03-execution-tests.yaml` | Recall and precision with planted diffs |
| `04-scenario-tests.yaml` | Scenario-based orchestration testing |

Run any example:

```bash
npx promptfoo eval -c examples/01-first-trigger.yaml
```

### Eval Fixtures

- `fixtures/consumer/` — A minimal project the agent runs against during evals, with skills symlinked into `.claude/skills/`
- `plugins/dev/skills/security-review/evals/diffs/` — Planted diffs for recall/precision tests
- `plugins/dev/skills/pr-readiness/evals/scenarios/` — Pre-written step results for scenario-based tests

## Authentication

The example configs use Vertex AI by default (`CLAUDE_CODE_USE_VERTEX`). To use the Anthropic API directly instead, remove the `env` block from the example YAML files and set:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

## Repo Structure

```
skill-workshop/
├── examples/                          # Runnable eval configs
├── plugins/dev/
│   ├── .claude-plugin/plugin.json     # Plugin metadata
│   └── skills/
│       ├── pre-commit-check/          # SKILL.md + evals/
│       ├── security-review/           # SKILL.md + evals/ + diffs/
│       ├── style-check/               # SKILL.md (no evals)
│       └── pr-readiness/              # SKILL.md + evals/ + scenarios/
├── fixtures/consumer/                 # Test fixture project
│   ├── .claude/skills/                # Symlinks → plugins/dev/skills/*
│   ├── .agents/skills/                # Symlinks → plugins/dev/skills/*
│   └── src/                           # Sample Python code
├── .github/workflows/skill-evals.yml  # CI workflow
├── marketplace.json                   # Marketplace config
└── AGENTS.md                          # Repo orientation for agents
```

## License

MIT
