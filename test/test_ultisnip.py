from snipsync.lexer import tokenize
from snipsync.position import Position
from snipsync.settings import ALLOWED_TOKENS
from snipsync.ultisnip import UltiSnipsFileSource, UltiSnipsSnippetDefinition


# CHECK = re.compile(r"^\${\d+[:}]")

# read snippet file
def test_ultisnips_file_source(ultisnips, ultisnips_file):
    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(ultisnips, ultisnips_file)
    snippet = next(data)[1][0]
    assert isinstance(snippet, UltiSnipsSnippetDefinition)
    assert snippet._value == """let ${1} = require('${0:$1}');"""
    _ = None


def test_tokenize():
    text = """let ${1} = require('${0:$1}');"""
    offset = Position(line=0, col=0)
    indent = 0
    t1, t2, t3 = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
    _ = None
    # assert t2.initial_text == '$1'


def test_tokenize2():
    text = '${1:arr}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${${0:$1}[@]}"\necho "Index: ${!${0:$1}[@]}"\necho "Size: ${#${0:$1}[@]}"\nfor el in "${${0:$1}[@]}"; do\n\techo $el\ndone'
    offset = Position(line=0, col=0)
    indent = 0

    t = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
    assert t[0].number == 1
    assert t[0].initial_text == 'arr'
    assert t[4].number == 0
    assert t[4].initial_text == '$1'
    _ = None
