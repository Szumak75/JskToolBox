# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 03.12.2023

  Purpose: Sets of containter classes with FIFO queue functionality.
"""

from typing import List, Dict, Any

from jsktoolbox.attribtool import NoDynamicAttributes


class Fifo(dict, NoDynamicAttributes):
    """"""

    __in: int = None
    __out: int = None

    def __init__(self) -> None:
        """Constructor."""
        self.__in = 0
        self.__out = 0

    def put(self, data: Any) -> None:
        """"""
        self.__in += 1
        self[self.__in] = data

    def get(self) -> Any:
        """"""
        self.__out += 1
        return dict.pop(self, self.__out)


# #[EOF]#######################################################################
