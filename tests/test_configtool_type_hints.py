# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2025-02-14

Purpose: Validate lazy loading and type hints for configtool exports.
"""

import sys
import unittest
from typing import get_type_hints


class TestConfigToolLazyImports(unittest.TestCase):
    """Test type hints and lazy loading for configtool module."""

    def setUp(self) -> None:
        """Reset cached configtool modules before each test."""
        prefix = "jsktoolbox.configtool."
        to_purge = []
        for key in sys.modules:
            if key.startswith(prefix):
                to_purge.append(key)
        for key in to_purge:
            sys.modules.pop(key, None)
        sys.modules.pop("jsktoolbox.configtool", None)

    def test_01_lazy_loading_not_imported_initially(self) -> None:
        """Ensure submodules remain unloaded after package import."""
        import jsktoolbox.configtool

        self.assertNotIn("jsktoolbox.configtool.main", sys.modules)
        self.assertNotIn("jsktoolbox.configtool.libs.file", sys.modules)
        self.assertNotIn("jsktoolbox.configtool.libs.data", sys.modules)
        self.assertTrue(hasattr(jsktoolbox.configtool, "__all__"))

    def test_02_lazy_loading_triggers_on_access(self) -> None:
        """Verify accessing exports loads the matching submodule."""
        from jsktoolbox.configtool import Config

        self.assertEqual(Config.__name__, "Config")
        self.assertIn("jsktoolbox.configtool.main", sys.modules)

    def test_03_type_hints_available_for_config(self) -> None:
        """Check Config exposes type annotations via lazy import."""
        from jsktoolbox.configtool import Config

        init_hints = get_type_hints(Config.__init__)
        self.assertIn("filename", init_hints)
        self.assertIn("main_section_name", init_hints)
        self.assertIn("auto_create", init_hints)

    def test_04_all_exports_are_accessible(self) -> None:
        """Ensure every exported symbol resolves successfully."""
        import jsktoolbox.configtool as configtool

        for export_name in configtool.__all__:
            self.assertTrue(hasattr(configtool, export_name))
            value = getattr(configtool, export_name)
            self.assertIsNotNone(value)

    def test_05_type_hints_for_models(self) -> None:
        """Validate processor and model classes publish annotations."""
        from jsktoolbox.configtool import (
            DataProcessor,
            FileProcessor,
            SectionModel,
            VariableModel,
        )

        self.assertIn("section", get_type_hints(DataProcessor.set))
        self.assertTrue(hasattr(FileProcessor, "__init__"))
        self.assertTrue(hasattr(SectionModel, "set_variable"))
        self.assertTrue(hasattr(VariableModel, "parser"))


if __name__ == "__main__":
    unittest.main()
