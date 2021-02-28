from snipsync.lexer import EscapeCharToken, VisualToken, TransformationToken, ChoicesToken, TabStopToken, \
    MirrorToken, PythonCodeToken, VimLCodeToken, ShellCodeToken

# CHECK = re.compile(r"^\${\d+[:}]")

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
