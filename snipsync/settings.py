from enum import Enum

from snipsync.lexer import (
    ChoicesToken,
    EscapeCharToken,
    MirrorToken,
    PythonCodeToken,
    ShellCodeToken,
    TabStopToken,
    TransformationToken,
    VimLCodeToken,
    VisualToken,
)

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
