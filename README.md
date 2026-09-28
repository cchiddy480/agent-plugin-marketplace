# 🛒 Milo Agent Plugin Marketplace

A curated plugin registry for AI coding agents (**Claude Code**, **OpenAI Codex CLI**, **Hermes Agent**, **Cursor**, **Windsurf**).

---

## 📦 Available Plugins

| Plugin | Version | Category | Description |
|---|---|---|---|
| **`design-engine`** | `1.0.1` | `software-development` | Standalone UI/UX design engine enforcing anti-slop rules, `DESIGN.md` token specs, the Iris triad workflow, and MCP hooks (Figma, v0, CDP). |

---

## ⚡ How to Add this Marketplace to Claude Code

```bash
# Add this marketplace to Claude Code
claude plugin marketplace add /home/open-claw/agent-plugin-marketplace

# Install the design-engine plugin
claude plugin install design-engine@milo-agent-marketplace
```

---

## 🛠️ Direct Standalone Install for Other Agents (Codex / Hermes / Cursor)

Each plugin includes its own universal `install.py`:

```bash
# Run standalone installer for design-engine
python3 plugins/design-engine/install.py
```

---

## 📁 Repository Structure

```
agent-plugin-marketplace/
├── marketplace.json                # Plugin registry manifest
├── .claude-plugins/
│   └── marketplace.json            # Claude Code plugin registry compatibility link
├── README.md                       # Marketplace documentation
└── plugins/
    └── design-engine/              # Standalone Design Engine plugin package
        ├── .claude-plugin/
        │   └── plugin.json
        ├── SKILL.md
        ├── install.py
        ├── README.md
        ├── LICENSE
        ├── references/
        ├── templates/
        └── skills/
```

---

## 📄 License
MIT License.
