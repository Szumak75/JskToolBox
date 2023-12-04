#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose:
"""

from jsktoolbox.devices.network.connectors import API
from jsktoolbox.netaddresstool.ipv4 import Address

if __name__ == "__main__":
    obj = API(
        ip_address=Address("10.5.5.254"),
        port=8728,
        login="devel",
        password="mojehaslo",
    )
    obj.connect()
    print(obj.execute("/system/routerboard/print"))
    print(obj.outputs())
    print(obj.errors())
    print(obj.execute("/system/resource/cpu/print"))
    print(obj.outputs())
    print(obj.errors())

# #[EOF]#######################################################################
