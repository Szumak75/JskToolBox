# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 07.05.2023

  Purpose: NoNewAttributes class for restricting the creation of dynamic
  attributes on instances of derived types.

  The solution idea published in: Python Cookbook (2004), A. Martelli,
  A. Ravenscroft, D. Ascher
"""

from typing import Any, Callable


def _no_new_attributes(
    wrapped_setattr: Any,
) -> Callable[[Any, str, Any], None]:
    """Internal function for use in the current module only."""

    def __setattr__(self, name: str, value: Any) -> None:
        """Check if the attribute is defined, throw an exception if not."""
        if hasattr(self, name):
            wrapped_setattr(self, name, value)
        else:
            raise AttributeError(
                f"Undefined attribute {name} cannot be added to {self}"
            )

    return __setattr__


class NoNewAttributes:
    """NoNewAttributes - base class.

    Class for restricting the creation of dynamic attributes on instances
    of derived types.
    """

    __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
        object.__setattr__
    )

    class __metaclass__(type):
        __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
            type.__setattr__
        )


# #[EOF]#######################################################################
