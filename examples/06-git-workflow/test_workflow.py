"""Offline checks for the disposable Git fixture and its verifier."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = load("prepare")
verify = load("verify")


class GitWorkflowFixtureTests(unittest.TestCase):
    def test_passing_case_accepts_only_intended_commit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = prepare.prepare("pass", Path(temp) / "fixture")
            self.assertFalse(verify.verify_repo(root / "with-skill", "pass")["pass"])
            repo = root / "with-skill"
            marker = repo / ".eval" / "pytest-ran"
            marker.parent.mkdir()
            marker.write_text("yes\n")
            prepare.git(repo, "commit", "-qm", "fix: correct addition")
            result = verify.verify_repo(repo, "pass")
            self.assertTrue(result["pass"], result["checks"])
            self.assertFalse((root / "baseline" / ".claude").exists())
            skill = repo / ".claude" / "skills" / "pre-commit-check" / "SKILL.md"
            self.assertTrue(skill.exists())

    def test_failing_case_rejects_commit_and_preserves_staged_work(self):
        with tempfile.TemporaryDirectory() as temp:
            root = prepare.prepare("fail", Path(temp) / "fixture")
            repo = root / "with-skill"
            result = verify.verify_repo(repo, "fail")
            self.assertFalse(result["pass"], result["checks"])
            marker = repo / ".eval" / "pytest-ran"
            marker.parent.mkdir()
            marker.write_text("yes\n")
            self.assertTrue(verify.verify_repo(repo, "fail")["pass"])
            prepare.git(repo, "commit", "-qm", "fix: commit failing code")
            self.assertFalse(verify.verify_repo(repo, "fail")["pass"])

    def test_unrelated_file_in_commit_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = prepare.prepare("pass", Path(temp) / "fixture")
            repo = root / "with-skill"
            marker = repo / ".eval" / "pytest-ran"
            marker.parent.mkdir()
            marker.write_text("yes\n")
            prepare.git(repo, "add", "notes.txt")
            prepare.git(repo, "commit", "-qm", "fix: correct addition")
            result = verify.verify_repo(repo, "pass")
            self.assertFalse(result["pass"])
            self.assertFalse(result["checks"]["only_intended_file_committed"])


if __name__ == "__main__":
    unittest.main()
