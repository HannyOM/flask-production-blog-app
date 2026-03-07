# Agent Guidelines for flask-production-blog-app

## Project Overview
- **Type**: Flask web application (blog)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Testing**: pytest with testcontainers (Docker-based PostgreSQL)
- **Authentication**: Flask-Security with roles-based access control

## Build, Lint, and Test Commands

### Running Tests

Run all tests:
```bash
pytest
```

Run a single test file:
```bash
pytest tests/test_blog.py
```

Run a single test function:
```bash
pytest tests/test_blog.py::test_index
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests matching a pattern:
```bash
pytest -k "test_login"
```

### Development Server

Run the Flask app:
```bash
flask run
# or
python wsgi.py
```

Run in debug mode:
```bash
export DEBUG=1 && flask run
```

### Database Migrations

Create a migration:
```bash
flask db migrate -m "migration message"
```

Apply migrations:
```bash
flask db upgrade
```

Rollback:
```bash
flask db downgrade
```

---

## Code Style Guidelines

### Imports
Organize imports in the following order (separate groups with blank lines):
1. Standard library (`os`, `datetime`, `typing`)
2. Third-party packages (`flask`, `sqlalchemy`)
3. Local application modules (`from .models import ...`)

```python
# Standard library
from datetime import datetime
from typing import List

# Third-party
from flask import Blueprint, render_template
from flask_security.core import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local
from . import db
from .models import Post
```

### Type Annotations
- Use SQLAlchemy's `Mapped` and `mapped_column` for type-safe column definitions
- Use `| None` syntax for nullable types (Python 3.10+)
- Add `# type: ignore` comments for SQLAlchemy ORM attributes where needed
- Use explicit type hints for all function parameters and return values

```python
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(50), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(db.Date, nullable=False)
```

### Naming Conventions
- **Variables/functions**: snake_case (`create_app`, `all_posts`)
- **Classes**: PascalCase (`User`, `Role`, `Post`)
- **Constants**: UPPER_SNAKE_CASE
- **Database tables**: singular, lowercase (`user`, `role`, `post`)
- **Blueprint names**: snake_case (`bp = Blueprint("blog", __name__)`)

### Formatting
- Use **double quotes** for strings
- Maximum line length: 100 characters (soft guideline)
- Use blank lines sparingly to separate logical sections
- Align assignments with spaces after `=`

```python
# Good
app.config.from_mapping(
    DEBUG = os.environ.get("DEBUG") == "1",
    SECRET_KEY = os.environ.get("SECRET_KEY"),
)

# Avoid
app.config.from_mapping({
    'DEBUG': os.environ.get("DEBUG") == "1",
})
```

### Error Handling
- Use Flask's `abort()` for HTTP errors (e.g., `abort(403)`)
- Use `flash()` for user-facing error messages
- Validate form inputs early and return errors inline

```python
if not title:
    error = "Title is required."
    return render_template("blog/new.html", error_msg=error)
```

### Routes/Views
- Use `@bp.route()` decorator pattern
- Place `@auth_required()` and role decorators above route decorators
- Use descriptive endpoint names matching blueprint name (`url_for("blog.index")`)

```python
@bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
@auth_required()
def edit(post_id):
    # ...
```

### Database Operations
- Use `db.session.commit()` after `db.session.add()` or modifications
- Use `db.get_or_404(Model, id)` for 404 handling on lookups
- Use `filter_by()` for simple filters, `filter()` for complex queries

```python
# Simple lookup with 404
post = db.get_or_404(Post, post_id)

# Query with filter
post = Post.query.filter_by(id=post_id).first()
```

### Testing Conventions
- Test files: `test_*.py` in `tests/` directory
- Use fixtures from `conftest.py` for common setup (`client`, `app`, `db`, `auth`)
- Use `@pytest.mark.parametrize` for testing multiple inputs
- Use `with app.app_context()` when accessing database in tests
- Test client returns follow redirects with `follow_redirects=True`

```python
def test_add_post(client, create_user, auth, app):
    auth.login()
    response = client.get("/new")
    assert response.status_code == 200

    client.post("/add", data={"post_title": "Title", "post_content": "Content"})
    with app.app_context():
        count = Post.query.count()
        assert count == 1
```

