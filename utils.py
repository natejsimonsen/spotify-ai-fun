import os


def clear_terminal():
    # for Windows
    if os.name == "nt":
        _ = os.system("cls")
    # for macOS and Linux
    else:
        _ = os.system("clear")
