---
name: design-engine
description: Use when building or reviewing UI. Anti-slop visual rules, DESIGN.md tokens, Iris/Forge/Tester loop, Figma/v0/CDP hooks.
version: 1.0.1
author: Design Engine
license: MIT
status: active
category: software-development
metadata:
  hermes:
    tags: [design, ui, ux, frontend, anti-slop, tokens]
    related_skills: [design-md, sketch, browser-ui-verification]
---

# Design Engine: Agent Design & UI System

The **Design Engine** turns AI coding agents into disciplined UI/UX engineers. It rejects generic AI visual tropes ("AI slop") and enforces a design-first loop backed by token specs, modern component libraries, and rendered-DOM verification.

## When to Use

- Building or restyling a landing page, dashboard, app shell, or component.
- The user asks for "better UI", "less AI slop", "make it look like Linear/Stripe/Vercel".
- A repo has no `DESIGN.md` and frontend work is about to start.
- Visual QA after implementation (spacing, contrast, responsive, focus states).

Do not use for backend-only, CLI, or data-pipeline work with no UI surface.

## 1. Core Principles (Iris UX Engine)

When executing any design, component, or frontend task, adopt the **Iris UX Lead** mindset before writing code:

1. **Design Before Assembly.** Do not jump to production React/Vue logic without visual hierarchy, palette, and component boundaries.
2. **Anti-Slop Craftsmanship.** Reject generic gradient blobs, oversaturated purple-on-black cards, unaligned padding, and empty visual density.
3. **Token-Driven Consistency.** Ground styling in an explicit `DESIGN.md`.
4. **Verification Over Assumption.** Inspect rendered UI via CDP/DOM tools. Generated Tailwind is not proof it looks right.

## 2. The Design-First Triad Loop

Every UI feature follows this sequence:

```
[ Stage 1: Iris Pass ]  --->  [ Stage 2: Forge Pass ]  --->  [ Stage 3: Tester Pass ]
 Design Token Spec            Component Build                Visual QA & DOM Verification
 Prototype & Wireframe        Production React/Tailwind      Responsive & A11y Audit
```

Load `references/triad-workflow.md` for the full stage checklist.

### Stage 1: Iris Design Pass

1. Author or validate `DESIGN.md` in the repo root (see `templates/DESIGN.md`).
2. Create a lightweight HTML/CSS mockup or Tailwind prototype (`sketch` or v0) before application state.
3. Validate contrast, type scale, and layout density.

**Done when:** `DESIGN.md` exists, a mockup or layout spec exists, and the primary accent + radius scale are locked.

### Stage 2: Forge Implementation Pass

1. Build with **Tailwind CSS v3/v4** and **Shadcn UI** / **Radix** primitives.
2. Implement loading skeletons, empty states, error boundaries, and dark/light parity.
3. Add short transitions (`duration-150 ease-in-out`) and visible focus rings.

**Done when:** default/loading/empty/error/dark states exist and classes map to `DESIGN.md` tokens.

### Stage 3: Tester QA Pass

1. Inspect live output with CDP, Playwright, or browser snapshots.
2. Check 320px, 768px, 1024px, and 1440px.
3. Fix spacing mismatches, overflow, and broken focus before handoff.

**Done when:** the pre-flight matrix in `references/anti-slop-rules.md` is checked against the rendered page.

## 3. Anti-Slop Visual Rules Summary

| Aspect | Banned (AI Slop) | Required |
|---|---|---|
| **Colors** | Generic `from-purple-500 to-indigo-600` gradients | Neutral (`zinc`/`slate`) + 1 sharp primary accent |
| **Typography** | Default browser sans, uniform size/weight | Display title (tight tracking), mono for data |
| **Borders** | Stark drop shadows, missing borders | `border-border/50`, subtle layered shadows |
| **Layout** | Centered floating cards, identical padding | Optical anchor, 4px/8px micro-grid |
| **Radius** | Unconditional `rounded-3xl` on small widgets | `rounded-md` controls, `rounded-xl` containers |

Full rules: `references/anti-slop-rules.md`.

## 4. MCP Tools & Plugin Integrations

Do not invent tool names. Use the agent's actual MCP tools, or configure servers from `templates/mcp-config.json`.

### A. Figma

Official remote MCP: `https://mcp.figma.com/mcp` (OAuth in the client). Optional local fallback: `npx -y figma-developer-mcp --stdio` with `FIGMA_API_KEY`.

When the user pastes a Figma URL, parse `file_key` and `node-id`, then pull tokens/layout from the connected Figma MCP. Map results into `DESIGN.md`.

### B. Vercel v0

Official MCP: `npx mcp-remote https://v0.app/api/mcp` (OAuth, no API key in client config). CLI generation (`v0 generate`) is optional if the v0 CLI is installed.

Use v0 output as an Iris-stage baseline, then clean class names in the Forge pass.

### C. Browser / CDP QA

Prefer the agent's built-in browser tools. Optional MCP: `@modelcontextprotocol/server-puppeteer`.

Verify bounding boxes, type size, contrast, and viewports. Screenshots without DOM checks are insufficient.

Details: `references/mcp-and-plugins.md`.

## 5. File Structure in Projects

- `DESIGN.md`: project tokens (colors, fonts, radii, spacing).
- `components/ui/`: Shadcn/Radix primitives when the stack is React.
- `.design-engine/`: local mockups and visual QA logs (created by the installer).
- `.claude/skills/design-engine/`: project-local skill copy when installed with `--project`.

## Common Pitfalls

1. **Skipping `DESIGN.md`.** Implementation without a token lock produces mixed accents and radii.
2. **Trusting generated Tailwind.** Always inspect the rendered DOM.
3. **Hallucinating MCP tools** such as `figma_get_file`. Use whatever tools the connected server actually exposes.
4. **Copying v0 output verbatim.** Treat it as a sketch, not production.
5. **Installing globally when you only needed a project copy.** Use `--project-only`.

## Verification Checklist

- [ ] `DESIGN.md` exists and names one accent + one radius scale
- [ ] No purple-to-indigo default gradient, no `h-screen` hero
- [ ] Loading, empty, and error states implemented
- [ ] Rendered layout checked at 320 / 768 / 1024 / 1440
- [ ] Icon-only buttons have `aria-label`; focus rings visible
- [ ] Anti-slop matrix in `references/anti-slop-rules.md` passed
