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

CONFIG_TEMPLATE = """\
[DEFAULT]
live_templates = "$HOME/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates"
ultisnips = "$HOME/dev/binx/vim-config/UltiSnips"

[GLOBAL]
init = yes

[SHELL]
ultisnips = %(ultisnips)s/sh.snippets
live_templates = %(live_templates)s/sh.snippets
"""
