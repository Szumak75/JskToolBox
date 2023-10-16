# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 16.10.2023

  Purpose: Stringtool testing class.
"""

import unittest
from jsktoolbox.stringtool.crypto import SimpleCrypto


class TestStringtool(unittest.TestCase):
    """TestStringtool testing class."""

    def test_01_create_object(self) -> None:
        """Test nr 01."""
        try:
            SimpleCrypto()
        except Exception as ex:
            self.fail(f"Unexpected exception was thrown: '{ex}'")

    def test_02_salt_generator(self) -> None:
        """Test nr 02."""
        self.assertIsInstance(SimpleCrypto.salt_generator(), int)

    def test_03_salt_generator_length(self) -> None:
        """Test nr 03."""
        x_len: int = 100
        self.assertEqual(len(str(SimpleCrypto.salt_generator(x_len))), x_len)

    def test_04_salt_generator_values(self) -> None:
        """Test nr 04."""
        x_len: int = 6
        for _ in range(0, 1000):
            self.assertTrue(
                SimpleCrypto.salt_generator(x_len) in range(100000, 1000000)
            )


# #[EOF]#######################################################################
