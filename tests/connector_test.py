#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose:
"""

from typing import Optional

from jsktoolbox.netaddresstool.ipv4 import Address
from jsktoolbox.logstool.queue import LoggerQueue

from jsktoolbox.devices.network.connectors import API
from jsktoolbox.devices.mikrotik.routerboard import RouterBoard

from jsktoolbox.devices.mikrotik.elements.libs.search import RBQuery
from jsktoolbox.devices.mikrotik.base import Element

if __name__ == "__main__":
    ch = API(
        # ip_address=Address("10.5.5.254"),
        # ip_address=Address("10.255.53.118"),
        ip_address=Address("10.1.15.36"),
        port=8728,
        login="devel",
        password="mojehaslo",
    )
    ch.connect()
    q = LoggerQueue()
    query = RBQuery()
    # query.add_attrib("list", "allowed-devices3")
    # query.add_attrib("address", "10.30.32.9")
    query.add_attrib("state", "Full")
    print(query.query)

    rb = RouterBoard(connector=ch, qlog=q, debug=True, verbose=True)
    # rb.dump()
    # print("Check element return")
    # out = rb.element("/ip/firewall/address-list/")
    # out: Optional[Element] = rb.element("/ip/firewall/address-list/", auto_load=True)
    # out: Optional[Element] = rb.element("/routing/ospf/neighbor/", auto_load=True)
    out: Optional[Element] = rb.element("/file/", auto_load=True)

    if out:
        # print(out.search(query.query))
        out.dump()
        # print(out)
        # print(out.root)
        # print(out.get())
        # print(out)
        # out.dump()
    print(q.get())

# #[EOF]#######################################################################
