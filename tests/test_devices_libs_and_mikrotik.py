# -*- coding: UTF-8 -*-
"""
Author:  Project Test Suite --<tests@jsktoolbox.local>
Created: 2024-05-12

Purpose: Unit tests for helper classes in `jsktoolbox.devices`.
"""

import unittest
from typing import Any, Dict, List, Optional, Tuple, Union

from jsktoolbox.devices.libs.base import BDebug, BDev
from jsktoolbox.devices.libs.converters import B64Converter
from jsktoolbox.devices.mikrotik.base import BRouterOS, Element
from jsktoolbox.devices.network.connectors import IConnector
from jsktoolbox.logstool.logs import LoggerClient
from jsktoolbox.netaddresstool import Address, Address6


class DummyDebug(BDebug):
    """Concrete helper to expose BDebug behaviour in tests."""


class DummyDevice(BDev):
    """Concrete helper to expose BDev behaviour in tests."""


class FakeConnector(IConnector):
    """Lightweight connector stub used to exercise BRouterOS logic."""

    def __init__(self) -> None:
        self._address: Optional[Union[Address, Address6]] = None
        self._login: Optional[str] = None
        self._password: Optional[str] = None
        self._port: Optional[int] = None
        self._last_stdout: List[List[Dict[str, Any]]] = [[]]
        self._last_stderr: List[List[Dict[str, Any]]] = [[]]
        self._errors: List[str] = []
        self._pending: List[
            Tuple[
                bool,
                List[List[Dict[str, Any]]],
                List[List[Dict[str, Any]]],
            ]
        ] = []
        self.commands: List[Union[str, List[str]]] = []
        self.disconnected = False

    def enqueue_response(
        self,
        stdout: Optional[List[List[Dict[str, Any]]]] = None,
        stderr: Optional[List[List[Dict[str, Any]]]] = None,
        result: bool = True,
    ) -> None:
        """Register canned connector outputs for the next execute call."""
        if stdout is None:
            stdout = [[]]
        if stderr is None:
            stderr = [[]]
        self._pending.append((result, stdout, stderr))

    # -- IConnector API -----------------------------------------------------

    def connect(self) -> bool:
        return True

    def disconnect(self) -> bool:
        self.disconnected = True
        return True

    def errors(self) -> List[str]:
        return list(self._errors)

    def execute(self, commands: Union[str, List[str]]) -> bool:
        self.commands.append(commands)
        if self._pending:
            result, stdout, stderr = self._pending.pop(0)
            self._last_stdout = stdout
            self._last_stderr = stderr
            if not result:
                self._errors.append("execute returned False")
            return result
        self._last_stdout = [[]]
        self._last_stderr = [[]]
        return True

    @property
    def address(self) -> Optional[Union[Address, Address6]]:
        return self._address

    @address.setter
    def address(self, ip_address: Union[Address, Address6]) -> None:
        self._address = ip_address

    @property
    def is_alive(self) -> bool:
        return True

    @property
    def login(self) -> Optional[str]:
        return self._login

    @login.setter
    def login(self, username: str) -> None:
        self._login = username

    def outputs(
        self,
    ) -> Tuple[List[List[Dict[str, Any]]], List[List[Dict[str, Any]]]]:
        return self._last_stdout, self._last_stderr

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, passwd: str) -> None:
        self._password = passwd

    @property
    def port(self) -> Optional[int]:
        return self._port

    @port.setter
    def port(self, port: int) -> None:
        self._port = port

    @property
    def prototype(self) -> str:
        return "FAKE"


class DevicesLibsMikrotikTests(unittest.TestCase):
    """Test suite covering helpers from `jsktoolbox.devices`."""

    def test_b64_converter_roundtrip(self) -> None:
        """Ensure base64 conversion preserves payloads."""
        text = "RouterOS FTW!"
        encoded = B64Converter.string_to_base64(text)
        self.assertIsInstance(encoded, bytes)
        decoded = B64Converter.base64_to_string(encoded)
        self.assertEqual(decoded, text)

    def test_debug_flags_default_and_assignment(self) -> None:
        """BDebug should expose togglable debug/verbose flags."""
        helper = DummyDebug()
        self.assertFalse(helper.debug)
        self.assertFalse(helper.verbose)
        helper.debug = True
        helper.verbose = True
        self.assertTrue(helper.debug)
        self.assertTrue(helper.verbose)

    def test_device_root_chains_from_parent(self) -> None:
        """BDev root should include parent prefixes."""
        parent = DummyDevice()
        parent.root = "/system/"
        child = DummyDevice()
        child.parent = parent
        child.root = "identity/"
        self.assertEqual(child.root, "/system/identity/")

    def test_brouteros_load_populates_attributes(self) -> None:
        """BRouterOS.load should hydrate attrib dict for single result."""
        connector = FakeConnector()
        connector.enqueue_response(
            stdout=[[{"identity": "core-router"}]],
            stderr=[[]],
            result=True,
        )
        router = BRouterOS(
            parent=None,
            connector=connector,
            logs=LoggerClient(name="root"),
            debug=False,
            verbose=False,
        )
        router.root = "/system/"
        self.assertTrue(router.load(router.root))
        self.assertTrue(router.is_loaded)
        self.assertEqual(router.attrib["identity"], "core-router")
        self.assertEqual(connector.commands[-1], "/system/print")

    def test_brouteros_load_handles_list_payload(self) -> None:
        """BRouterOS.load should populate list when several entries appear."""
        connector = FakeConnector()
        connector.enqueue_response(
            stdout=[[{"name": "bridge1"}, {"name": "bridge2"}]],
            stderr=[[]],
            result=True,
        )
        router = BRouterOS(
            parent=None,
            connector=connector,
            logs=LoggerClient(name="root"),
            debug=False,
            verbose=False,
        )
        router.root = "/interface/"
        self.assertTrue(router.load(router.root))
        names = [entry["name"] for entry in router.list]
        self.assertListEqual(names, ["bridge1", "bridge2"])

    def test_add_elements_builds_nested_tree(self) -> None:
        """_add_elements should create Element objects recursively."""
        connector = FakeConnector()
        router = BRouterOS(
            parent=None,
            connector=connector,
            logs=LoggerClient(name="root"),
            debug=False,
            verbose=False,
        )
        router.root = "/"
        elements = {"system": {"identity": {}, "routerboard": {}}}
        router._add_elements(router, elements)
        self.assertIn("system", router.elements)
        system_element = router.elements["system"]
        self.assertIn("identity", system_element.elements)
        self.assertIn("routerboard", system_element.elements)

    def test_element_search_matches_attributes_and_list(self) -> None:
        """Element.search should locate entries in attrib or list."""
        connector = FakeConnector()
        router = BRouterOS(
            parent=None,
            connector=connector,
            logs=LoggerClient(name="root"),
            debug=False,
            verbose=False,
        )
        router.root = "/"
        element = Element(
            key="routing",
            parent=router,
            connector=connector,
            qlog=None,
            debug=False,
            verbose=False,
        )
        element.attrib["id"] = "ospf"
        self.assertEqual(element.search({"id": "ospf"}), element.attrib)
        element.attrib.clear()
        element.list.append({"name": "default", "distance": "1"})
        element.list.append({"name": "backup", "distance": "2"})
        matches = element.search({"name": "default", "distance": "1"})
        self.assertEqual(matches, [{"name": "default", "distance": "1"}])


# #[EOF]#######################################################################
