#!/usr/bin/env python3
"""Self-test for install.py. Run: python3 scripts/selftest.py"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLER = ROOT / "install.py"


def run(home: Path, extra: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(INSTALLER), *extra],
        cwd=str(cwd or ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def assert_ok(proc: subprocess.CompletedProcess[str], label: str) -> None:
    if proc.returncode != 0:
        raise SystemExit(
            f"{label} failed ({proc.returncode})\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        home = tmp_path / "home"
        home.mkdir()
        project = tmp_path / "app"
        project.mkdir()
        (project / "package.json").write_text("{}\n", encoding="utf-8")

        proc = run(home, ["--dry-run"])
        assert_ok(proc, "dry-run")
        if (home / ".claude").exists():
            raise SystemExit("dry-run wrote files")

        proc = run(home, ["--project", str(project), "--project-only"])
        assert_ok(proc, "project-only")
        if (home / ".claude" / "skills" / "design-engine").exists():
            raise SystemExit("project-only leaked into HOME")
        if not (project / "DESIGN.md").is_file():
            raise SystemExit("DESIGN.md missing")
        if not (project / ".claude" / "skills" / "design-engine" / "SKILL.md").is_file():
            raise SystemExit("project skill missing")
        if not (project / ".design-engine" / "README.md").is_file():
            raise SystemExit(".design-engine missing")

        proc = run(home, [])
        assert_ok(proc, "global install")
        for rel in (
            ".claude/skills/design-engine/SKILL.md",
            ".claude/skills/design-engine/skill.md",
            ".codex/skills/design-engine/SKILL.md",
            ".hermes/skills/design-engine/SKILL.md",
            ".claude/CLAUDE.md",
            ".codex/AGENTS.md",
        ):
            if not (home / rel).is_file():
                raise SystemExit(f"missing {rel}")
        claude_md = (home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")
        if "DESIGN-ENGINE-PLUGIN:START" not in claude_md:
            raise SystemExit("marker missing from CLAUDE.md")

        proc = run(home, ["--uninstall"])
        assert_ok(proc, "uninstall")
        if (home / ".claude" / "skills" / "design-engine").exists():
            raise SystemExit("uninstall left skill dir")

        # project path that is a file
        file_target = tmp_path / "not-a-dir"
        file_target.write_text("x\n", encoding="utf-8")
        proc = run(home, ["--project", str(file_target), "--project-only"])
        if proc.returncode == 0:
            raise SystemExit("accepted a file as --project")

        missing = tmp_path / "nope"
        proc = run(home, ["--project", str(missing), "--project-only"])
        if proc.returncode == 0:
            raise SystemExit("accepted missing --project")

        proc = run(home, ["--project-only"])
        if proc.returncode == 0:
            raise SystemExit("accepted --project-only without --project")

    print("selftest: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
