#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  tkinter.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.01.2024, 10:54:49
  
  Purpose: testing tkinter widget classes.
"""

import os

import tkinter as tk
from tkinter import ttk
from jsktoolbox.tktool.widgets import (
    VerticalScrolledFrame,
    VerticalScrolledTtkFrame,
    CreateToolTip,
)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry("400x500")
    root.minsize(width=300, height=400)
    root.maxsize(width=900, height=900)

    frame = VerticalScrolledTtkFrame(
        root,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,  # background="light gray"
    )
    # frame.grid(column=0, row=0, sticky=tk.E)  # fixed size
    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)  # fill window

    for i in range(30):
        line = tk.Frame(frame.interior, borderwidth=1, relief=tk.GROOVE)
        # line.columnconfigure(0)

        line.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, expand=tk.TRUE)
        label = tk.Label(line, text="This is a label " + str(i))
        label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)
        # label.grid(column=0, row=i, sticky=tk.W)

        text = tk.Entry(line, textvariable=tk.StringVar(value="text"))
        sv = tk.StringVar(value=f"text nr {i}")
        CreateToolTip(text, text=sv)
        sv.set(f"text nr {i+1}")
        text.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.X)
        # text.grid(column=1, row=i, sticky=tk.EW)
    # for i in range(30):
    #     line = tk.Frame(frame, borderwidth=1, relief=tk.GROOVE)
    #     line.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER, expand=tk.TRUE)
    #     label = tk.Label(line, text="This is a label " + str(i))
    #     label.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X)
    #     # label.grid(column=0, row=i, sticky=tk.W)
    #     spacer = ttk.Separator(line, orient=tk.HORIZONTAL)
    #     spacer.pack(side=tk.LEFT, expand=tk.TRUE)

    #     text = tk.Entry(line, textvariable=tk.StringVar(value="text"))
    #     text.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.X)
    #     # text.grid(column=1, row=i, sticky=tk.EW)

    root.mainloop()

# #[EOF]#######################################################################
