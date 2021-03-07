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
templates = "$HOME/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates"
ultisnips = "$HOME/dev/binx/vim-config/UltiSnips"
init = yes

[FILES]
files = [
    sh.snippets
    python.snippets
]
"""
