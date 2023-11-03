# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 03.11.2023

  Purpose: Base class for classess derived from threading.Thread
"""

from typing import Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.libs.base_data import BData


class ThBaseObject(BData, NoDynamicAttributes):
    """Base class for classes derived from threading.Thread"""

    @property
    def _target(self) -> Any:
        if "_target" not in self._data:
            self._data["_target"] = None
        return self._data["_target"]

    @_target.setter
    def _target(self, value: Any) -> None:
        self._data["_target"] = value

    @property
    def _name(self) -> Any:
        if "_name" not in self._data:
            self._data["_name"] = None
        return self._data["_name"]

    @_name.setter
    def _name(self, value: Any) -> None:
        self._data["_name"] = value

    @property
    def _args(self) -> Any:
        if "_args" not in self._data:
            self._data["_args"] = None
        return self._data["_args"]

    @_args.setter
    def _args(self, value: Any) -> None:
        self._data["_args"] = value

    @property
    def _kwargs(self) -> Any:
        if "_kwargs" not in self._data:
            self._data["_kwargs"] = None
        return self._data["_kwargs"]

    @_kwargs.setter
    def _kwargs(self, value: Any) -> None:
        self._data["_kwargs"] = value

    @property
    def _daemonic(self) -> Any:
        if "_daemonic" not in self._data:
            self._data["_daemonic"] = None
        return self._data["_daemonic"]

    @_daemonic.setter
    def _daemonic(self, value: Any) -> None:
        self._data["_daemonic"] = value

    @property
    def _ident(self) -> Any:
        if "_ident" not in self._data:
            self._data["_ident"] = None
        return self._data["_ident"]

    @_ident.setter
    def _ident(self, value: Any) -> None:
        self._data["_ident"] = value

    @property
    def _native_id(self) -> Any:
        if "_native_id" not in self._data:
            self._data["_native_id"] = None
        return self._data["_native_id"]

    @_native_id.setter
    def _native_id(self, value: Any) -> None:
        self._data["_native_id"] = value

    @property
    def _tstate_lock(self) -> Any:
        if "_tstate_lock" not in self._data:
            self._data["_tstate_lock"] = None
        return self._data["_tstate_lock"]

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        self._data["_tstate_lock"] = value

    @property
    def _started(self) -> Any:
        if "_started" not in self._data:
            self._data["_started"] = None
        return self._data["_started"]

    @_started.setter
    def _started(self, value: Any) -> None:
        self._data["_started"] = value

    @property
    def _is_stopped(self) -> Any:
        if "_is_stopped" not in self._data:
            self._data["_is_stopped"] = None
        return self._data["_is_stopped"]

    @_is_stopped.setter
    def _is_stopped(self, value: Any) -> None:
        self._data["_is_stopped"] = value

    @property
    def _stderr(self) -> Any:
        if "_stderr" not in self._data:
            self._data["_stderr"] = None
        return self._data["_stderr"]

    @_stderr.setter
    def _stderr(self, value: Any) -> None:
        self._data["_stderr"] = value

    @property
    def _invoke_excepthook(self) -> Any:
        if "_invoke_excepthook" not in self._data:
            self._data["_invoke_excepthook"] = None
        return self._data["_invoke_excepthook"]

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Any) -> None:
        self._data["_invoke_excepthook"] = value


# #[EOF]#######################################################################
