# Repository Guidelines

## Project Structure & Module Organization
Focus code changes on `jsktoolbox/**/*.py` and companion tests in `tests/**/*.py`, mirroring the layout enforced by the Gemini configuration. Core toolsets live in modules like `datetool.py`, `raisetool.py`, and package directories (`logstool/`, `stringtool/`); shared helpers sit in `jsktoolbox/libs/`, and device adapters in `jsktoolbox/devices/`. Keep reusable scripts alongside peers, expose public APIs through `jsktoolbox/__init__.py`, document features in `docs/`, stash runnable snippets in `examples/`, and store automation assets in `tools/`.

## Build, Test, and Development Commands
Run `poetry install` to sync dependencies. Execute `poetry run pytest` for the test suite, which wraps unittest-style cases. Format with `poetry run black .`, lint using `poetry run pycodestyle jsktoolbox tests`, and build artifacts via `poetry build`. Execute additional utilities through `poetry run <command>` to ensure the venv is respected.

## Coding Style & Naming Conventions
Black governs formatting (4 spaces, 88 columns); prefer single quotes unless double quotes improve clarity. Name files and functions in snake_case, classes in PascalCase, and constants in upper snake. Every new public API requires explicit type hints and explicit imports. Docstrings and inline documentation stay in English and must follow the project template: summary line plus `### Arguments`, `### Returns`, and `### Raises` sections where relevant. Update any module-level `__all__` collections when adjusting exports.

## Testing Guidelines
Mirror module structure when adding `test_*.py` files under `tests/`. Extend existing `unittest.TestCase` subclasses or fixtures instead of duplicating setup. Choose descriptive names such as `test_timestamp_handles_leap_second`, cover both happy paths and edge cases, and add regression tests for every fixed bug. Run `poetry run pytest` before review and share results when opening a PR.

## Commit & Pull Request Guidelines
Follow the established style: concise sentence-case summaries mentioning affected modules (e.g., `Refactor Timestamp class in datetool.py and add test cases in test_datetool.py`). Group related changes per commit to aid review. Pull requests should outline motivation, list key updates, link tracking issues, and include logs or screenshots when behaviour changes. Confirm CI status or paste the latest `poetry run pytest` output in the description.

## Documentation & Examples
Repository comments and docs stay in English even though day-to-day communication may be Polish. Update or add guides in `docs/` for new capabilities and contribute runnable examples in `examples/` that show canonical imports. Ensure Markdown adheres to the provided template and cross-link from the README or tool-specific guides to keep navigation tidy.

## Error Handling
Surface exceptions through `raisetool.Raise.error(message, exception_type, class_name, frame)` so stack context and formatting remain consistent across tool modules.
