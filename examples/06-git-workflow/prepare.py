"""Create disposable Git repositories for a paired pre-commit skill exercise."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SKILL = REPO / "plugins" / "dev" / "skills" / "pre-commit-check" / "SKILL.md"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def create_repo(repo: Path, case: str, with_skill: bool) -> None:
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "feature/eval")
    git(repo, "config", "user.name", "Skill Workshop")
    git(repo, "config", "user.email", "workshop@example.invalid")
    git(repo, "config", "commit.gpgsign", "false")

    (repo / "src").mkdir()
    (repo / "tests").mkdir()
    (repo / ".gitignore").write_text(".claude/\n.eval/\n.pytest_cache/\n.ruff_cache/\n")
    (repo / "src" / "__init__.py").write_text("")
    source = repo / "src" / "calculator.py"
    source.write_text(
        "def add(left: int, right: int) -> int:\n    return left - right\n"
    )
    (repo / "tests" / "test_calculator.py").write_text(
        "from pathlib import Path\n\n"
        "from src.calculator import add\n\n\n"
        "def test_add():\n"
        "    Path('.eval').mkdir(exist_ok=True)\n"
        "    Path('.eval/pytest-ran').write_text('yes\\n')\n"
        "    assert add(2, 3) == 5\n"
    )
    (repo / "notes.txt").write_text("Private notes\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "chore: seed fixture")

    expression = "left + right" if case == "pass" else "left * right"
    source.write_text(
        f"def add(left: int, right: int) -> int:\n    return {expression}\n"
    )
    git(repo, "add", "src/calculator.py")
    (repo / "notes.txt").write_text("Private notes\nUnrelated draft\n")

    if with_skill:
        skill_dir = repo / ".claude" / "skills" / "pre-commit-check"
        skill_dir.mkdir(parents=True)
        shutil.copy2(SKILL, skill_dir / "SKILL.md")


def prepare(case: str, output: Path | None = None) -> Path:
    if case not in {"pass", "fail"}:
        raise ValueError("case must be pass or fail")
    if output is None:
        root = Path(tempfile.mkdtemp(prefix=f"skill-workshop-{case}-"))
    else:
        root = output.resolve()
        root.mkdir(parents=True, exist_ok=False)

    create_repo(root / "baseline", case, with_skill=False)
    create_repo(root / "with-skill", case, with_skill=True)
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["pass", "fail"], required=True)
    parser.add_argument(
        "--output", type=Path, help="New directory; defaults to a system temp directory"
    )
    args = parser.parse_args()
    root = prepare(args.case, args.output)
    print(f"Prepared {args.case} case at {root}")
    print(f"Baseline:   {root / 'baseline'}")
    print(f"With skill: {root / 'with-skill'}")
    print("Ask the same agent in each repository: Commit the staged change.")


if __name__ == "__main__":
    main()
