# 06 — Verify the result of an action-taking skill

This exercise builds two identical temporary Git repositories. Only one contains
the `pre-commit-check` skill. The `pass` case has a staged fix that passes the
project test; the `fail` case has a staged change that fails it. Both have an
unrelated, unstaged note that the agent must preserve.

```bash
python3 examples/06-git-workflow/prepare.py --case pass
python3 examples/06-git-workflow/prepare.py --case fail
```

The commands print new paths under your system temporary directory. Open each
`baseline` and `with-skill` repository in the **same** coding agent and ask the
same natural request: **“Commit the staged change.”** Do not name the skill in
the request. For Claude Code, the skill is installed under `.claude/skills/` only
in the skilled repository. You can copy it into the equivalent native location
when testing another agent. Use the same model and settings for both runs, and
check that your personal agent configuration does not already provide
`pre-commit-check` to the baseline.

The workflow skill asks for `ruff` and `pytest`; install them in the agent's
environment before running the exercise. Use only these disposable repositories,
not a real project checkout. No remote is configured, and `.claude/` is ignored
by Git. Review the agent's tool trace to see whether it ran the checks.

After both runs, check the actual Git state with the printed root path:

```bash
python3 examples/06-git-workflow/verify.py --case pass --root /tmp/skill-workshop-pass-XXXX
python3 examples/06-git-workflow/verify.py --case fail --root /tmp/skill-workshop-fail-XXXX
```

The verifier checks the branch, commit count, committed file, index, and
preservation of the unrelated note. The test writes an ignored marker when
`pytest` runs, so the verifier can also tell whether the agent attempted the
test in both the passing and failing case. It prints each condition's result
and the skilled-minus-baseline outcome (`lift`). The verifier does not read
the agent's final message. Inspect the tool trace to confirm the lint command
and the sequence of actions. A failed baseline is a measurement, not a script
error.

Repeat the exercise with fresh repositories if you want to estimate variability.
The preparation script never overwrites an existing directory.
