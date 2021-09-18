import re

import pytest

from snipsync.environment import ALLOWED_TOKENS
from snipsync.lexer import EndOfTextToken, MirrorToken, TabStopToken, tokenize
from snipsync.position import Position


def test_tokenize():
    text = """let ${1} = require('${0:$1}');"""
    offset = Position(line=0, col=0)
    _INDENT = re.compile(r"^[ \t]*")
    indent = _INDENT.match("").group(0)
    t1, t2, t3 = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
    assert isinstance(t1, TabStopToken)
    assert isinstance(t2, TabStopToken)
    assert isinstance(t3, EndOfTextToken)
    assert t2.initial_text == "$1"


def test_tokenize2():
    text = """${1}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${$1[@]}" """
    offset = Position(line=0, col=0)
    _INDENT = re.compile(r"^[ \t]*")
    indent = _INDENT.match("").group(0)
    t = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
    assert isinstance(t[0], TabStopToken)
    assert isinstance(t[1], MirrorToken)
    assert isinstance(t[2], EndOfTextToken)
    _ = None


def test_tokenize3():
    text = '${1:arr}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${${0:$1}[@]}"\necho "Index: ${!${0:$1}[@]}"\necho "Size: ${#${0:$1}[@]}"\nfor el in "${${0:$1}[@]}"; do\n\techo $el\ndone'
    offset = Position(line=0, col=0)
    _INDENT = re.compile(r"^[ \t]*")
    indent = _INDENT.match("").group(0)

    t = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
    assert t[0].number == 1
    assert t[0].initial_text == "arr"
    assert t[4].number == 0
    assert t[4].initial_text == "$1"
    _ = None


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (
            """${1:arr}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${${0:$1}[@]}"\necho "Index: ${!${0:$1}[@]}"\necho "Size: ${#${0:$1}[@]}"\nfor el in "${${0:$1}[@]}"; do\n\techo $el\ndone""",
            ["${1:arr}", "${0:$1}", "${0:$1}", "${0:$1}", "${0:$1}"],
        ),
        ("""$1=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${$1[@]}" """, []),
        ("""${1}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${$1[@]}" """, ["${1}"]),
        (
            """test -z "\$${1:var}" & & echo "-E- tag required." 1 > & 2 & & exit 1""",
            ["${1:var}"],
        ),
    ],
)
def test_tabstop(input, output):
    # _TABSTOP = re.compile(r"\${\d+[:]?.*?(?<!})}")
    _TABSTOP = re.compile(r"\${\d+[:]?.*?}")
    print(_TABSTOP.findall(input))
    assert _TABSTOP.findall(input) == output


@pytest.mark.parametrize(
    ("input", "output"),
    [
        (
            "${1:arr}",
            ["1"],
        ),
        (
            "${0:$1}",
            ["0"],
        ),
        (
            "${111:$1}",
            ["111"],
        ),
        (
            "",
            [],
        ),
        (
            "${1}",
            ["1"],
        ),
    ],
)
def test_re(input, output):
    _NUMBER = re.compile(r"\${(\d+).*?}")
    print(_NUMBER.findall(input))
    assert _NUMBER.findall(input) == output
