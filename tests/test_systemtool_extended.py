import os
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from jsktoolbox.systemtool import CommandLineParser, Env, PathChecker


class TestCommandLineParser(TestCase):
    def setUp(self) -> None:
        self._argv_backup = sys.argv[:]

    def tearDown(self) -> None:
        sys.argv = self._argv_backup

    def test_configure_and_parse(self) -> None:
        parser = CommandLineParser()
        parser.configure_option("h", "help", "display help")
        parser.configure_option(
            "o",
            "output",
            "output file",
            has_value=True,
            example_value="file.txt",
        )
        sys.argv = ["prog", "-h", "-o", "result.txt"]
        self.assertTrue(parser.parse())
        self.assertTrue(parser.has_option("help"))
        self.assertEqual(parser.get_option("output"), "result.txt")
        dump = parser.dump()
        self.assertIn("output=", dump)
        self.assertEqual(dump["output="]["example"], "file.txt")

    def test_help_output(self) -> None:
        parser = CommandLineParser()
        parser.configure_option("h", "help", "show help")
        sys.argv = ["prog", "-h"]
        parser.parse()
        with mock.patch("builtins.print") as wrapped_print:
            parser.help()
        printed = "\n".join(
            " ".join(map(str, call.args)) for call in wrapped_print.call_args_list
        )
        self.assertIn("[HELP]", printed)
        self.assertIn("--help", printed)


class TestEnv(TestCase):
    def test_home_and_tmp(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/home/test", "TEMP": "/tmp"}):
            env = Env()
            self.assertEqual(env.home, "/home/test")
            self.assertEqual(env.tmpdir, "/tmp")

    def test_username(self) -> None:
        with mock.patch.dict(os.environ, {"USER": "tester"}):
            env = Env()
            self.assertEqual(env.username, "tester")

    def test_os_arch_uname(self) -> None:
        with mock.patch("os.name", "posix"), mock.patch(
            "subprocess.check_output", return_value=b"x86_64\n"
        ):
            env = Env()
            self.assertEqual(env.os_arch(), "64-bit")

    def test_os_arch_wmic(self) -> None:
        def fake_check_output(cmd, stderr=None):
            if cmd[:2] == ["wmic", "os"]:
                return b"OSArchitecture\n64-bit\n"
            raise FileNotFoundError

        with mock.patch("os.name", "nt"), mock.patch(
            "subprocess.check_output", side_effect=fake_check_output
        ):
            env = Env()
            self.assertEqual(env.os_arch(), "64-bit")

    def test_os_arch_fallback(self) -> None:
        with mock.patch("os.name", "posix"), mock.patch(
            "subprocess.check_output", side_effect=FileNotFoundError
        ), mock.patch("platform.architecture", return_value=("32-bit", "")):
            env = Env()
            self.assertEqual(env.os_arch(), "32-bit")


class TestPathChecker(TestCase):
    def test_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.txt"
            file_path.write_text("data")
            checker = PathChecker(str(file_path))
            self.assertTrue(checker.exists)
            self.assertTrue(checker.is_file)
            self.assertEqual(checker.filename, "sample.txt")
            self.assertEqual(checker.dirname, str(Path(temp_dir)))

    def test_directory_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "dir" / "subdir" / "file.txt"
            checker = PathChecker(str(target))
            self.assertFalse(checker.exists)
            self.assertTrue(checker.create())
            self.assertTrue(checker.exists)
            self.assertTrue(checker.is_file)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(TypeError):
            PathChecker(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            PathChecker(10)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            PathChecker("")
