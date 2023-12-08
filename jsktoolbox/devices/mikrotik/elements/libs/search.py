# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: Query class as helper for build query elements dict.
"""

from copy import copy
from typing import Dict
from jsktoolbox.libs.base_data import BData
from jsktoolbox.attribtool import ReadOnlyClass


class RBQuery(BData):
    """RBQuery class helper."""

    class Keys(object, metaclass=ReadOnlyClass):
        SEARCH = "_search_query_"

    def __init__(self) -> None:
        """Constructor."""
        self._data[RBQuery.Keys.SEARCH] = {}

    def add_attrib(self, attrib: str) -> None:
        """"""
        self._data[RBQuery.Keys.SEARCH][attrib] = None

    def add_attrib_with_value(self, attrib: str, value: str) -> None:
        """"""
        self._data[RBQuery.Keys.SEARCH][attrib] = value

    @property
    def query(self) -> Dict:
        """"""
        return copy(self._data[RBQuery.Keys.SEARCH])


# #[EOF]#######################################################################
