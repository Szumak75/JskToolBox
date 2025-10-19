#!/usr/bin/env python3
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2025-10-18

Purpose: Generate API documentation for JskToolBox library.

This script generates both HTML documentation using Sphinx and
a JSON file containing API information suitable for AI agents.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any


def generate_html_docs() -> bool:
    """Generate HTML documentation using Sphinx.

    ### Returns:
    bool - True if successful, False otherwise.
    """
    docs_dir = Path(__file__).parent / "docs_api"

    print("Generating HTML documentation...")
    try:
        result = subprocess.run(
            ["poetry", "run", "make", "html"],
            cwd=docs_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        print("✓ HTML documentation generated successfully")
        print(f"  Output: {docs_dir / 'build' / 'html' / 'index.html'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating HTML documentation: {e}")
        print(f"  stdout: {e.stdout}")
        print(f"  stderr: {e.stderr}")
        return False


def extract_module_info(module_path: str) -> Dict[str, Any]:
    """Extract basic information from a Python module.

    ### Arguments:
    * module_path: str - Path to the module file.

    ### Returns:
    Dict[str, Any] - Dictionary containing module information.
    """
    info = {"path": module_path, "docstring": None, "classes": [], "functions": []}

    try:
        with open(module_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract module docstring
        if content.startswith('"""') or content.startswith("'''"):
            quote = '"""' if content.startswith('"""') else "'''"
            end = content.find(quote, 3)
            if end != -1:
                info["docstring"] = content[3:end].strip()

    except Exception as e:
        print(f"  Warning: Could not parse {module_path}: {e}")

    return info


def generate_api_json() -> bool:
    """Generate JSON file with API structure for AI agents.

    ### Returns:
    bool - True if successful, False otherwise.
    """
    print("\nGenerating API JSON for AI agents...")

    base_path = Path(__file__).parent / "jsktoolbox"
    api_structure = {
        "name": "JskToolBox",
        "version": "1.2.dev",
        "description": "Small sets of classes for various operations.",
        "repository": "https://github.com/Szumak75/JskToolBox",
        "modules": {},
    }

    # Scan all Python files
    for py_file in base_path.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue

        rel_path = py_file.relative_to(base_path.parent)
        module_name = str(rel_path).replace("/", ".").replace("\\", ".")[:-3]

        if module_name.endswith(".__init__"):
            module_name = module_name[:-9]

        info = extract_module_info(str(py_file))
        api_structure["modules"][module_name] = info

    # Save to JSON
    output_file = Path(__file__).parent / "api_structure.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(api_structure, f, indent=2, ensure_ascii=False)
        print(f"✓ API JSON generated: {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error generating API JSON: {e}")
        return False


def generate_markdown_index() -> bool:
    """Generate Markdown index of all modules.

    ### Returns:
    bool - True if successful, False otherwise.
    """
    print("\nGenerating Markdown API index...")

    base_path = Path(__file__).parent / "jsktoolbox"
    output_file = Path(__file__).parent / "API_INDEX.md"

    modules_by_package = {}

    # Group modules by package
    for py_file in sorted(base_path.rglob("*.py")):
        if "__pycache__" in str(py_file):
            continue

        rel_path = py_file.relative_to(base_path.parent)
        module_name = str(rel_path).replace("/", ".").replace("\\", ".")[:-3]

        package = module_name.split(".")[1] if "." in module_name else "root"

        if package not in modules_by_package:
            modules_by_package[package] = []
        modules_by_package[package].append(module_name)

    # Generate markdown
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# JskToolBox API Index\n\n")
            f.write("Complete index of all modules in JskToolBox library.\n\n")
            f.write("## Installation\n\n")
            f.write("```bash\n")
            f.write("pip install jsktoolbox\n")
            f.write("```\n\n")
            f.write("## Available Packages\n\n")

            for package in sorted(modules_by_package.keys()):
                f.write(f"### {package}\n\n")
                for module in sorted(modules_by_package[package]):
                    # Convert to import statement
                    import_stmt = module.replace("jsktoolbox.", "from jsktoolbox.")
                    if "." in import_stmt.replace("from jsktoolbox.", ""):
                        parts = import_stmt.rsplit(".", 1)
                        import_stmt = f"{parts[0]} import {parts[1]}"
                    else:
                        import_stmt = f"import {module}"

                    f.write(f"- `{module}`\n")
                    f.write(f"  ```python\n")
                    f.write(f"  {import_stmt}\n")
                    f.write(f"  ```\n\n")

            f.write("\n## Documentation\n\n")
            f.write(
                "Full API documentation is available in `docs_api/build/html/index.html`\n\n"
            )
            f.write("Generate documentation:\n")
            f.write("```bash\n")
            f.write("poetry run python generate_docs.py\n")
            f.write("```\n")

        print(f"✓ Markdown index generated: {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error generating Markdown index: {e}")
        return False


def main():
    """Main function to generate all documentation."""
    print("=" * 60)
    print("JskToolBox Documentation Generator")
    print("=" * 60)

    results = []

    # Generate HTML docs
    results.append(("HTML Documentation", generate_html_docs()))

    # Generate API JSON
    results.append(("API JSON", generate_api_json()))

    # Generate Markdown index
    results.append(("Markdown Index", generate_markdown_index()))

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    for name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {name}")

    # Exit code
    all_success = all(success for _, success in results)
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
