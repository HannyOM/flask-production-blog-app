# Frontend Design Playbook

If you are generating or modifying frontend code, you MUST follow this playbook.

Do not skip steps.

If a step requires approval, STOP and wait for confirmation before continuing.

# Frontend Design Specification

This document defines the workflow Opencode must follow when designing the frontend of a web application.

You will be provided with:

- A downloaded webpage `.html` file (usually from a Framer template)
- `template_tailwind.config.js` (consistent across different pages)
- `design-tokens.json` (consistent across different pages)

Your task is to analyze the design and translate it into a **componentized Tailwind + Flowbite frontend architecture**.

Follow the phases below **in order**.

---

# Phase 1 — Design Analysis

First analyze the provided HTML template.

Extract the following structural patterns:

- Visual hierarchy
- Spacing scale
- Grid patterns
- Repeated components

Focus on **layout structure**, not styling details.

---

# Phase 2 — Layout System Description

Before writing **any code**, describe the layout system used in the design.

Do **NOT generate HTML yet**.

Describe the following:

### Container

- Maximum container width
- Centering method
- Horizontal padding

### Grid System

Identify the grid layout used in major sections.

Examples:

- Hero section grid
- Feature section grid
- Blog card grid
- Footer columns

### Spacing System

Describe vertical rhythm and internal spacing.

Examples:

- Section spacing
- Card padding
- Grid gaps
- Container padding

### Column Layouts

Explain how many columns are used across sections.

Examples:

- 2-column hero layout
- 3-column feature grid
- 3-column blog cards

### Responsive Breakpoints

Describe how the layout adapts across screen sizes.

Examples:

- Mobile stacking
- Tablet column count
- Desktop grid layout

---

### Example Layout Analysis

Layout Analysis

Container

- max-width: 1280px
- centered using `mx-auto`

Grid system

- Hero section: 2 columns (text + image)
- Features section: 3-column grid
- Blog posts: 3-column card grid

Spacing

- Section spacing: `py-24`
- Card padding: `p-6`
- Grid gaps: `gap-8`

---

After presenting the layout system:

**Stop and wait for approval before continuing.**

Do not generate HTML yet.

---

# Phase 3 — Tailwind Configuration Update

Once the layout analysis is approved:

Update the existing `tailwind.config.js` file with `template_tailwind.config.js` and to match the design system.

Adjust:

- container width
- spacing scale
- fonts
- colors
- breakpoints
- design tokens

Ensure the configuration matches values found in:

- `design-tokens.json`
- the analyzed template

---

# Phase 4 — Tailwind Design System Translation

Convert the design into **reusable Tailwind utilities**. Also read the `design-tokens.json` file for this. 

Define a clear design system.

Example:

### Colors

- Primary: `indigo-600`
- Accent: `pink-500`
- Background: `slate-50`
- Text: `slate-900`

### Typography

- H1 → `text-5xl font-bold`
- H2 → `text-3xl font-semibold`
- Body → `text-base`

### Layout

- Max container width → `max-w-7xl`
- Section spacing → `py-24`
- Card padding → `p-6`
- Grid gaps → `gap-8`

These utilities should be reused consistently across components.

---

# Phase 5 — Flowbite Component Mapping

Whenever possible, use **Flowbite UI components** instead of custom implementations.

Map UI elements to Flowbite equivalents.

Example:

| UI Element | Flowbite Component |
| ---------- | ------------------ |
| Navbar     | Flowbite Navbar    |
| Buttons    | Flowbite Buttons   |
| Cards      | Flowbite Cards     |
| Dropdowns  | Flowbite Dropdown  |
| Modals     | Flowbite Modal     |
| Forms      | Flowbite Forms     |

Only create custom components if Flowbite does not provide a suitable one.

---

# Phase 6 — Componentized Template Structure

All reusable UI components must be separated into template components.

Check for a `components` folder in the `templates` folder in the `bloggr` folder of the root directory, flask-blog-production-app.

If there is none, create a `components` folder in the `templates` folder in the `bloggr` folder of the root directory, flask-blog-production-app.

In this folder, store the components.
The structure will look like this:
flask-blog-production-app/
bloggr/
templates/
components/
navbar.html
hero.html
post_card.html
footer.html

Rules:

- Each UI element must be a reusable component.
- Components should contain **only their own markup**.
- Components must be included inside layout templates.

---

# Phase 7 — Layout Skeleton Creation

Next create the **page layout skeleton**.

Break the design into major sections.

Examples:

- Page layout
- Navbar
- Hero section
- Features section
- Blog post grid
- Footer

At this stage:

- Generate **layout containers only**
- Do **not add styling or content**
- Do **not implement components yet**

Use only structural Tailwind utilities.

Example:

```html
<div class="max-w-7xl mx-auto px-6">
  <section class="py-24">
    <!-- hero -->
  </section>

  <section class="py-24">
    <!-- blog posts -->
  </section>
</div>
```

---

# Phase 8 — Populate Sections With Components

Finally populate each section with the appropriate components.

Use:
- Flowbite components
- Tailwind utilities
- Reusable template components

Ensure:
- Components follow the layout grid
- Spacing system remains consistent
- Responsive behavior matches the original design

---

# Implementation Principles

Follow these principles at all times:

1. Layout First
Never write UI components before defining the layout system.

2. Component Reuse
Avoid duplicate markup. Reuse components.

3. Flowbite Priority
Prefer Flowbite components whenever possible.

4. Consistent Spacing
All spacing must follow the defined spacing scale.

5. Responsive by Default
Layouts must adapt cleanly across mobile, tablet, and desktop.

---

# Output Expectations

The final frontend must provide:
- Clean Tailwind layout structure
- Flowbite UI components
- Componentized Flask templates
- Consistent design system
- Responsive grid layout
