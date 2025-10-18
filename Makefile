.PHONY: help docs docs-clean docs-open test lint format install

help:
	@echo "JskToolBox Development Commands"
	@echo "================================"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs       - Generate all documentation (HTML, JSON, Markdown)"
	@echo "  make docs-clean - Clean generated documentation"
	@echo "  make docs-open  - Generate and open HTML documentation in browser"
	@echo ""
	@echo "Development:"
	@echo "  make install    - Install project dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters (pycodestyle)"
	@echo "  make format     - Format code with black"
	@echo ""

docs:
	@echo "Generating documentation..."
	poetry run python generate_docs.py

docs-clean:
	@echo "Cleaning documentation..."
	rm -rf docs_api/build
	rm -f api_structure.json
	rm -f API_INDEX.md

docs-open: docs
	@echo "Opening documentation in browser..."
	@python -m webbrowser docs_api/build/html/index.html || xdg-open docs_api/build/html/index.html || open docs_api/build/html/index.html

test:
	@echo "Running tests..."
	poetry run pytest

lint:
	@echo "Running linters..."
	poetry run pycodestyle jsktoolbox/
	poetry run pydocstyle jsktoolbox/

format:
	@echo "Formatting code..."
	poetry run black .

install:
	@echo "Installing dependencies..."
	poetry install
