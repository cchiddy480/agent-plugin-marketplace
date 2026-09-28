# Anti-Slop Visual Rules & Craftsmanship Guide

This reference defines the strict aesthetic standards enforced by the **Design Engine**. Standard AI code generation often defaults to generic, uninspired visual patterns ("AI slop"). Follow these explicit rules to ensure designs match top-tier hand-crafted applications (Linear, Stripe, Vercel, Supabase).

---

## 1. Color Science & Palette Discipline

### The "Single Accent" Rule
- Standard AI models mix multiple saturated gradients (`purple` + `pink` + `cyan`) without visual purpose.
- **Design Engine Rule:** Base 90% of your interface on refined neutrals (`slate`, `zinc`, or `neutral`). Introduce **exactly ONE** primary accent color (e.g., crisp emerald `#10b981`, sharp blue `#2563eb`, or amber `#f59e0b`).
- Semantic status colors (Red = Error, Green = Success, Yellow = Warning) must remain muted and desaturated until active.

### Background & Surface Layering
Do not use flat single-color backgrounds. Create depth through 3 surface levels:
1. **App Background:** Lowest elevation (`bg-background` / `bg-zinc-950`).
2. **Card Surface:** Middle elevation (`bg-card` / `bg-zinc-900/80` with `border border-zinc-800/60`).
3. **Floating Controls & Popovers:** Highest elevation (`bg-popover` / `bg-zinc-800` with `shadow-lg border border-zinc-700/50`).

### Color Consistency Lock
Once an accent color is chosen for a page, it is used on the WHOLE page. A warm-grey site does not suddenly get a blue CTA in section 7. A rose-accented site does not get a teal status badge in the footer. Pick one accent, lock it, and audit every component before shipping.

---

## 2. Typography & Spatial Hierarchy

### Font Pairing Standards
- **Sans-Serif (Body & Display):** Use Geist, Inter, Satoshi, or SF Pro with tight letter spacing on titles (`tracking-tight`) and relaxed line height on body text (`leading-relaxed`).
- **Monospace (Data & Code):** Use Geist Mono or JetBrains Mono for numbers, badge counters, table columns, code blocks, and timestamps (`font-mono text-xs`).

### Scale & Weight Distinctions
- Contrast should come from **weight and size**, not just raw scale.
- Main titles: `text-2xl md:text-5xl font-semibold tracking-tight text-foreground`
- Section labels: `text-xs font-medium uppercase tracking-wider text-muted-foreground`
- Body copy: `text-sm text-muted-foreground max-w-[65ch]`

### Italic Descender Clearance
When italic is used in display type and the word contains a descender letter (`y g j p q`), `leading-[1]` will clip the descender. Use `leading-[1.1]` minimum and add `pb-1` reserve on the wrapping element.

---

## 3. Micro-Spacing Grid & Borders

### The 4px/8px Spatial Budget
- Every padding, margin, and gap must be a multiple of 4px (`p-2` = 8px, `p-4` = 16px, `p-6` = 24px, `gap-3` = 12px).
- **Padding Hierarchy:** Container cards use `p-5` or `p-6`. Inner sections use `p-4`. Buttons and badge controls use `px-3 py-1.5`.

### Subtle Borders Over Harsh Shadows
- Replace heavy `shadow-2xl` drop shadows with crisp 1px borders:
  ```css
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  ```

---

## 4. Proportional Border Radii & Shape Consistency

- **Inputs, Buttons, Badges:** `rounded-md` (6px) or `rounded-lg` (8px).
- **Cards, Modals, Panels:** `rounded-xl` (12px) or `rounded-2xl` (16px).
- **Avatars, Status Dots:** `rounded-full`.
- **Nested Radii Rule:** Parent radius must be larger than child radius! `Parent Radius = Child Radius + Inner Padding`.
- **Shape Consistency Lock:** Pick ONE corner-radius scale for the page and stick to it across all cards and controls.

---

## 5. Banned AI Tells & Forbidden Patterns

### 1. The Em-Dash Ban (`—`)
The em-dash character (`—` or `–`) is **completely banned** as a visual or typographic flourish in headlines, eyebrows, button labels, quotes, image captions, and alt text. Restructure copy using commas, periods, or clean layout breaks.

### 2. Eyebrow Restraint
- **Maximum 1 eyebrow per 3 sections.** An "eyebrow" is the small uppercase wide-tracking label sitting above a section headline (`text-xs uppercase tracking-wider`). Do not put an eyebrow above every single section header.

### 3. Hero Layout Discipline
- **Hero MUST fit in initial viewport (`min-h-[100dvh]`).** Never use `h-screen`.
- Headline max 2 lines on desktop. Subtext max **20 words**.
- Top padding cap: max `pt-24` on desktop.
- Max 4 text elements in hero (Eyebrow/Brand strip, H1, Subtext, CTAs). No taglines below CTAs, no trust micro-strips inside the hero card.

### 4. Logo Wall Rules
- "Trusted by" logo walls must live **UNDER** the hero, never inside it.
- Logos must be real SVG icons (`Simple Icons` / `devicon`) or clean SVG marks. Never plain text wordmarks with category labels printed underneath.

### 5. Fake Product Previews
- **Div-based fake screenshots are banned.** Do not draw fake terminal windows or fake dashboard grids with styled `<div>` rectangles to simulate a product preview. Use a real screenshot, a generated image asset, or an actual mini-component preview.

---

## 6. Pre-Flight Verification Check Matrix

Run this matrix before declaring any UI output complete:

- [ ] **ZERO em-dashes (`—`) anywhere on the page.**
- [ ] **Page Theme Lock:** Single theme consistency (no random section flips).
- [ ] **Color Consistency Lock:** Single primary accent color used across all components.
- [ ] **Shape Consistency Lock:** One uniform corner-radius scale.
- [ ] **CTA Button Wrap:** Primary CTAs fit on one line at desktop without wrapping.
- [ ] **Button & Form Contrast Check:** Passes WCAG AA contrast (min 4.5:1).
- [ ] **Eyebrow Count:** Eyebrow uppercase labels ≤ `ceil(sectionCount / 3)`.
- [ ] **Hero Stack Discipline:** Max 4 text elements; subtext ≤ 20 words.
- [ ] **Logo Wall:** Uses clean SVG marks under hero, no plain-text category labels.
- [ ] **No Div-based Fake Screenshots:** Uses real images/SVG or mini-components.
- [ ] **Viewport Stability:** Uses `min-h-[100dvh]`, never `h-screen`.
