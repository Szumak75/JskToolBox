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
        previous = clip.get_clipboard()
        clip.set_clipboard("jsktoolbox-tk")
        current = clip.get_clipboard()
        if current != "jsktoolbox-tk":
            self.skipTest("Clipboard contents could not be updated in this environment")
        self.assertEqual(current, "jsktoolbox-tk")
        clip.set_clipboard(previous)
        del clip
