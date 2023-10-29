# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 16.10.2023

  Purpose: simple class for basic cryptographics procedures for strings.
"""

import string
from typing import Dict

from base64 import b64decode, b64encode
from codecs import getencoder
from inspect import currentframe
from random import randrange

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_xor_process.htm
# https://teachen.info/cspp/unit4/lab04-02.html


class SimpleCrypto(NoDynamicAttributes):
    """SimpleCrypto class."""

    @staticmethod
    def chars_table_generator() -> str:
        """Return printable chars list."""
        return string.printable + "ĄĆĘŁŃÓŚŻŹąćęłńóśżź"

    @classmethod
    def salt_generator(cls, length: int = 8) -> int:
        """Method for generate random salt with specific length."""
        if length < 1:
            raise Raise.error(
                f"...{length}",
                ValueError,
                cls.__qualname__,
                currentframe(),
            )
        return randrange(int(10**length / 10), 10**length - 1)

    @classmethod
    def caesar_encrypt(cls, salt: int, message: str) -> str:
        """Caesar encoder method with chars translate table."""
        chars: str = cls.chars_table_generator()
        chars_len: int = len(chars)
        shift: int = salt % chars_len
        transtable: Dict = str.maketrans(chars, chars[shift:] + chars[:shift])

        return message.translate(transtable)

    @classmethod
    def caesar_decrypt(cls, salt: int, message: str) -> str:
        """Caesar decoder method with chars translate table."""
        chars: str = cls.chars_table_generator()
        chars_len: int = len(chars)
        shift: int = chars_len - (salt % chars_len)
        transtable: Dict = str.maketrans(chars, chars[shift:] + chars[:shift])

        return message.translate(transtable)

    @classmethod
    def rot13_codec(cls, message: str) -> str:
        """Rot13 encoder/decoder method."""
        codec = lambda s: getencoder("rot13")(s)[0]
        return codec(message)

    @classmethod
    def b64_encrypt(cls, message: str) -> str:
        """Base64 encoder method."""
        return b64encode(message.encode("UTF-32")).decode()

    @classmethod
    def b64_decrypt(cls, message: str) -> str:
        """Base64 decoder method."""
        # return cls.rot13_codec(b64decode(cls.rot13_codec(message)).decode())
        return b64decode(message.encode("UTF-32")).decode("UTF-32")

    @classmethod
    def multiple_encrypt(cls, salt: int, message: str) -> str:
        """Multiple encoder method."""
        return cls.b64_encrypt(cls.caesar_encrypt(salt, cls.rot13_codec(message)))

    @classmethod
    def multiple_decrypt(cls, salt: int, message: str) -> str:
        """Multiple decoder method."""
        return cls.rot13_codec(cls.caesar_decrypt(salt, cls.b64_decrypt(message)))


# #[EOF]#######################################################################
