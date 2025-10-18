# JskToolBox API Documentation

This directory contains the Sphinx-based API documentation for JskToolBox library.

## Structure

```
docs_api/
├── source/          # Documentation source files (RST)
│   ├── conf.py     # Sphinx configuration
│   ├── index.rst   # Main documentation index
│   └── modules/    # Module-specific documentation
├── build/          # Generated documentation
│   └── html/       # HTML output (open index.html)
├── Makefile        # Build commands for Unix/Linux
└── README.md       # This file
```

## Building Documentation

### Prerequisites

Install documentation dependencies:

```bash
poetry install
```

### Build HTML Documentation

From project root:

```bash
# Using convenience script
poetry run python generate_docs.py

# Using make (from project root)
make docs

# Using make (from docs_api directory)
cd docs_api
poetry run make html
```

### View Documentation

After building, open in browser:

```bash
# Linux
xdg-open build/html/index.html

# macOS
open build/html/index.html

# Windows
start build/html/index.html

# Or use make command from project root
make docs-open
```

## Documentation Features

- **Automatic API Reference**: Generated from docstrings
- **Type Hints**: Full type annotation support
- **Cross-references**: Links between modules and classes
- **Search**: Full-text search functionality
- **Module Index**: Alphabetical index of all modules
- **Source Code**: View source code from documentation

## Customization

### Configuration

Edit `source/conf.py` to customize:

- Theme and appearance
- Extensions
- Autodoc behavior
- Intersphinx mappings

### Adding New Modules

1. Create RST file in `source/modules/`
2. Add module to `source/index.rst` toctree
3. Rebuild documentation

Example module RST:

```rst
mymodule
========

.. automodule:: jsktoolbox.mymodule
   :members:
   :undoc-members:
   :show-inheritance:
```

## Troubleshooting

### Build Errors

If documentation build fails:

1. Check Python path in `source/conf.py`
2. Ensure all dependencies are installed
3. Verify module imports work
4. Check for docstring syntax errors

### Missing Modules

If modules don't appear:

1. Check module is imported correctly
2. Verify RST file syntax
3. Check exclude patterns in `conf.py`
4. Ensure module has docstrings

### Warnings

Warnings are usually related to:
- Malformed docstrings
- Missing cross-references
- Type hint issues

Most warnings don't prevent documentation generation.

## Clean Build

To remove generated files:

```bash
# From project root
make docs-clean

# From docs_api directory
poetry run make clean
```

## Alternative Formats

Sphinx can generate documentation in multiple formats:

```bash
cd docs_api

# PDF (requires LaTeX)
poetry run make latexpdf

# EPUB
poetry run make epub

# Plain text
poetry run make text
```

## For AI Agents

When working with this library, AI agents should:

1. **Generate docs first**: Run `poetry run python generate_docs.py`
2. **Check API structure**: Review `api_structure.json` in project root
3. **Browse HTML docs**: Open `build/html/index.html` for detailed API info
4. **Use examples**: See `EXAMPLES_FOR_AI.md` for usage patterns
5. **Check module index**: See `API_INDEX.md` for quick module reference

## CI/CD Integration

To integrate documentation generation in CI/CD:

```yaml
# Example GitHub Actions
- name: Generate Documentation
  run: |
    poetry install
    poetry run python generate_docs.py
    
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs_api/build/html
```

## Read the Docs

Configuration for Read the Docs is in `.readthedocs.yaml` in project root.

## Support

- **Repository**: https://github.com/Szumak75/JskToolBox
- **Issues**: Report documentation issues on GitHub
- **Sphinx Docs**: https://www.sphinx-doc.org/
