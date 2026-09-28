# Design Engine

Standalone UI/UX skill pack for AI coding agents: **Claude Code**, **OpenAI Codex CLI**, **Hermes**, **Cursor**, **Windsurf**.

It is a skill + installer + templates. It does not ship a runtime MCP server. Agents still need Figma/v0/browser tools configured in the host client.

---

## What it enforces

- **Anti-slop rules:** neutrals + one accent, 4px/8px grid, no default purple gradients, no `h-screen` heroes, no em-dash flourishes.
- **Token lock:** project `DESIGN.md` before production components.
- **Triad loop:** Iris spec/mockup → Forge implementation → Tester rendered-DOM QA.
- **MCP hooks (optional):** Figma remote MCP, v0 MCP via `mcp-remote`, Puppeteer/CDP.

---

## Install

Requires Python 3.9+.

```bash
# Global: Claude Code, Codex, Hermes (+ Cursor/Windsurf/brain-vault if present)
python3 install.py

# Preview writes
python3 install.py --dry-run

# One project only (DESIGN.md + .claude/skills/design-engine + .design-engine/)
python3 install.py --project /path/to/webapp --project-only

# Global + project
python3 install.py --project /path/to/webapp

# Remove skill copies and instruction markers (leaves DESIGN.md)
python3 install.py --uninstall
```

### Claude Code plugin layout

This directory is also a Claude Code plugin (`skills` at plugin root):

```bash
claude plugin validate .
# then load with --plugin-dir, or add to a marketplace
```

### Codex / Hermes / Cursor

The installer copies `SKILL.md` + `references/` + `templates/` into:

| Client | Path |
|---|---|
| Claude Code | `~/.claude/skills/design-engine/` and a marker in `~/.claude/CLAUDE.md` |
| Codex CLI | `~/.codex/skills/design-engine/` and a marker in `~/.codex/AGENTS.md` |
| Hermes | `~/.hermes/skills/design-engine/` |
| Cursor | `~/.cursor/skills/design-engine/` if `~/.cursor` exists |
| Windsurf | `~/.windsurf/skills/` or `~/.codeium/windsurf/skills/` if present |
| Brain Vault | `~/brain-vault/02-skills/design-engine/` if that vault exists |

---

## Layout

```
design-engine-plugin/
├── SKILL.md
├── README.md
├── LICENSE
├── install.py
├── .claude-plugin/plugin.json
├── references/
│   ├── anti-slop-rules.md
│   ├── triad-workflow.md
│   └── mcp-and-plugins.md
└── templates/
    ├── DESIGN.md
    ├── mcp-config.json
    └── tailwind.config.template.js
```

---

## MCP (optional)

Copy `templates/mcp-config.json` into the client MCP config. Do not commit secrets.

- **Figma (preferred):** `https://mcp.figma.com/mcp` (OAuth)
- **Figma local fallback:** `npx -y figma-developer-mcp --stdio` + `FIGMA_API_KEY`
- **v0:** `npx mcp-remote https://v0.app/api/mcp` (OAuth, no API key in config)
- **Browser:** `@modelcontextprotocol/server-puppeteer` or the agent's own browser tools

Agents must use the **connected** tool names. Do not call invented names like `figma_get_file`.

---

## How agents should run a UI task

1. Read or create `DESIGN.md`.
2. Iris: mockup / layout spec.
3. Forge: Tailwind + Shadcn/Radix, with loading/empty/error/dark states.
4. Tester: inspect the rendered DOM at 320 / 768 / 1024 / 1440.
5. Pass `references/anti-slop-rules.md` pre-flight before claiming done.

---

## License

MIT.
