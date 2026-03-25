# JskToolBox

JskToolBox provides curated sets of Python classes that support system automation, networking,
configuration handling, and Tkinter-based GUI development. The documentation in `docs/` offers
module-by-module guides; the sections below highlight the available references.

## Development Rules

The project uses Poetry for development workflows. Run project tools through `poetry run <command>`.

### Code Formatting and Class Layout

- Format Python code with `black` via `poetry run black .`
- Validate style with `poetry run pycodestyle`
- Use full type annotations for methods, properties, and class-level constants
- Prefer single quotes unless double quotes are required
- Organize each class into ordered sections separated by 80-character markers such as `# #[PUBLIC METHODS]####################################################################`

Required class section order:

1. `CONSTANTS`
2. `CONSTRUCTOR`
3. `PUBLIC PROPERTIES`
4. `PROTECTED PROPERTIES`
5. `PRIVATE PROPERTIES`
6. `PUBLIC METHODS`
7. `PROTECTED METHODS`
8. `PRIVATE METHODS`
9. `STATIC/CLASS METHODS`
10. `EOF` as the single final marker of the module file

Methods and properties inside each section must be sorted alphabetically.

### Versioning and Changelog

The project follows Semantic Versioning in `X.Y.Z` format.

- `MAJOR` for breaking API changes
- `MINOR` for backward-compatible features
- `PATCH` for fixes, small improvements, and refactoring
- Documentation-only changes do not require a version bump
- Code changes must update both `pyproject.toml` and `jsktoolbox/__init__.py`

Project history is tracked in [CHANGELOG.md](CHANGELOG.md). Changelog entries use the format `<type>: <subject>` with these types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

For `BData` dictionary keys, use `ReadOnlyClass` constants with the narrowest sensible scope:

- `__Keys` for a single class
- `_Keys` for a shared module scope
- public `NameKeys` classes for project-wide reuse in easy-to-find public keys modules

## Core Utilities

- **AttribTool** – base classes that restrict dynamic attribute creation and manage declared fields  
  [AttribTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/AttribTool.md)
- **BaseTool** – mixins for metadata reporting, data storage, logging, and threading used across the project  
  [BaseTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/BaseTool.md)
- **RaiseTool** – helpers that standardise exception formatting and error reporting  
  [RaiseTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/RaiseTool.md)
- **SystemTool** – utilities for interacting with the host operating system  
  [SystemTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/SystemTool.md)

## Configuration and Data

- **ConfigTool** – parsers and helpers for working with configuration files  
  [ConfigTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/ConfigTool.md)
- **DateTool** – date/time conversions, validation, and formatting helpers  
  [DateTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/DateTool.md)
- **StringTool** – routines for text manipulation and sanitising  
  [StringTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/StringTool.md)

## Logging and Networking

- **LogsTool** – components that assemble the project logging subsystem (queues, formatters, workers)  
  [LogsTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/LogsTool.md)
- **NetTool** – general-purpose classes for networking tasks  
  [NetTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetTool.md)
- **NetAddressTool** – toolkits for IP addressing with dedicated IPv4 and IPv6 guides  
  [NetAddressTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool.md)  
  [NetAddressTool IPv4 Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool4.md)  
  [NetAddressTool IPv6 Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/NetAddressTool6.md)

## Tkinter

- **TkTool** – Tk mixins, layout helpers, clipboard adapters, and reusable widgets (excluding the unreliable `_TkClip`)  
  [TkTool Readme](https://github.com/Szumak75/JskToolBox/blob/master/docs/TkTool.md)

## API Documentation

Complete API reference documentation is available:

- **Generate Documentation**: `make docs` or `poetry run python generate_docs.py`
- **HTML Documentation**: Open `docs_api/build/html/index.html` after generation
- **Preferred Imports**: [PREFERRED_IMPORTS.md](PREFERRED_IMPORTS.md) - Lazy import patterns
- **AI Agent Guide**: [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - Integration guide for AI agents
- **Code Examples**: [EXAMPLES_FOR_AI.md](EXAMPLES_FOR_AI.md) - Practical usage examples
- **Project Changelog**: [CHANGELOG.md](CHANGELOG.md) - Versioned history of project changes
- **Module Index**: [API_INDEX.md](API_INDEX.md) - Quick reference of all modules
- **API Structure**: `api_structure.json` - Machine-readable API structure

### Lazy Imports (Important)

The library uses lazy imports for performance. Use the preferred shorter patterns:

```python
# ✓ Preferred (lazy loading)
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient

# ✗ Avoid (works but longer)
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient
```

### Quick Start

```bash
# Install dependencies
poetry install

# Generate all documentation
make docs

# Or use the script directly
poetry run python generate_docs.py

# Open documentation in browser
make docs-open
```

## Examples

Examples demonstrating selected modules can be found in:
- [docs/examples](https://github.com/Szumak75/JskToolBox/tree/master/docs/examples) - Module examples
- [EXAMPLES_FOR_AI.md](EXAMPLES_FOR_AI.md) - Complete code examples
