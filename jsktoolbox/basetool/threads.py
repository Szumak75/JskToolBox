# -*- coding: utf-8 -*-
"""
  threads.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.01.2024, 10:23:51
  
  Purpose: Base class for classes derived from threading.Thread
"""

from io import TextIOWrapper
from typing import Any, Optional, Tuple, Dict
from threading import Event

from .data import BData
from ..attribtool import ReadOnlyClass


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS: str = "_args"
    DAEMONIC: str = "_daemonic"
    DEBUG: str = "_debug"
    IDENT: str = "_ident"
    INVOKE_EXCEPTHOOK: str = "_invoke_excepthook"
    IS_STOPPED: str = "_is_stopped"
    KWARGS: str = "_kwargs"
    NAME: str = "_name"
    NATIVE_ID: str = "_native_id"
    SLEEP_PERIOD: str = "_sleep_period"
    STARTED: str = "_started"
    STDERR: str = "_stderr"
    STOP_EVENT: str = "_stop_event"
    TARGET: str = "_target"
    TSTATE_LOCK: str = "_tstate_lock"


class ThBaseObject(BData):
    """Base class for classes derived from threading.Thread.

    Definition of properties used in the threading library.
    """

    @property
    def _target(self) -> Optional[Any]:
        return self._get_data(
            key=_Keys.TARGET, set_default_type=Optional[Any], default_value=None
        )

    @_target.setter
    def _target(self, value: Any) -> None:
        self._set_data(key=_Keys.TARGET, value=value, set_default_type=Optional[Any])

    @property
    def _name(self) -> Optional[str]:
        return self._get_data(
            key=_Keys.NAME, set_default_type=Optional[str], default_value=None
        )

    @_name.setter
    def _name(self, value: Optional[str]) -> None:
        self._set_data(key=_Keys.NAME, value=value, set_default_type=Optional[str])

    @property
    def _args(self) -> Optional[Tuple]:
        return self._get_data(
            key=_Keys.ARGS, set_default_type=Optional[Tuple], default_value=None
        )

    @_args.setter
    def _args(self, value: Tuple) -> None:
        self._set_data(key=_Keys.ARGS, value=value, set_default_type=Optional[Tuple])

    @property
    def _kwargs(self) -> Optional[Dict]:
        return self._get_data(
            key=_Keys.KWARGS, set_default_type=Optional[Dict], default_value=None
        )

    @_kwargs.setter
    def _kwargs(self, value: Dict) -> None:
        self._set_data(key=_Keys.KWARGS, value=value, set_default_type=Optional[Dict])

    @property
    def _daemonic(self) -> Optional[bool]:
        return self._get_data(
            key=_Keys.DAEMONIC, set_default_type=Optional[bool], default_value=None
        )

    @_daemonic.setter
    def _daemonic(self, value: bool) -> None:
        self._set_data(key=_Keys.DAEMONIC, value=value, set_default_type=Optional[bool])

    @property
    def _debug(self) -> Optional[bool]:
        return self._get_data(
            key=_Keys.DEBUG, set_default_type=Optional[bool], default_value=None
        )

    @_debug.setter
    def _debug(self, value: bool) -> None:
        self._set_data(key=_Keys.DEBUG, value=value, set_default_type=Optional[bool])

    @property
    def _ident(self) -> Optional[int]:
        return self._get_data(
            key=_Keys.IDENT, set_default_type=Optional[int], default_value=None
        )

    @_ident.setter
    def _ident(self, value: Optional[int]) -> None:
        self._set_data(key=_Keys.IDENT, value=value, set_default_type=Optional[int])

    @property
    def _native_id(self) -> Optional[int]:
        return self._get_data(
            key=_Keys.NATIVE_ID, set_default_type=Optional[int], default_value=None
        )

    @_native_id.setter
    def _native_id(self, value: Optional[int]) -> None:
        self._set_data(key=_Keys.NATIVE_ID, value=value, set_default_type=Optional[int])

    @property
    def _tstate_lock(self) -> Optional[Any]:
        return self._get_data(
            key=_Keys.TSTATE_LOCK, set_default_type=Optional[Any], default_value=None
        )

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        self._set_data(
            key=_Keys.TSTATE_LOCK, value=value, set_default_type=Optional[Any]
        )

    @property
    def _started(self) -> Optional[Event]:
        return self._get_data(
            key=_Keys.STARTED, set_default_type=Optional[Event], default_value=None
        )

    @_started.setter
    def _started(self, value: Event) -> None:
        self._set_data(key=_Keys.STARTED, value=value, set_default_type=Optional[Event])

    @property
    def _is_stopped(self) -> Optional[bool]:
        return self._get_data(
            key=_Keys.IS_STOPPED, set_default_type=Optional[bool], default_value=None
        )

    @_is_stopped.setter
    def _is_stopped(self, value: bool) -> None:
        self._set_data(
            key=_Keys.IS_STOPPED, value=value, set_default_type=Optional[bool]
        )

    @property
    def _stderr(self) -> Optional[TextIOWrapper]:
        return self._get_data(
            key=_Keys.STDERR,
            set_default_type=Optional[TextIOWrapper],
            default_value=None,
        )

    @_stderr.setter
    def _stderr(self, value: Optional[TextIOWrapper]) -> None:
        self._set_data(
            key=_Keys.STDERR, value=value, set_default_type=Optional[TextIOWrapper]
        )

    @property
    def _invoke_excepthook(self) -> Optional[Any]:
        return self._get_data(
            key=_Keys.INVOKE_EXCEPTHOOK,
            set_default_type=Optional[Any],
            default_value=None,
        )

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Any) -> None:
        self._set_data(
            key=_Keys.INVOKE_EXCEPTHOOK, value=value, set_default_type=Optional[Any]
        )

    @property
    def _stop_event(self) -> Optional[Event]:
        return self._get_data(
            key=_Keys.STOP_EVENT, set_default_type=Optional[Event], default_value=None
        )

    @_stop_event.setter
    def _stop_event(self, obj: Event) -> None:
        self._set_data(key=_Keys.STOP_EVENT, value=obj, set_default_type=None)

    @property
    def is_stopped(self) -> Optional[bool]:
        return self._is_stopped

    @property
    def started(self) -> bool:
        if self._started is not None:
            return self._started.is_set()
        return False

    @property
    def sleep_period(self) -> float:
        """Return sleep period value."""
        return self._get_data(
            key=_Keys.SLEEP_PERIOD, set_default_type=float, default_value=1.0
        )  # type: ignore

    @sleep_period.setter
    def sleep_period(self, value: float) -> None:
        """Set sleep period value."""
        self._set_data(key=_Keys.SLEEP_PERIOD, value=value, set_default_type=float)


# #[EOF]#######################################################################
