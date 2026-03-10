# Workflow Orchestration

## Planning Requirement

Before performing any non-trivial task, the agent must:

1. Enter plan mode
2. Identify which playbook applies
3. Load that playbook
4. Follow the steps sequentially

### 1. Plan Mode (Default for Non-Trivial Tasks)

Enter **plan mode** for any task involving:

-   3+ steps
-   architectural decisions
-   debugging or root cause analysis
-   refactoring
-   verification work

Rules:

-   Write a **clear execution plan before coding**.
-   If progress stalls or results diverge from expectations → **STOP and
    re-plan immediately**.
-   Plans must include **verification steps**, not only implementation.
-   Favor **detailed specs upfront** to eliminate ambiguity.

----

### 2. Subagent Strategy (Compute Scaling)

Use **subagents aggressively** to improve reasoning quality and keep the
main context window clean.

Guidelines:

-   Offload **research, exploration, analysis, and experimentation** to
    subagents.
-   Assign **one clearly defined task per subagent**.
-   Parallelize when possible.
-   Use subagents whenever the user request includes **"usesubagents"**.
-   Large or complex problems should **scale compute through multiple
    subagents**.

Goals:

-   Maintain **focus in the main agent**
-   Reduce **context pollution**
-   Increase **parallel reasoning depth**

----

### 3. Autonomous Execution

When a task is given:

-   **Act immediately** without requesting unnecessary guidance.
-   For bug reports:
    -   Identify failing tests, logs, stack traces, or errors.
    -   Diagnose root cause.
    -   Implement the fix.
    -   Verify resolution.

Never require the user to guide debugging steps.

Example expectations:

-   Fix failing CI tests autonomously.
-   Trace log errors to source code.
-   Resolve dependency or configuration issues independently.

----

### 4. Verification Before Completion

A task is **never complete without proof**.

Before marking work done:

-   Run tests
-   Check logs
-   Validate behavior
-   Compare behavior **before vs after changes**

Always ask:

> Would a senior staff engineer approve this change?

Verification methods:

-   test execution
-   behavior comparison
-   code diff inspection
-   functional validation

----

### 5. Elegant Solutions (Balanced Engineering)

For meaningful changes:

Pause and ask:

> "Is there a simpler or more elegant solution?"

Rules:

-   Avoid hacky patches.
-   Prefer **clean architecture over quick fixes**.
-   Implement the **best long-term solution once root cause is known**.

However:

-   Do **not over-engineer simple problems**.
-   Use the **simplest solution that fully solves the problem**.

----

### 6. Continuous Self-Improvement Loop

Every correction from the user must trigger **agent improvement**.

After receiving a correction:

1.  Update `tasks/lessons.md`
2.  Document:
    -   the mistake
    -   the correct pattern
    -   a rule preventing recurrence

Add a rule that prevents repeating the same error.

Mandatory behavior:

End correction handling with:

> "Update AGENTS.md so this mistake never happens again."

The goal is **progressively reducing mistake frequency across
sessions**.

----

### 7. AGENTS.md Evolution

AGENTS.md is a **living operational document**.

Maintenance rules:

-   Update it whenever repeated mistakes appear.
-   Continuously refine rules to improve agent behavior.
-   Remove weak or ambiguous instructions.
-   Strengthen rules that reduce error rates.

Goal:

> Iteratively optimize AGENTS.md until mistake rates measurably
> decrease.

----

## Task Management Protocol

### 1. Plan First

Write the execution plan in:

`tasks/todo.md`

Plans must contain:

-   checkable task items
-   implementation steps
-   verification steps

----

### 2. Confirm Plan

Before implementation begins:

-   validate the plan
-   ensure steps are clear and sufficient

----

### 3. Track Progress

During execution:

-   mark completed tasks in `tasks/todo.md`
-   update status continuously

----

### 4. Explain Changes

At each major step:

-   provide a **high-level summary**
-   explain **why the change was made**

----

### 5. Document Results

When a task completes:

Add a **review section** to `tasks/todo.md` including:

-   summary of solution
-   verification results
-   known limitations

----

### 6. Capture Lessons

If corrections occur:

Create a `task/lessons.md` file only if it does not exist. If a `task/lessons.md` already exists, update it with:
-   mistake description
-   root cause
-   preventative rule

----

## Project Knowledge Tracking

Maintain a **notes directory for each project or major task**.

Purpose:

-   persist insights
-   record architectural decisions
-   document debugging discoveries

Update notes:

-   after major tasks
-   after pull requests
-   after important fixes

AGENTS.md should reference this directory as a **knowledge base for
future work**.

----

## Core Engineering Principles

### Simplicity First

Always implement the **simplest solution that works correctly**.

Avoid:

-   unnecessary abstractions
-   premature optimization
-   complex refactors without benefit

----

### Root Cause Thinking

Never apply temporary fixes.

Always:

-   find the root cause
-   resolve the underlying issue
-   prevent recurrence

Temporary patches are unacceptable unless explicitly justified.

----

### Minimal Impact

Code changes must:

-   affect **only necessary components**
-   minimize risk of regressions
-   preserve existing behavior where possible

Prefer **surgical modifications over large rewrites**.

----

## Advanced Operational Rules

### Subagent Compute Scaling

If a task is complex:

-   spawn additional subagents
-   parallelize investigation
-   synthesize results

The main agent remains the **coordinator and integrator**.

----

### Context Window Management

Keep the main context focused by:

-   offloading large investigations
-   summarizing subagent outputs
-   storing knowledge in notes

Never allow the context window to become polluted with unnecessary
exploration.

----

### Security & Permission Checks

When permission requests appear:

-   route them through automated validation hooks
-   approve safe operations automatically
-   flag suspicious or potentially unsafe operations

This ensures **secure autonomous operation**.

## Frontend Framework Rules

All frontend UI must use:

- Tailwind CSS for styling
- Flowbite components for UI elements

### Styling rules
- Do NOT write custom CSS unless absolutely necessary.
- Prefer Tailwind utility classes.
- Use Flowbite components for:
  - Navbar
  - Cards
  - Forms
  - Buttons
  - Modals
  - Dropdowns
  - Alerts

### Template rules
- All UI must be written in Jinja templates inside:
  bloggr/templates/

- Static assets go in:
  bloggr/static/

### CSS build
Tailwind input:
bloggr/static/css/input.css

Tailwind output:
bloggr/static/css/output.css

Always ensure Tailwind scans:
bloggr/templates/**/*.html