### Security
- Never commit secrets to version control (use `.env` files)
- Use environment variables for configuration (`os.environ.get()`)
- Enable CSRF protection in forms (Flask-WTF handles this)
- Use proper password hashing (Flask-Security provides this)

### File Organization
```
bloggr/
  __init__.py      # App factory, extensions, blueprint registration
  models.py        # SQLAlchemy models (User, Role, Post)
  blog.py          # Blueprint with routes
  roles.py         # Role initialization signals
  templates/       # Jinja2 templates
  static/         # CSS, JS, images
```

---

## Common Patterns

### Application Factory
```python
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(...)
    
    if test_config is not None:
        app.config.update(test_config)
    
    db.init_app(app)
    # ... initialize other extensions
    
    return app
```

### Model with Relationships
```python
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[List[Post]] = relationship(backref="author", lazy=True)
```

### Using Test Fixtures
```python
def test_something(client, app, db, create_user, auth):
    # client: test client for HTTP requests
    # app: Flask application instance
    # db: database instance
    # create_user: creates and returns a test user
    # auth: helper for login/logout
```

---

## Notes for Agents
- This project uses Docker testcontainers for PostgreSQL during testing
- The test database is created/destroyed for each test session
- Flask-Security handles authentication, roles, and password hashing
- The app uses Blueprint-based architecture for modularity


## Workflow Orchestration

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

------------------------------------------------------------------------

### 2. Subagent Strategy (Compute Scaling)

Use **subagents aggressively** to improve reasoning quality and keep the
main context window clean.

Guidelines:

-   Offload **research, exploration, analysis, and experimentation** to
    subagents.
-   Assign **one clearly defined task per subagent**.
-   Parallelize when possible.
-   Use subagents whenever the user request includes **"use
    subagents"**.
-   Large or complex problems should **scale compute through multiple
    subagents**.

Goals:

-   Maintain **focus in the main agent**
-   Reduce **context pollution**
-   Increase **parallel reasoning depth**

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

## Task Management Protocol

### 1. Plan First

Write the execution plan in:

`tasks/todo.md`

Plans must contain:

-   checkable task items
-   implementation steps
-   verification steps

------------------------------------------------------------------------

### 2. Confirm Plan

Before implementation begins:

-   validate the plan
-   ensure steps are clear and sufficient

------------------------------------------------------------------------

### 3. Track Progress

During execution:

-   mark completed tasks in `tasks/todo.md`
-   update status continuously

------------------------------------------------------------------------

### 4. Explain Changes

At each major step:

-   provide a **high-level summary**
-   explain **why the change was made**

------------------------------------------------------------------------

### 5. Document Results

When a task completes:

Add a **review section** to `tasks/todo.md` including:

-   summary of solution
-   verification results
-   known limitations

------------------------------------------------------------------------

### 6. Capture Lessons

If corrections occur:

Update:

`tasks/lessons.md`

Include:

-   mistake description
-   root cause
-   preventative rule

------------------------------------------------------------------------

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

------------------------------------------------------------------------

## Core Engineering Principles

### Simplicity First

Always implement the **simplest solution that works correctly**.

Avoid:

-   unnecessary abstractions
-   premature optimization
-   complex refactors without benefit

------------------------------------------------------------------------

### Root Cause Thinking

Never apply temporary fixes.

Always:

-   find the root cause
-   resolve the underlying issue
-   prevent recurrence

Temporary patches are unacceptable unless explicitly justified.

------------------------------------------------------------------------

### Minimal Impact

Code changes must:

-   affect **only necessary components**
-   minimize risk of regressions
-   preserve existing behavior where possible

Prefer **surgical modifications over large rewrites**.

------------------------------------------------------------------------

## Advanced Operational Rules

### Subagent Compute Scaling

If a task is complex:

-   spawn additional subagents
-   parallelize investigation
-   synthesize results

The main agent remains the **coordinator and integrator**.

------------------------------------------------------------------------

### Context Window Management

Keep the main context focused by:

-   offloading large investigations
-   summarizing subagent outputs
-   storing knowledge in notes

Never allow the context window to become polluted with unnecessary
exploration.

------------------------------------------------------------------------

### Security & Permission Checks

When permission requests appear:

-   route them through automated validation hooks
-   approve safe operations automatically
-   flag suspicious or potentially unsafe operations

This ensures **secure autonomous operation**.
