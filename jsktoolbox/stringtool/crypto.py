# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 16.10.2023

  Purpose: simple class for basic cryptographics procedures for strings.
"""

from base64 import b64decode, b64encode
from codecs import getencoder
from inspect import currentframe
from random import randrange

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_xor_process.htm


class SimpleCrypto(NoDynamicAttributes):
    """SimpleCrypto class."""

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
    def rot13_codec(cls, message: str) -> str:
        """Rot13 encoder/decoder method."""
        codec = lambda s: getencoder("rot13")(s)[0]
        return codec(message)

    @classmethod
    def b64_encode(cls, message: str) -> str:
        """Base64 encoder method with rot13."""
        return cls.rot13_codec(
            b64encode(cls.rot13_codec(message).encode()).decode()
        )

    @classmethod
    def b64_decode(cls, message: str) -> str:
        """Base64 decoder method with rot13."""
        return cls.rot13_codec(b64decode(cls.rot13_codec(message)).decode())


# #[EOF]#######################################################################
