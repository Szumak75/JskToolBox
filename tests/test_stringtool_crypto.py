# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 16.10.2023

Purpose: Stringtool testing class.
"""

import unittest
from jsktoolbox.stringtool.crypto import SimpleCrypto


class TestStringtoolCrypto(unittest.TestCase):
    """TestStringtoolCrypto testing class."""

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

    def test_05_rot13_codec(self) -> None:
        """Test rn 05."""
        message: str = "This is example text: ąśżćń"
        self.assertEqual(
            SimpleCrypto.rot13_codec(SimpleCrypto.rot13_codec(message)),
            message,
        )

    def test_06_b64_codec(self) -> None:
        """Test nr 06."""
        message: str = "This is example text: ąśżćń"
        self.assertEqual(
            SimpleCrypto.b64_decrypt(SimpleCrypto.b64_encrypt(message)),
            message,
        )

    def test_07_caesar(self) -> None:
        """Test nr 07."""
        message: str = "This is example text: ąśżćń"
        salt: int = SimpleCrypto.salt_generator(6)
        self.assertEqual(
            SimpleCrypto.caesar_decrypt(
                salt, SimpleCrypto.caesar_encrypt(salt, message)
            ),
            message,
        )

    def test_08_multiple(self) -> None:
        """Test nr 08."""
        message: str = "This is example text: ĄŻŹĆŚŁÓŃĘąśżćń"
        for _ in range(0, 1000):
            salt: int = SimpleCrypto.salt_generator(12)
            self.assertEqual(
                SimpleCrypto.multiple_decrypt(
                    salt, SimpleCrypto.multiple_encrypt(salt, message)
                ),
                message,
            )

    def test_09_b64_accepts_standard_payload(self) -> None:
        """Test nr 09."""
        self.assertEqual(SimpleCrypto.b64_decrypt("dGVzdA=="), "test")

    def test_10_b64_invalid_payload(self) -> None:
        """Test nr 10."""
        with self.assertRaisesRegex(ValueError, "Invalid Base64 payload."):
            SimpleCrypto.b64_decrypt("not-base64!")

    def test_11_chars_table_includes_extended_alphabets(self) -> None:
        """Test nr 11."""
        table: str = SimpleCrypto.chars_table_generator()
        self.assertIn('Ω', table)
        self.assertIn('Ж', table)
        self.assertIn('ي', table)

    def test_12_chars_table_has_unique_characters(self) -> None:
        """Test nr 12."""
        table: str = SimpleCrypto.chars_table_generator()
        self.assertEqual(len(table), len(set(table)))

    def test_13_caesar_handles_greek_characters(self) -> None:
        """Test nr 13."""
        message: str = "Τεστ Κρυπτο"
        salt: int = SimpleCrypto.salt_generator(4)
        encoded = SimpleCrypto.caesar_encrypt(salt, message)
        self.assertEqual(SimpleCrypto.caesar_decrypt(salt, encoded), message)

    def test_14_salt_generator_invalid_length(self) -> None:
        """Test nr 14."""
        with self.assertRaises(ValueError):
            SimpleCrypto.salt_generator(0)

    def test_15_rot13_codec_invalid_type(self) -> None:
        """Test nr 15."""
        with self.assertRaises(TypeError):
            SimpleCrypto.rot13_codec(123)  # type: ignore[arg-type]


# #[EOF]#######################################################################
