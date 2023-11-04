# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 03.11.2023

  Purpose: Base class for classess derived from threading.Thread
"""

from inspect import currentframe
from typing import Any, Optional, Tuple, Dict
from threading import Event
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def TARGET(cls) -> str:
        """Return TARGET Key."""
        return "_target"

    @classmethod
    @property
    def NAME(cls) -> str:
        """Return NAME Key."""
        return "_name"

    @classmethod
    @property
    def ARGS(cls) -> str:
        """Return ARGS Key."""
        return "_args"

    @classmethod
    @property
    def KWARGS(cls) -> str:
        """Return KWARGS Key."""
        return "_kwargs"

    @classmethod
    @property
    def DAEMONIC(cls) -> str:
        """Return DAEMONIC Key."""
        return "_daemonic"

    @classmethod
    @property
    def IDENT(cls) -> str:
        """Return IDENT Key."""
        return "_ident"

    @classmethod
    @property
    def NATIVE_ID(cls) -> str:
        """Return NATIVE_ID Key."""
        return "_native_id"

    @classmethod
    @property
    def TSTATE_LOCK(cls) -> str:
        """Return TSTATE_LOCK Key."""
        return "_tstate_lock"

    @classmethod
    @property
    def STARTED(cls) -> str:
        """Return STARTED Key."""
        return "_started"

    @classmethod
    @property
    def IS_STOPPED(cls) -> str:
        """Return IS_STOPPED Key."""
        return "_is_stopped"

    @classmethod
    @property
    def STDERR(cls) -> str:
        """Return STDERR Key."""
        return "_stderr"

    @classmethod
    @property
    def INVOKE_EXCEPTHOOK(cls) -> str:
        """Return INVOKE_EXCEPTHOOK Key."""
        return "_invoke_excepthook"

    @classmethod
    @property
    def STOP_EVENT(cls) -> str:
        """Return STOP_EVENT Key."""
        return "_stop_event"

    @classmethod
    @property
    def SLEEP_PERIOD(cls) -> str:
        """Return SLEEP_PERIOD Key."""
        return "_sleep_period"


class ThBaseObject(BData, NoDynamicAttributes):
    """Base class for classes derived from threading.Thread.

    Definition of properties used in the threading library.
    """

    @property
    def _target(self) -> Optional[Any]:
        if Keys.TARGET not in self._data:
            self._data[Keys.TARGET] = None
        return self._data[Keys.TARGET]

    @_target.setter
    def _target(self, value: Any) -> None:
        self._data[Keys.TARGET] = value

    @property
    def _name(self) -> Optional[str]:
        if Keys.NAME not in self._data:
            self._data[Keys.NAME] = None
        return self._data[Keys.NAME]

    @_name.setter
    def _name(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise Raise.error(
                f"String type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.NAME] = value

    @property
    def _args(self) -> Optional[Tuple]:
        if Keys.ARGS not in self._data:
            self._data[Keys.ARGS] = None
        return self._data[Keys.ARGS]

    @_args.setter
    def _args(self, value: Tuple) -> None:
        self._data[Keys.ARGS] = value

    @property
    def _kwargs(self) -> Optional[Dict]:
        if Keys.KWARGS not in self._data:
            self._data[Keys.KWARGS] = None
        return self._data[Keys.KWARGS]

    @_kwargs.setter
    def _kwargs(self, value: Dict) -> None:
        if value is not None and not isinstance(value, Dict):
            raise Raise.error(
                f"Dict type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.KWARGS] = value

    @property
    def _daemonic(self) -> Optional[bool]:
        if Keys.DAEMONIC not in self._data:
            self._data[Keys.DAEMONIC] = None
        return self._data[Keys.DAEMONIC]

    @_daemonic.setter
    def _daemonic(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Boolean type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.DAEMONIC] = value

    @property
    def _ident(self) -> Optional[int]:
        if Keys.IDENT not in self._data:
            self._data[Keys.IDENT] = None
        return self._data[Keys.IDENT]

    @_ident.setter
    def _ident(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise Raise.error(
                f"Integer type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.IDENT] = value

    @property
    def _native_id(self) -> Optional[int]:
        if Keys.NATIVE_ID not in self._data:
            self._data[Keys.NATIVE_ID] = None
        return self._data[Keys.NATIVE_ID]

    @_native_id.setter
    def _native_id(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise Raise.error(
                f"Integer type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.NATIVE_ID] = value

    @property
    def _tstate_lock(self) -> Optional[Any]:
        if Keys.TSTATE_LOCK not in self._data:
            self._data[Keys.TSTATE_LOCK] = None
        return self._data[Keys.TSTATE_LOCK]

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        self._data[Keys.TSTATE_LOCK] = value

    @property
    def _started(self) -> Optional[Event]:
        if Keys.STARTED not in self._data:
            self._data[Keys.STARTED] = None
        return self._data[Keys.STARTED]

    @_started.setter
    def _started(self, value: Event) -> None:
        if value is not None and not isinstance(value, Event):
            raise Raise.error(
                f"threading.Event type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.STARTED] = value

    @property
    def _is_stopped(self) -> Optional[bool]:
        if Keys.IS_STOPPED not in self._data:
            self._data[Keys.IS_STOPPED] = None
        return self._data[Keys.IS_STOPPED]

    @_is_stopped.setter
    def _is_stopped(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Boolean type expected, '{type(value)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.IS_STOPPED] = value

    @property
    def _stderr(self) -> Optional[Any]:
        if Keys.STDERR not in self._data:
            self._data[Keys.STDERR] = None
        return self._data[Keys.STDERR]

    @_stderr.setter
    def _stderr(self, value: Any) -> None:
        self._data[Keys.STDERR] = value

    @property
    def _invoke_excepthook(self) -> Optional[Any]:
        if Keys.INVOKE_EXCEPTHOOK not in self._data:
            self._data[Keys.INVOKE_EXCEPTHOOK] = None
        return self._data[Keys.INVOKE_EXCEPTHOOK]

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Any) -> None:
        self._data[Keys.INVOKE_EXCEPTHOOK] = value

    @property
    def _stop_event(self) -> Optional[Event]:
        if Keys.STOP_EVENT not in self._data:
            self._data[Keys.STOP_EVENT] = None
        return self._data[Keys.STOP_EVENT]

    @_stop_event.setter
    def _stop_event(self, obj: Event) -> None:
        if obj is not None and not isinstance(obj, Event):
            raise Raise.error(
                f"threading.Event type expected, '{type(obj)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.STOP_EVENT] = obj

    @property
    def is_stopped(self) -> Optional[bool]:
        return self._is_stopped

    @property
    def started(self) -> bool:
        return self._started.is_set()

    @property
    def _sleep_period(self) -> float:
        """Return sleepperiod value."""
        if Keys.SLEEP_PERIOD not in self._data:
            self._data[Keys.SLEEP_PERIOD] = 1.0
        return self._data[Keys.SLEEP_PERIOD]

    @_sleep_period.setter
    def _sleep_period(self, value: float) -> None:
        """Set sleepperiod value."""
        if not isinstance(value, float):
            raise Raise.error(
                f"Positive float type expected, '{value}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self._data[Keys.SLEEP_PERIOD] = value


# #[EOF]#######################################################################
