import pytest
from unittest.mock import patch, MagicMock
from typing import List
from .nettool import Pinger, Tracert

# Python

class TestPinger:
    @patch("jsktoolbox.nettool.find_executable", return_value="/usr/bin/ping")
    @patch("jsktoolbox.nettool.os.system", return_value=0)
    def test_is_alive_true(self, mock_system, mock_find):
        p = Pinger(timeout=1)
        assert p.is_alive("127.0.0.1") is True

    @patch("jsktoolbox.nettool.find_executable", return_value="/usr/bin/ping")
    @patch("jsktoolbox.nettool.os.system", return_value=1)
    def test_is_alive_false(self, mock_system, mock_find):
        p = Pinger(timeout=1)
        assert p.is_alive("127.0.0.1") is False

    @patch("jsktoolbox.nettool.find_executable", return_value=None)
    def test_is_alive_no_command(self, mock_find):
        p = Pinger(timeout=1)
        # Remove command so is_alive will raise
        p._set_data(key=p._Keys.COMMAND, value=None)
        with pytest.raises(Exception):
            p.is_alive("127.0.0.1")

class TestTracert:
    @patch("jsktoolbox.nettool.find_executable", return_value="/usr/bin/traceroute")
    @patch("jsktoolbox.nettool.os.system", return_value=0)
    def test_execute_success(self, mock_system, mock_find):
        t = Tracert()
        mock_proc = MagicMock()
        mock_proc.__enter__.return_value = mock_proc
        mock_proc.__exit__.return_value = False
        mock_proc.stdout = [b"1 127.0.0.1 0.123 ms\n", b"2 192.168.0.1 0.456 ms\n"]
        with patch("jsktoolbox.nettool.subprocess.Popen", return_value=mock_proc):
            result = t.execute("127.0.0.1")
            assert isinstance(result, List)
            assert "1 127.0.0.1 0.123 ms\n" in result
            assert "2 192.168.0.1 0.456 ms\n" in result

    @patch("jsktoolbox.nettool.find_executable", return_value=None)
    def test_execute_no_command(self, mock_find):
        t = Tracert()
        # Remove command so execute will raise
        t._set_data(key=t._Keys.COMMAND, value=None)
        with pytest.raises(Exception):
            t.execute("127.0.0.1")