# 05 — Does a review skill improve the result?

This is a paired **real-agent** evaluation. Both Claude Agent SDK providers use the
same model, prompts, read-only tools, and diff files. The only intended difference
is that one workspace contains `security-review/SKILL.md`. The requests do not
name the skill, so the skilled provider must discover it on its own.

```bash
python3 examples/05-paired-review/prepare.py
npx promptfoo eval -c examples/05-paired-review/promptfooconfig.yaml --repeat 3 --no-cache
```

You need the Claude Agent SDK (installed by the repository's `npm install`) and
working Anthropic authentication. If you use Vertex AI, configure the Claude SDK
environment as for the earlier examples. The three cases become six provider
rows per repeat, so `--repeat 3` makes 18 agent runs and incurs API cost.

The `prepare.py` script creates ignored workspaces under `fixtures/part3-review/`.
Run it with `--reset` to rebuild them after changing the skill or case files.
It refuses to delete a directory it did not generate.

`score-review.js` checks the final structured result against a small answer key:
two known vulnerabilities and one clean near-miss. It requires the right issue
kind **and file**, a usable explanation and fix, and rejects extra findings. The
same JSON schema is given to both providers and preserves the fields required by
the skill. The score is deliberately strict
for this teaching example; production review evals need more cases, human-checked
labels, and a matcher that can recognize equivalent findings expressed differently.

Compare scores by provider. A `3/3` repeat is a useful smoke signal, not a
reliability estimate. `skill-used` is omitted from the shared assertions because
it would correctly fail for the no-skill provider. Inspect the skilled provider's
trajectory or use the earlier trigger examples when you need invocation evidence.

For a larger case set, [Agent Eval Harness](https://github.com/opendatahub-io/agent-eval-harness)
could run the same comparison with each diff as a case and this answer key as a
code judge. Use its `execution.prompt` mode and stage the skill only in the
skilled condition. Its `execution.skill` mode invokes the skill explicitly, so
that mode measures execution after selection rather than natural discovery.
