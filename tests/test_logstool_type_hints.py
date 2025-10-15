# -*- coding: utf-8 -*-
"""
test_logstool_type_hints.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2025-10-15

Purpose: Verify that TYPE_CHECKING provides proper type hints while maintaining
         lazy loading behavior in logstool module.
"""

import sys
import unittest
from typing import get_type_hints


class TestLogsToolTypeHints(unittest.TestCase):
    """Test type hints and lazy loading for logstool module."""

    def test_01_lazy_loading_not_imported_initially(self) -> None:
        """Verify submodules are not loaded on package import."""
        # Clean up any previous imports
        modules_to_remove = [
            key for key in sys.modules.keys() 
            if key.startswith('jsktoolbox.logstool') and key != 'jsktoolbox.logstool'
        ]
        for mod in modules_to_remove:
            del sys.modules[mod]
        
        # Import the package
        import jsktoolbox.logstool
        
        # Verify submodules are NOT loaded
        self.assertNotIn('jsktoolbox.logstool.logs', sys.modules)
        self.assertNotIn('jsktoolbox.logstool.engines', sys.modules)
        self.assertNotIn('jsktoolbox.logstool.formatters', sys.modules)
        self.assertNotIn('jsktoolbox.logstool.queue', sys.modules)
        self.assertNotIn('jsktoolbox.logstool.keys', sys.modules)

    def test_02_lazy_loading_triggers_on_access(self) -> None:
        """Verify accessing an attribute triggers lazy loading."""
        from jsktoolbox.logstool import LoggerClient
        
        # Now the logs module should be loaded
        self.assertIn('jsktoolbox.logstool.logs', sys.modules)
        
        # Verify we got the actual class
        self.assertEqual(LoggerClient.__name__, 'LoggerClient')
        self.assertTrue(hasattr(LoggerClient, '__init__'))
        self.assertTrue(hasattr(LoggerClient, 'message'))

    def test_03_type_hints_available_for_logger_client(self) -> None:
        """Verify LoggerClient has proper type hints."""
        from jsktoolbox.logstool import LoggerClient
        
        # Check __init__ signature
        init_hints = get_type_hints(LoggerClient.__init__)
        self.assertIn('queue', init_hints)
        self.assertIn('name', init_hints)
        
        # Check message method signature
        message_hints = get_type_hints(LoggerClient.message)
        self.assertIn('message', message_hints)
        self.assertIn('log_level', message_hints)

    def test_04_type_hints_available_for_logger_engine(self) -> None:
        """Verify LoggerEngine has proper type hints."""
        from jsktoolbox.logstool import LoggerEngine
        
        # Check add_engine method signature
        add_engine_hints = get_type_hints(LoggerEngine.add_engine)
        self.assertIn('log_level', add_engine_hints)
        self.assertIn('engine', add_engine_hints)

    def test_05_type_hints_available_for_engines(self) -> None:
        """Verify engine classes have proper type hints."""
        from jsktoolbox.logstool import (
            LoggerEngineStdout,
            LoggerEngineStderr,
            LoggerEngineFile,
            LoggerEngineSyslog,
        )
        
        # Check each engine has __init__ with proper signature
        for engine_class in [
            LoggerEngineStdout,
            LoggerEngineStderr,
            LoggerEngineFile,
            LoggerEngineSyslog,
        ]:
            init_hints = get_type_hints(engine_class.__init__)
            self.assertIn('name', init_hints)
            self.assertIn('formatter', init_hints)
            self.assertIn('buffered', init_hints)

    def test_06_type_hints_available_for_formatters(self) -> None:
        """Verify formatter classes have proper type hints."""
        from jsktoolbox.logstool import (
            LogFormatterNull,
            LogFormatterDateTime,
            LogFormatterTime,
            LogFormatterTimestamp,
        )
        
        # Check each formatter exists and is a class
        for formatter_class in [
            LogFormatterNull,
            LogFormatterDateTime,
            LogFormatterTime,
            LogFormatterTimestamp,
        ]:
            self.assertTrue(isinstance(formatter_class, type))
            self.assertTrue(hasattr(formatter_class, '__init__'))

    def test_07_type_hints_available_for_keys(self) -> None:
        """Verify key classes are accessible."""
        from jsktoolbox.logstool import (
            LogKeys,
            LogsLevelKeys,
            SysLogKeys,
        )
        
        # Verify key classes have expected attributes
        self.assertTrue(hasattr(LogsLevelKeys, 'INFO'))
        self.assertTrue(hasattr(LogsLevelKeys, 'ERROR'))
        self.assertTrue(hasattr(LogsLevelKeys, 'DEBUG'))
        
        self.assertTrue(hasattr(LogKeys, 'QUEUE'))
        self.assertTrue(hasattr(LogKeys, 'NAME'))
        
        self.assertTrue(hasattr(SysLogKeys, 'level'))
        self.assertTrue(hasattr(SysLogKeys, 'facility'))

    def test_08_all_exports_are_accessible(self) -> None:
        """Verify all __all__ exports are accessible."""
        from jsktoolbox import logstool
        
        # Get __all__ list
        all_exports = logstool.__all__
        
        # Verify we can access each export
        for export_name in all_exports:
            self.assertTrue(
                hasattr(logstool, export_name),
                f"Export '{export_name}' not accessible"
            )
            
            # Access it to trigger lazy loading
            export_value = getattr(logstool, export_name)
            self.assertIsNotNone(export_value)

    def test_09_docstrings_are_preserved(self) -> None:
        """Verify docstrings are accessible through lazy loading."""
        from jsktoolbox.logstool import LoggerClient, LoggerEngine
        
        # Check class docstrings
        self.assertIsNotNone(LoggerClient.__doc__)
        self.assertIn("Logger Client", LoggerClient.__doc__)
        
        self.assertIsNotNone(LoggerEngine.__doc__)
        self.assertIn("LoggerEngine", LoggerEngine.__doc__)
        
        # Check method docstrings
        self.assertIsNotNone(LoggerClient.message.__doc__)
        self.assertIn("message", LoggerClient.message.__doc__.lower())


if __name__ == '__main__':
    unittest.main()


# #[EOF]#######################################################################
