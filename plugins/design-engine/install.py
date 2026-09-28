#!/usr/bin/env python3
"""
Design Engine Installer

Installs the standalone Design Engine skill and reference specs into AI coding agents:
  - Claude Code (~/.claude/skills/ & ~/.claude/CLAUDE.md)
  - OpenAI Codex CLI (~/.codex/skills/ & ~/.codex/AGENTS.md)
  - Hermes Agent (~/.hermes/skills/)
  - Cursor (~/.cursor/skills/) when ~/.cursor exists
  - Windsurf (~/.windsurf/skills/ or ~/.codeium/windsurf/skills/) when present
  - Brain Vault (~/brain-vault/02-skills/) when present
  - Local project repository (--project <path>)

Usage:
  python3 install.py
  python3 install.py --project /path/to/my-web-app
  python3 install.py --project /path/to/my-web-app --project-only
  python3 install.py --dry-run
  python3 install.py --uninstall
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent

BEGIN_MARKER = "<!-- DESIGN-ENGINE-PLUGIN:START -->"
END_MARKER = "<!-- DESIGN-ENGINE-PLUGIN:END -->"

REQUIRED_FILES = (
    PLUGIN_ROOT / "SKILL.md",
    PLUGIN_ROOT / "references" / "anti-slop-rules.md",
    PLUGIN_ROOT / "references" / "triad-workflow.md",
    PLUGIN_ROOT / "references" / "mcp-and-plugins.md",
    PLUGIN_ROOT / "templates" / "DESIGN.md",
    PLUGIN_ROOT / "templates" / "mcp-config.json",
    PLUGIN_ROOT / "templates" / "tailwind.config.template.js",
)

GLOBAL_INSTRUCTION_BLOCK = f"""{BEGIN_MARKER}
## Design Engine (UI/UX & Anti-Slop System)
- **Active Skill:** Installed and enabled (`design-engine`).
- **Workflow:** 3-Stage Design Loop (Stage 1: Iris Pass -> Stage 2: Forge Build -> Stage 3: Tester QA).
- **Standards:** Enforce anti-slop visual rules, ground styling in project `DESIGN.md`, pair clean typography, strict 4px/8px micro-grid.
- **MCP Hooks:** Figma MCP / v0 MCP / CDP Browser Visual QA.
{END_MARKER}"""


class InstallError(Exception):
    """Recoverable installer failure with a user-facing message."""


def _eprint(message: str) -> None:
    print(message, file=sys.stderr)


def validate_plugin_root() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        raise InstallError(
            "Plugin package is incomplete. Missing:\n  - " + "\n  - ".join(missing)
        )


def replace_tree(src: Path, dest: Path, *, dry_run: bool) -> None:
    if not src.is_dir():
        raise InstallError(f"Source directory missing: {src}")
    if dest.exists() and dest.is_symlink():
        raise InstallError(f"Refusing to replace symlink: {dest}")
    if dest.exists() and dest.is_file():
        raise InstallError(f"Refusing to replace file with directory: {dest}")
    if dry_run:
        print(f"  [dry-run] sync {src} -> {dest}")
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_skill_directory(dest_dir: Path, *, dry_run: bool) -> None:
    if dest_dir.exists() and dest_dir.is_symlink():
        raise InstallError(f"Refusing to install into symlink: {dest_dir}")
    if dest_dir.exists() and not dest_dir.is_dir():
        raise InstallError(f"Skill destination is not a directory: {dest_dir}")
    if dry_run:
        print(f"  [dry-run] would sync skill to: {dest_dir}")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PLUGIN_ROOT / "SKILL.md", dest_dir / "SKILL.md")
    # Brain Vault and some older loaders look for skill.md (lowercase).
    shutil.copy2(PLUGIN_ROOT / "SKILL.md", dest_dir / "skill.md")
    replace_tree(PLUGIN_ROOT / "references", dest_dir / "references", dry_run=False)
    replace_tree(PLUGIN_ROOT / "templates", dest_dir / "templates", dry_run=False)
    print(f"  [ok] Synced Design Engine skill to: {dest_dir}")


def inject_global_instruction(file_path: Path, *, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] would update global instructions: {file_path}")
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = file_path.read_text(encoding="utf-8") if file_path.exists() else ""

    start_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_idx += len(END_MARKER)
        new_content = content[:start_idx] + GLOBAL_INSTRUCTION_BLOCK + content[end_idx:]
    elif start_idx != -1:
        # START without END: replace from START to EOF to avoid duplicate blocks.
        prefix = content[:start_idx].rstrip()
        new_content = (prefix + "\n\n" if prefix else "") + GLOBAL_INSTRUCTION_BLOCK + "\n"
    else:
        prefix = content.rstrip()
        new_content = (prefix + "\n\n" if prefix else "") + GLOBAL_INSTRUCTION_BLOCK + "\n"

    if not new_content.endswith("\n"):
        new_content += "\n"
    file_path.write_text(new_content, encoding="utf-8")
    print(f"  [ok] Updated global instructions: {file_path}")


def remove_instruction_block(file_path: Path, *, dry_run: bool) -> None:
    if not file_path.is_file():
        return
    content = file_path.read_text(encoding="utf-8")
    start_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)
    if start_idx == -1:
        return
    if dry_run:
        print(f"  [dry-run] would strip instruction block from: {file_path}")
        return
    if end_idx != -1 and end_idx > start_idx:
        end_idx += len(END_MARKER)
        new_content = (content[:start_idx] + content[end_idx:]).strip() + "\n"
    else:
        new_content = content[:start_idx].rstrip() + "\n"
    file_path.write_text(new_content, encoding="utf-8")
    print(f"  [ok] Removed instruction block: {file_path}")


def remove_skill_directory(dest_dir: Path, *, dry_run: bool) -> None:
    if not dest_dir.exists():
        return
    if dest_dir.is_symlink() or not dest_dir.is_dir():
        raise InstallError(f"Refusing to delete non-directory skill path: {dest_dir}")
    if dest_dir.name != "design-engine":
        raise InstallError(f"Refusing to delete unexpected path: {dest_dir}")
    if dry_run:
        print(f"  [dry-run] would remove: {dest_dir}")
        return
    shutil.rmtree(dest_dir)
    print(f"  [ok] Removed: {dest_dir}")


def home_dir() -> Path:
    return Path.home()


def optional_skill_targets(home: Path) -> list[Path]:
    targets: list[Path] = []
    if (home / "brain-vault").is_dir():
        targets.append(home / "brain-vault" / "02-skills" / "design-engine")
    if (home / ".cursor").exists():
        targets.append(home / ".cursor" / "skills" / "design-engine")
    if (home / ".windsurf").exists():
        targets.append(home / ".windsurf" / "skills" / "design-engine")
    elif (home / ".codeium" / "windsurf").exists():
        targets.append(home / ".codeium" / "windsurf" / "skills" / "design-engine")
    return targets


def install_global(*, dry_run: bool) -> None:
    home = home_dir()
    print("Installing Design Engine into global agent environments...")

    copy_skill_directory(home / ".claude" / "skills" / "design-engine", dry_run=dry_run)
    inject_global_instruction(home / ".claude" / "CLAUDE.md", dry_run=dry_run)

    copy_skill_directory(home / ".codex" / "skills" / "design-engine", dry_run=dry_run)
    inject_global_instruction(home / ".codex" / "AGENTS.md", dry_run=dry_run)

    copy_skill_directory(home / ".hermes" / "skills" / "design-engine", dry_run=dry_run)

    for dest in optional_skill_targets(home):
        copy_skill_directory(dest, dry_run=dry_run)


def uninstall_global(*, dry_run: bool) -> None:
    home = home_dir()
    print("Removing Design Engine from global agent environments...")
    remove_skill_directory(home / ".claude" / "skills" / "design-engine", dry_run=dry_run)
    remove_instruction_block(home / ".claude" / "CLAUDE.md", dry_run=dry_run)
    remove_skill_directory(home / ".codex" / "skills" / "design-engine", dry_run=dry_run)
    remove_instruction_block(home / ".codex" / "AGENTS.md", dry_run=dry_run)
    remove_skill_directory(home / ".hermes" / "skills" / "design-engine", dry_run=dry_run)
    for dest in optional_skill_targets(home):
        remove_skill_directory(dest, dry_run=dry_run)


def resolve_project_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    if not path.exists():
        raise InstallError(f"Project path does not exist: {raw}")
    if not path.is_dir():
        raise InstallError(f"Project path is not a directory: {raw}")
    if os.name != "nt" and path == Path("/"):
        raise InstallError("Refusing to install into filesystem root.")
    return path


def install_project(project_path: Path, *, dry_run: bool) -> None:
    print(f"Installing Design Engine into project: {project_path}")

    target_design_md = project_path / "DESIGN.md"
    if target_design_md.exists():
        print(f"  [skip] DESIGN.md already exists: {target_design_md}")
    elif dry_run:
        print(f"  [dry-run] would write: {target_design_md}")
    else:
        shutil.copy2(PLUGIN_ROOT / "templates" / "DESIGN.md", target_design_md)
        print(f"  [ok] Instantiated project template: {target_design_md}")

    design_engine_dir = project_path / ".design-engine"
    if dry_run:
        print(f"  [dry-run] would ensure: {design_engine_dir}")
    else:
        design_engine_dir.mkdir(parents=True, exist_ok=True)
        readme = design_engine_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                "# Design Engine local workspace\n\n"
                "Store reference mockups, visual QA logs, and token experiments here.\n"
                "Do not commit secrets. MCP tokens belong in your agent config, not this folder.\n",
                encoding="utf-8",
            )
        print(f"  [ok] Ensured local workspace: {design_engine_dir}")

    copy_skill_directory(
        project_path / ".claude" / "skills" / "design-engine",
        dry_run=dry_run,
    )


def uninstall_project(project_path: Path, *, dry_run: bool) -> None:
    print(f"Removing Design Engine skill from project: {project_path}")
    remove_skill_directory(
        project_path / ".claude" / "skills" / "design-engine",
        dry_run=dry_run,
    )
    print("  [note] Left DESIGN.md and .design-engine/ in place (project content).")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Design Engine into Claude Code, Codex, Hermes, Cursor, Windsurf, or local projects."
    )
    parser.add_argument("--project", type=str, help="Target project directory path")
    parser.add_argument(
        "--project-only",
        action="store_true",
        help="Install into --project without writing global agent skill directories",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove installed skill copies and instruction markers",
    )
    args = parser.parse_args(argv)
    if args.project_only and not args.project:
        parser.error("--project-only requires --project")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_plugin_root()
        project_path = resolve_project_path(args.project) if args.project else None

        if args.uninstall:
            if not args.project_only:
                uninstall_global(dry_run=args.dry_run)
            if project_path is not None:
                uninstall_project(project_path, dry_run=args.dry_run)
            print("\nDesign Engine uninstall complete.")
            return 0

        if not args.project_only:
            install_global(dry_run=args.dry_run)
        if project_path is not None:
            install_project(project_path, dry_run=args.dry_run)

        print("\nDesign Engine installation complete. Agents can now apply anti-slop UI rules.")
        return 0
    except InstallError as exc:
        _eprint(f"Error: {exc}")
        return 1
    except OSError as exc:
        _eprint(f"Error: filesystem failure: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
