# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 16.10.2023

  Purpose: simple class for basic cryptographics procedures for strings.
"""

from inspect import currentframe
from random import randrange

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise


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


# #[EOF]#######################################################################
