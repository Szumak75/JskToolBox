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

    def test_configure_argument_emits_deprecation_warning(self) -> None:
        parser = CommandLineParser()
        with self.assertWarns(DeprecationWarning):
            parser.configure_argument("h", "help", "display help")
        self.assertIn("help", parser.dump())

    def test_parse_arguments_emits_deprecation_warning(self) -> None:
        parser = CommandLineParser()
        parser.configure_option("h", "help", "display help")
        sys.argv = ["prog", "-h"]
        with self.assertWarns(DeprecationWarning):
            self.assertTrue(parser.parse_arguments())

    def test_parse_returns_false_on_invalid_arguments(self) -> None:
        parser = CommandLineParser()
        parser.configure_option("h", "help", "display help")
        sys.argv = ["prog", "--unknown"]
        with mock.patch("builtins.print") as wrapped_print:
            self.assertFalse(parser.parse())
        printed = "\n".join(
            " ".join(map(str, call.args)) for call in wrapped_print.call_args_list
        )
        self.assertIn("Command line argument error", printed)

    def test_configure_option_requires_long_name(self) -> None:
        parser = CommandLineParser()
        with self.assertRaises(AttributeError):
            parser.configure_option("h", "")


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

    def test_home_from_homepath_and_homedrive(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"HOMEPATH": "\\Users\\tester", "HOMEDRIVE": "C:"},
            clear=True,
        ):
            env = Env()
            self.assertEqual(env.home, "C:\\Users\\tester")

    def test_tmpdir_falls_back_to_gettempdir(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"HOME": "/home/test"},
            clear=True,
        ), mock.patch("tempfile.gettempdir", return_value="/fallback/tmp"):
            env = Env()
            self.assertEqual(env.tmpdir, "/fallback/tmp")

    def test_username_empty_when_missing(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/home/test"}, clear=True):
            env = Env()
            self.assertEqual(env.username, "")

    def test_is_64bits_property(self) -> None:
        env = Env()
        with mock.patch("sys.maxsize", 2**63):
            self.assertTrue(env.is_64bits)
        with mock.patch("sys.maxsize", 2**31):
            self.assertFalse(env.is_64bits)


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

    def test_symlink_and_repr(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            target = base_dir / "target.txt"
            target.write_text("data")
            link = base_dir / "link.txt"
            link.symlink_to(target)

            checker = PathChecker(str(link))

            self.assertTrue(checker.exists)
            self.assertTrue(checker.is_symlink)
            self.assertTrue(checker.is_file)
            self.assertEqual(checker.filename, "link.txt")
            self.assertEqual(checker.posixpath, str(target.resolve()))
            self.assertEqual(repr(checker), f"PathChecker('{link}')")
            self.assertIn("'is_symlink': 'True'", str(checker))

    def test_missing_path_has_no_name_parts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing" / "file.txt"
            checker = PathChecker(str(missing_path))
            self.assertFalse(checker.exists)
            self.assertIsNone(checker.dirname)
            self.assertIsNone(checker.filename)
            self.assertIsNone(checker.posixpath)
