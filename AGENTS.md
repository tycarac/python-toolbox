# AI Agent Instructions (AGENTS.md)

This file contains operational instructions for AI coding assistants interacting with this project and repository.

## Project overview

Read the project documentation:

- [README.md](README.md)
- [Architecture](doc/architecture.md)
- [Development](doc/development.md)
- [Data Model](doc/data-model.md)

Do not duplicate architecture descriptions, designs, or decisions in this document.

## Build Environment and Dependency Management

- Use `uv` for all dependency and project management.
    - Use `uv add <package>` (or `uv add --dev <package>` for development tools).
    - Always prefix execution commands with `uv run` to ensure they run in the correct isolated environment (e.g.,
      `uv run flask run`, `uv run pytest`).
- Do not use `pip install`, `pip freeze`, or `virtualenv` directly.

## Code Style and Linting

- Using Python:
    - Use modern Python syntax and best coding practices for Python target release.
    - Make use of newest language features and library functions.
    - Use of type hinting for all function, variable, and parameter declarations.
    - Remove any compatibility code needed for older Python releases.
    - Always ensure commands are run within the active virtual environment.

- Formatter/Linter:
    - Use `ruff` from with `uv`.
- **Type Checking:** We use `mypy` for strict type checking.
- **Rules:**
    - All new functions and methods MUST have complete type hints.
    - All new files MUST include docstrings for classes and complex functions.
    - **Before completing any task, you MUST run:**
        - `ruff check . --fix`
        - `ruff format .`
        - `mypy .`

- Formatting/Linting:
    - Before completing any task, run commands:
        - `uv run ruff check . --fix`
        - `uv run ruff format .`

## Testing and Debugging

- Unit and Regression testing:
    - Use framework: `pytest`.
        - Write regression tests when fixing bugs and issues.
        - Maintain all tests self-contained in the `tests/` directory.
- Running Tests:
    - To run the full suite: `uv run pytest`
    - When debugging a specific Flask route, use the Flask test client fixture.
    - Mock DuckDB using an in-memory database (`duckdb.connect(':memory:')`) for isolated unit tests instead of writing
      to the disk.

## 3. Database Constraints (DuckDB)

- **Connection Handling:** Abstract all DuckDB connections into a dedicated `db.py` or `database/` module. Do not open
  connections directly inside Flask route definitions.
- **Query Execution:** Use parameterized queries (e.g., `db.execute("SELECT * FROM table WHERE id = ?", [id])`) to
  prevent SQL injection.
- **File Management:** DuckDB creates local database files (e.g., `app.duckdb`, `app.duckdb.wal`). **Never** track or
  commit these database files or their Write-Ahead Logs to version control.
- **Data Processing:** DuckDB is highly optimized for analytical queries. Push filtering, joining, and aggregation down
  to the DuckDB SQL layer rather than processing raw data structures in standard Python.

## 4. Flask Architectural Constraints

- **Routing:** Use Flask Blueprints for routing if the application grows beyond a single `app.py` file. Keep route
  functions lean.
- **Separation of Concerns:**
    - **Routes:** Handle HTTP requests, form validation, and return JSON/HTML.
    - **Services/Queries:** Perform the actual DuckDB queries and business logic.
- **Templates & Static Files:**
    - HTML files must go in the `templates/` directory.
    - CSS/JS files must go in the `static/` directory.

## Execution Workflow

When assigned a task, follow this exact sequence:

1. Search the codebase to understand existing Blueprint routing and DuckDB query patterns.
2. Write the code, strictly keeping database queries out of the Flask route definitions.
3. Write an accompanying test using the in-memory DuckDB fixture.
4. Run `uv run ruff check . --fix` and `uv run ruff format .`.
5. Run `uv run pytest` to ensure nothing is broken.

## 3. Code Style & Linting

- **Formatter/Linter:** We use `ruff`.
- **Type Checking:** We use `mypy` for strict type checking.
- **Rules:**
    - All new functions and methods MUST have complete type hints.
    - All new files MUST include docstrings for classes and complex functions.
    - **Before completing any task, you MUST run:**
        - `ruff check . --fix`
        - `ruff format .`
        - `mypy .`

## 5. Architectural Constraints

- **Routing:** API endpoints live in `api/routes/`. Do NOT put business logic here.
- **Business Logic:** Put all business logic in `services/`.
- **Database:** Database models live in `db/models.py`. Only the `services/` layer is allowed to directly interact with
  the database session.
- **Immutability:** Do not modify the `migrations/` or `.github/` directories unless explicitly instructed.

## 6. Execution Workflow

When assigned a task, follow this exact sequence:

1. Search the codebase to understand existing patterns (especially in `services/` and `tests/`).
2. Write the code, adhering to the architectural constraints.
3. Write the accompanying test.
4. Run the formatting, linting, and type-checking commands.
5. Run the test suite to ensure nothing is broken.

## Validation

- After modifying Python code run:
    - uv run pytest uv run ruff check . uv run ty check
- After modifying SQL also run:
    - uv run pytest tests/database

## Database rules

- Read `doc/data-model.md` before modifying database code.
- Schema definitions in `src/sql/` are authoritative.
- Do not reproduce DuckDB table definitions in Python.

## General constraints

- Do not change public APIs unless the task requires it.
- Do not silently weaken database constraints.
- Do not introduce a new dependency when the standard library or an existing dependency provides the required
  functionality.
- Preserve existing type annotations.
- Add regression tests for bug fixes.

