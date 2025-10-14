import unittest

def _tk_available():
    try:
        import tkinter as tk  # noqa: F401
        return True
    except Exception:
        return False


@unittest.skipUnless(_tk_available(), "Tkinter not available")
class TestTkClip(unittest.TestCase):
    def test_clipboard_roundtrip(self) -> None:
        from jsktoolbox.tktool.tools import _TkClip

        clip = _TkClip()
        if not clip.is_tool:
            self.skipTest("Tk clipboard backend not initialised")
        clip.set_clipboard("jsktoolbox-tk")
        self.assertEqual(clip.get_clipboard(), "jsktoolbox-tk")
        del clip
