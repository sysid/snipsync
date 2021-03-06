from collections import defaultdict
from textwrap import dedent

import pytest

from snipsync.text import LineIterator
from snipsync.ultisnip import (
    UltiSnipsFileSource,
    UltiSnipsSnippetDefinition,
    _handle_snippet_or_global,
)


def test_ultisnips_file_source(ultisnips, ultisnips_file):
    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(ultisnips, ultisnips_file)
    snippet = next(data)[1][0]
    assert isinstance(snippet, UltiSnipsSnippetDefinition)
    assert snippet._value == """let ${1} = require('${0:$1}');"""
    _ = None


def test_create_snippet_definition_object(arr_snip_value, snippets):
    # given
    python_globals = defaultdict(list)
    data = dedent(snippets[0])
    lines = LineIterator(data)
    line = next(lines)
    current_priority = 0
    actions = {}
    context = None

    # when
    snippet, defintion = _handle_snippet_or_global(
        filename="test_filename",
        line=line,
        lines=lines,
        python_globals=python_globals,
        priority=current_priority,
        pre_expand=actions,
        context=context,
    )

    # then
    _ = None
    assert snippet == "snippet"
    assert defintion[0]._value == arr_snip_value
