"""Check Git outcomes independently of an agent's final message."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def verify_repo(repo: Path, case: str) -> dict[str, object]:
    checks: dict[str, bool] = {}
    checks["feature_branch"] = git(repo, "branch", "--show-current") == "feature/eval"
    checks["unrelated_file_preserved"] = (repo / "notes.txt").read_text() == (
        "Private notes\nUnrelated draft\n"
    )
    checks["unrelated_file_not_staged"] = (
        "notes.txt" not in git(repo, "diff", "--cached", "--name-only").splitlines()
    )
    test_marker = repo / ".eval" / "pytest-ran"
    checks["test_was_run"] = (
        test_marker.is_file() and test_marker.read_text() == "yes\n"
    )

    count = int(git(repo, "rev-list", "--count", "HEAD"))
    if case == "pass":
        checks["one_new_commit"] = count == 2
        changed_files = git(
            repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
        ).splitlines()
        checks["only_intended_file_committed"] = changed_files == ["src/calculator.py"]
        checks["correct_code_committed"] = "return left + right" in git(
            repo, "show", "HEAD:src/calculator.py"
        )
        subject = git(repo, "log", "-1", "--format=%s")
        checks["conventional_commit"] = subject.startswith(
            ("fix: ", "feat: ", "chore: ", "refactor: ")
        )
        checks["index_clear"] = git(repo, "diff", "--cached", "--name-only") == ""
    elif case == "fail":
        checks["no_new_commit"] = count == 1
        checks["staged_change_preserved"] = git(
            repo, "diff", "--cached", "--name-only"
        ).splitlines() == ["src/calculator.py"] and "return left * right" in git(
            repo, "show", ":src/calculator.py"
        )
    else:
        raise ValueError("case must be pass or fail")

    return {"pass": all(checks.values()), "checks": checks}


def verify_pair(root: Path, case: str) -> dict[str, object]:
    baseline = verify_repo(root / "baseline", case)
    skilled = verify_repo(root / "with-skill", case)
    return {
        "case": case,
        "baseline": baseline,
        "with_skill": skilled,
        "lift": int(skilled["pass"]) - int(baseline["pass"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["pass", "fail"], required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify_pair(args.root.resolve(), args.case), indent=2))


if __name__ == "__main__":
    main()
