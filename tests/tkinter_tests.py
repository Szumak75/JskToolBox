#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tkinter.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 10:54:49

Purpose: testing tkinter widget classes.
"""

import tkinter as tk
from tkinter import ttk
from jsktoolbox.tktool.widgets import VerticalScrolledTtkFrame, CreateToolTip, StatusBar


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry("400x500")
    root.minsize(width=300, height=400)

    frame = VerticalScrolledTtkFrame(root, width=300, borderwidth=2, relief=tk.SUNKEN)

    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)  # fill window

    status = StatusBar(root)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    status.set("This is a status bar")

    for i in range(30):
        line = ttk.Frame(frame.interior, borderwidth=1, relief=tk.GROOVE)

        line.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, expand=tk.TRUE)
        label = ttk.Label(line, text="This is a label " + str(i))
        label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)

        text = ttk.Entry(line, style="info.TEntry")
        text.insert(0, f"test {i}")

        sv = tk.StringVar()
        sv.set(f"text nr {i}")
        CreateToolTip(text, text=sv)
        sv.set(f"text nr {i+1}")
        text.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.X)

    root.mainloop()

# #[EOF]#######################################################################
