# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2026-02-28

Purpose: Demonstrate guarding mixin properties against subclass overriding.

This example shows two variants:
1. Warn mode: emit `UserWarning` when a guarded property is overridden.
2. Strict mode: raise `TypeError` when a guarded property is overridden.
"""

from __future__ import annotations

import warnings
from typing import ClassVar, FrozenSet

from jsktoolbox.basetool import ThBaseObject


class GuardedThBaseObject(ThBaseObject):
    """Mixin extension that checks for guarded property overrides."""

    _guarded_properties: ClassVar[FrozenSet[str]] = frozenset(
        {
            "_thread",
            "_handle",
            "_os_thread_handle",
            "_stop_event",
        }
    )
    _guard_mode: ClassVar[str] = "warn"

    def __init_subclass__(cls, **kwargs) -> None:
        """Validate guarded members when creating subclass definitions.

        ### Arguments:
        * kwargs: dict - Arbitrary keyword arguments passed by Python.

        ### Raises:
        * TypeError: Raised in strict mode when guarded members are overridden.
        """
        super().__init_subclass__(**kwargs)
        overridden: set[str] = set(cls.__dict__).intersection(cls._guarded_properties)
        if not overridden:
            return

        message: str = f"{cls.__name__} overrides guarded members: {sorted(overridden)}"
        if cls._guard_mode == "error":
            raise TypeError(message)
        warnings.warn(message, UserWarning, stacklevel=2)


class StrictGuardedThBaseObject(GuardedThBaseObject):
    """Variant that enforces strict no-override policy."""

    _guard_mode: ClassVar[str] = "error"


def demo_warn_mode() -> None:
    """Show warning behavior for guarded property override."""
    print("--- warn mode ---")
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")

        class WarnWorker(GuardedThBaseObject):
            """Subclass that intentionally overrides a guarded property."""

            @property
            def _thread(self):  # type: ignore
                return None

        print(f"class created: {WarnWorker.__name__}")
        for warning in captured:
            print(f"warning: {warning.message}")


def demo_error_mode() -> None:
    """Show exception behavior for guarded property override."""
    print("--- strict mode ---")
    try:

        class StrictWorker(StrictGuardedThBaseObject):
            """Subclass that intentionally violates strict guard rules."""

            @property
            def _thread(self):  # type: ignore
                return None

        print(f"class created: {StrictWorker.__name__}")
    except TypeError as ex:
        print(f"error: {ex}")


def demo_ok_mode() -> None:
    """Show subclass creation with no guarded override."""
    print("--- valid subclass ---")

    class ValidWorker(StrictGuardedThBaseObject):
        """Subclass that does not override guarded properties."""

        @property
        def worker_name(self) -> str:
            return self._c_name

    worker = ValidWorker()
    print(f"class created: {worker.__class__.__name__}")
    print(f"worker_name: {worker.worker_name}")


if __name__ == "__main__":
    demo_warn_mode()
    demo_error_mode()
    demo_ok_mode()
