# The Iris Design-First Triad Loop Workflow

The **Design-First Triad Loop** divides UI feature creation into 3 distinct operational roles: **Iris** (Design & UX), **Forge** (Full-Stack Engineering), and **The Tester** (QA & Verification).

---

## Workflow Overview

```
 ┌─────────────────────────────────────────────────────────┐
 │                   STAGE 1: IRIS PASS                    │
 │  - Define/Validate DESIGN.md                            │
 │  - Build lightweight HTML prototype or layout spec     │
 └────────────────────────────┬────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │                   STAGE 2: FORGE PASS                   │
 │  - Implement production React/Vue component             │
 │  - Connect Tailwind v4 & Shadcn primitives              │
 │  - Wire state: Loading, Empty, Error, Dark Mode        │
 └────────────────────────────┬────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │                  STAGE 3: TESTER PASS                   │
 │  - Execute CDP / Browser visual QA pass                 │
 │  - Verify responsive breakpoints (320px -> 1440px)      │
 │  - Validate accessibility & keyboard navigation         │
 └─────────────────────────────────────────────────────────┘
```

---

## Detailed Stage Execution

### Stage 1: Iris (Design Lead)
**Role:** Information Architecture, Visual Design, Token Specification.

1. **Check for `DESIGN.md`:** If `DESIGN.md` doesn't exist in the project root, instantiate it using `templates/DESIGN.md`.
2. **Draft Visual Layout:** Before writing complex application logic, produce a simple visual mockup or clean HTML file (`sketch.html` or draft component file) to inspect typography, spacing, and component structure.
3. **Establish Hierarchy:**
   - What is the primary focal point of this view?
   - Is data scannable without horizontal overflow?
   - Are primary actions visually distinct from secondary actions?

### Stage 2: Forge (Engineering Lead)
**Role:** Production Implementation & Component Assembly.

1. **Component Primitives:** Use clean, accessible component baselines (**Shadcn UI**, **Radix Primitives**, **Tailwind CSS**).
2. **State Complete Implementation:** Never leave a component half-baked. Always implement:
   - **Default State:** Clean layout with real/mock data.
   - **Loading State:** Skeleton loader (`animate-pulse bg-muted rounded`).
   - **Empty State:** Helpful icon, clear message, and primary CTA button.
   - **Error State:** Subtle red alert boundary with retry action.
   - **Dark / Light Mode:** Class-based `dark:` variant parity.
3. **Prop Architecture:** Expose clean TypeScript prop interfaces (`interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>`).

### Stage 3: The Tester (QA Lead)
**Role:** Visual Verification, DOM Inspection, Responsiveness & Accessibility Audit.

1. **Browser Inspection:** Launch browser verification using Chrome DevTools Protocol (CDP) or Playwright.
2. **Responsive Matrix:**
   - `Mobile (320px - 480px)`: Hamburger/drawer navigation, stacked columns, touch target padding (min 44px).
   - `Tablet (768px - 1024px)`: 2-column grids, collapsible sidebars.
   - `Desktop (1280px+)`: Full multi-column dashboard grid.
3. **Accessibility (a11y) Check:**
   - ARIA labels on icon-only buttons (`aria-label="Close menu"`).
   - Focus outline visibility when using `Tab` key navigation.
   - Semantic HTML tags (`<header>`, `<main>`, `<section>`, `<nav>`, `<article>`).
