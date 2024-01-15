#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  tkinter.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.01.2024, 10:54:49
  
  Purpose: 
"""

import os

import tkinter as tk
from tkinter import ttk
from jsktoolbox.tktool.widgets import VerticalScrolledFrame, VerticalScrolledTkFrame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollbar Test")
    root.geometry("400x500")

    frame = VerticalScrolledTkFrame(
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
