# MCP Tools, Plugins & Integration Hooks

Connect agents to design sources and rendered-DOM verification. Do **not** invent tool names. Use whatever tools the connected MCP server actually exposes.

Official sources:
- Figma remote MCP: https://mcp.figma.com/mcp ([Figma docs](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server))
- v0 MCP: `npx mcp-remote https://v0.app/api/mcp` ([v0 docs](https://v0.app/docs/api/v1/adapters/mcp-server))
- Optional local Figma fallback: `npx -y figma-developer-mcp --stdio` ([npm](https://www.npmjs.com/package/figma-developer-mcp))

Copy `templates/mcp-config.json` into the host client's MCP config (Claude Code, Codex, Cursor, VS Code). OAuth happens in the client. Do not put API keys in committed project files.

---

## 1. Figma MCP

**Preferred:** remote server at `https://mcp.figma.com/mcp` (OAuth in the client).

**Local fallback** (when remote is unavailable):

```json
{
  "command": "npx",
  "args": ["-y", "figma-developer-mcp", "--stdio"],
  "env": { "FIGMA_API_KEY": "YOUR_FIGMA_PERSONAL_ACCESS_TOKEN" }
}
```

### Agent workflow

When the user pastes a Figma URL:

1. Parse `file_key` and `node-id` from the URL (`node-id=1-2` becomes `1:2`).
2. Call the **connected** Figma MCP tools (names vary by server; do not assume `figma_get_file`).
3. Map colors, type, spacing, and radii into `DESIGN.md` before writing production components.

Do not invent `figma_get_file`, `figma_get_node`, or `figma_export_image`. Those names are not guaranteed.

---

## 2. Vercel v0 MCP

Official client config (OAuth, **no API key in MCP config**):

```json
{
  "mcpServers": {
    "v0": {
      "command": "npx",
      "args": ["mcp-remote", "https://v0.app/api/mcp"]
    }
  }
}
```

Use v0 as an **Iris-stage baseline**. Clean class names, tokens, and states in the Forge pass. Do not ship v0 output verbatim.

A `v0` CLI (`v0 generate`) is optional and separate from MCP. Only use it if installed.

---

## 3. Browser / CDP verification

Prefer the agent's built-in browser tools. Optional MCP: `@modelcontextprotocol/server-puppeteer`.

Checks:

1. Screenshot at `1440x900` (desktop) and `375x812` (mobile).
2. Bounding boxes: overflow, clip, overlapping text.
3. Contrast on text vs background.
4. Breakpoints: 320 / 768 / 1024 / 1440.

Screenshots without DOM inspection are not a pass.

---

## 4. Storybook (optional)

```bash
npx storybook@latest init
```

For reusable primitives (Button, Modal, Table), add `.stories.tsx` covering `default`, `disabled`, `loading`, `error`.
