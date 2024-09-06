#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 07.11.2023

  Purpose:
"""

from jsktoolbox.systemtool import CommandLineParser


if __name__ == "__main__":
    parser = CommandLineParser()

    # Konfiguracja argumentów
    parser.configure_argument("", "example", desc_arg="This is a test")
    parser.configure_argument(
        "f", "file", has_value=True, example_value="/etc/aasd.ini"
    )
    parser.configure_argument("h", "help")
    parser.configure_argument("v", "verbose")
    parser.configure_argument("d", "debug")

    # Parsowanie argumentów
    parser.parse_arguments()

    # Wyświetlenie przetworzonych argumentów
    print("Parsed arguments:")
    for arg, value in parser.args.items():
        print(f"{arg}: {value}")

    print(parser.get_option("verbose") is None)
    print(parser._data)
    print(parser.dump())


# #[EOF]#######################################################################
