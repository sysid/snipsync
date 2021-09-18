################################################################################
# Environment
################################################################################
from enum import Enum

import platform
import sys
from pathlib import Path
from pydantic import BaseSettings

from snipsync.lexer import EscapeCharToken, VisualToken, TransformationToken, ChoicesToken, TabStopToken, MirrorToken, \
    PythonCodeToken, VimLCodeToken, ShellCodeToken

ROOT_DIR = Path(__file__).parent.absolute()

# https://www.jetbrains.com/help/idea/directories-used-by-the-ide-to-store-settings-caches-plugins-and-logs.html#config-directory
plt = platform.system()
if plt == "Windows":
    # print("Your system is Windows")
    INTELIJ_CONFIG_DIR = r"%APPDATA%\JetBrains"
elif plt == "Linux":
    # print("Your system is Linux")
    INTELIJ_CONFIG_DIR = r"~/.config/JetBrains/"
elif plt == "Darwin":
    # print("Your system is MacOS")
    INTELIJ_CONFIG_DIR = r"~/Library/Application Support/JetBrains"
else:
    print("Unidentified system")
    sys.exit(1)


CONFIG_TEMPLATE = """\
[DEFAULT]
live_templates_path = ~/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates
ultisnips_path = ~/dev/binx/vim-config/UltiSnips

[GLOBAL]
init = yes

[SNIP.SHELL]
ultisnips = %(ultisnips_path)s/sh.snippets
live_templates = %(live_templates_path)s/user.xml
live_templates_contexts = ["SHELL_SCRIPT", "Bash"]

[SNIP.PYTHON]
ultisnips = %(ultisnips_path)s/python.snippets
live_templates = %(live_templates_path)s/user.xml
live_templates_contexts = ["Python"]
"""

USER_XML_TEMPLATE = """\
<templateSet group="user">
</templateSet>
"""


ALLOWED_TOKENS = [
    EscapeCharToken,
    VisualToken,
    TransformationToken,
    ChoicesToken,
    TabStopToken,
    MirrorToken,
    PythonCodeToken,
    VimLCodeToken,
    ShellCodeToken,
]


class IdeEnum(Enum):
    PYCHARM = "PyCharm"
    WEBSTORM = "WebStorm"
    IDEAI = "IdeaI"
    GOLAND = "GoLand"


class Environment(BaseSettings):
    log_level: str = "INFO"


config = Environment()
_ = None
