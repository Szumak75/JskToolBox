# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide a typed container mixin with helper accessors.

`BData` ensures subclasses can manage internal dictionaries with optional type
constraints, reliable copying, and lifecycle utilities for managed state.
"""

import copy
import warnings

from inspect import currentframe
from typing import Dict, List, Any, Optional, Type

from ..raisetool import Raise

from .classes import BClasses


class BData(BClasses):
    """Container base class that adds typed dictionary semantics."""

    __data: Optional[Dict[str, Any]] = None
    __types: Optional[Dict[str, Any]] = None

    def __check_keys(self, key: str) -> bool:
        """Check if the key is available in the storage dictionary.

        ### Arguments:
        * key: str - Dictionary key to verify.

        ### Returns:
        [bool] - True when the key exists, False otherwise.
        """
        if self.__data and key in self.__data:
            return True
        return False

    def __has_type(self, key: str) -> bool:
        """Check if a type hint is registered for the given key.

        ### Arguments:
        * key: str - Dictionary key to verify.

        ### Returns:
        [bool] - True when a type constraint is registered.
        """
        if self.__types and key in self.__types:
            return True
        return False

    def __check_type(self, key: str, received_type: Optional[Any]) -> bool:
        """Validate that the stored type matches the received one.

        ### Arguments:
        * key: str - Dictionary key whose type should be verified.
        * received_type: Optional[Any] - Type extracted from input data.

        ### Returns:
        [bool] - True when the type matches the stored constraint.

        ### Raises:
        * KeyError: Raised when the key has no registered type constraint.
        """
        if self.__types and self.__has_type(key):
            if received_type == self.__types[key]:
                return True
            return False
        raise Raise.error(
            f'The key: "{key}" is missing in the directory.',
            KeyError,
            self._c_name,
            currentframe(),
        )

    def _copy_data(self, key: str) -> Optional[Any]:
        """Copy data from the internal dictionary.

        ### Arguments:
        * key: str - Variable name to copy.

        ### Returns:
        [Optional[Any]] - Deep copy of the stored value or None when missing.
        """
        if self.__check_keys(key):
            return copy.deepcopy(self._data[key])
        return None

    def _get_data(
        self,
        key: str,
        default_value: Optional[Any] = None,
        **kwargs,
    ):
        """Gets data from internal dict.

        ### Arguments:
        * key: str - Variable name.
        * default_value: Optional[Any] - Fallback value when the key is missing.

        ### Returns:
        [Optional[Any]] - Stored value or provided default.

        ### Raises:
        * TypeError: Default value does not match the registered type.

        ### Note:
        The `set_default_type` parameter is deprecated and ignored if passed.
        Use `_set_data()` with `set_default_type` to register type constraints.
        """
        # Handle deprecated set_default_type parameter for backward compatibility
        if "set_default_type" in kwargs:
            warnings.warn(
                "The 'set_default_type' parameter in _get_data() is deprecated. "
                "Use _set_data() with set_default_type to register type constraints.",
                DeprecationWarning,
                stacklevel=2,
            )

        if self.__check_keys(key):
            return self._data[key]

        if default_value is not None:
            if (
                self.__types
                and self.__has_type(key)
                and not isinstance(default_value, self.__types[key])
            ):
                raise Raise.error(
                    f"Expected '{self.__types[key]}' type, received default_value type is: {type(default_value)}",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )
            return default_value
        return None

    def _set_data(
        self,
        key: str,
        value: Optional[Any],
        set_default_type: Optional[Any] = None,
    ) -> None:
        """Sets data to internal dict.

        ### Arguments:
        * key: str - Variable name.
        * value: Optional[Any] - Value to assign.
        * set_default_type: Optional[Any] - Optional type restriction for the key.
          If None, no type constraint is registered (existing constraints are preserved).

        ### Raises:
        * TypeError: Value violates the registered or provided type constraint.
        * TypeError: Attempting to overwrite an existing type constraint.
          Use _delete_data(key) first to change the type.
        * TypeError: default_value type does not match set_default_type.
        """
        if self.__types is None:
            self.__types = {}

        if self.__has_type(key):
            # Key already has a registered type
            if set_default_type is not None and set_default_type != self.__types[key]:
                # Attempting to change the type without deleting first
                raise Raise.error(
                    f"Cannot overwrite existing type constraint for key '{key}'. "
                    f"Current type: '{self.__types[key]}', attempted type: '{set_default_type}'. "
                    f"Use _delete_data('{key}') first to change the type constraint.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

            # Verify value matches existing type
            if isinstance(value, self.__types[key]):
                self._clear_data(key)
                self._data[key] = value
            else:
                raise Raise.error(
                    f"Expected '{self.__types[key]}' type, received: '{type(value)}'",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )
        else:
            # No type registered yet
            if set_default_type is not None:
                # Register new type and verify value matches
                self.__types[key] = set_default_type
                if isinstance(value, set_default_type):
                    self._data[key] = value
                else:
                    # Clean up type registration if value doesn't match
                    del self.__types[key]
                    raise Raise.error(
                        f"The type of the value: '{type(value)}' does not match the type passed in the 'set_default_type': '{set_default_type}' variable",
                        TypeError,
                        self._c_name,
                        currentframe(),
                    )
            else:
                # No type constraint - accept any type
                self._clear_data(key)
                self._data[key] = value

    def _delete_data(self, key: str) -> None:
        """Delete data and data type from internal dict.

        ### Arguments:
        * key: str - Variable name to delete.
        """
        if self.__check_keys(key):
            del self._data[key]
        if self.__has_type(key):
            del self.__types[key]  # type: ignore

    def _clear_data(self, key: str) -> None:
        """Clear data from internal dict.
        Does not delete data type.
        If key is not found, does nothing.

        ### Arguments:
        * key: str - Variable name to delete.
        """
        if self.__check_keys(key):
            if isinstance(self._data[key], (List, Dict)):
                self._data[key].clear()
            del self._data[key]

    @property
    def _data(self) -> Dict[str, Any]:
        """Return the internal data dictionary, initializing if needed.

        ### Returns:
        [Dict[str, Any]] - Mutable storage dictionary.
        """
        if self.__data is None:
            self.__data = {}
        if self.__types is None:
            self.__types = {}
        return self.__data

    @_data.setter
    def _data(self, value: Optional[Dict[str, Any]]) -> None:
        """Assign a dictionary to the internal storage.

        ### Arguments:
        * value: Optional[Dict[str, Any]] - New dictionary or None to clear.

        ### Raises:
        * TypeError: Provided value is neither None nor a dictionary.
        * TypeError: Incoming values conflict with registered type constraints.
        """
        if value is None:
            if self.__data is not None:
                self.__data.clear()
            if self.__types is not None:
                self.__types.clear()
            return None
        if isinstance(value, Dict) and self.__data is not None:
            for key in value.keys():
                if self.__types and self.__has_type(key):
                    if not self.__check_type(key, type(value[key])):
                        raise Raise.error(
                            f"Expected '{self.__types[key]}' type, received: '{type(value[key])}'",
                            TypeError,
                            self._c_name,
                            currentframe(),
                        )
                self.__data[key] = value[key]
        else:
            raise Raise.error(
                f"Expected Dict type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )

    @_data.deleter
    def _data(self) -> None:
        """Delete the data dictionary and registered types."""
        if self.__data is not None:
            self.__data.clear()
        if self.__types is not None:
            self.__types.clear()
        self.__data = None
        self.__types = None


#
# #[EOF]#######################################################################
