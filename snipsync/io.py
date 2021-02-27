from pathlib import Path
from typing import List

from snipsync.ultisnip import UltiSnipsFileSource


def read_ultisnips(file: Path) -> str:
    source = UltiSnipsFileSource()
    # with open(file, 'r') as f:
    #     return f.readlines()
    with open(file, "r", encoding="utf-8") as f:
        return f.read()
