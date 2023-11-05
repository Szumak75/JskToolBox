#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 05.11.2023

  Purpose:
"""
import getopt
import sys


class CommandLineParser:
    def __init__(self):
        self.configured_args = {}
        self.args = {}

    def configure_argument(self, short_arg, long_arg, has_value=False):
        if "short_opts" not in self.configured_args:
            self.configured_args["short_opts"] = ""
        if "long_opts" not in self.configured_args:
            self.configured_args["long_opts"] = []

        self.configured_args["short_opts"] += short_arg + (
            ":" if has_value else ""
        )
        self.configured_args["long_opts"].append(
            long_arg + ("=" if has_value else "")
        )

    def parse_arguments(self):
        print(f"{self.configured_args} # {self.args}")
        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                self.configured_args["short_opts"],
                self.configured_args["long_opts"],
            )
        except getopt.GetoptError:
            print("Usage: python script.py <options>")
            sys.exit(2)

        for opt, value in opts:
            for short_arg, long_arg in zip(
                self.configured_args["short_opts"],
                self.configured_args["long_opts"],
            ):
                if opt in ("-" + short_arg, "--" + long_arg):
                    self.args[long_arg] = value
        print(f"{self.configured_args} # {self.args}")

    def get_option(self, option):
        """"""
        return self.args.get(option)


if __name__ == "__main__":
    parser = CommandLineParser()

    # Konfiguracja argumentów
    parser.configure_argument("h", "help")
    parser.configure_argument("v", "verbose")
    parser.configure_argument("f", "file", has_value=True)
    parser.configure_argument("d", "debug")

    # Parsowanie argumentów
    parser.parse_arguments()

    # Wyświetlenie przetworzonych argumentów
    print("Parsed arguments:")
    for arg, value in parser.args.items():
        print(f"{arg}: {value}")

    print(parser.get_option("verbose"))

# #[EOF]#######################################################################
