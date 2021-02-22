#!/usr/bin/env python3

import subprocess


def notify(text: str, time="8000") -> str:
    subprocess.run(["notify-send", "-t", time, text])

def copy_to_clipboard(text: str) -> None:
    subprocess.run(["xclip", "-selection", "clipboard"],
                   input=text.encode("UTF-8"))
