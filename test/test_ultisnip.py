from snipsync.ultisnip import UltiSnipsFileSource, UltiSnipsSnippetDefinition


def test_UltisnipsFileSource(ultisnips, ultisnips_file):
    source = UltiSnipsFileSource()
    data = source._parse_snippet_file(ultisnips, ultisnips_file)
    snippet = next(data)[1][0]
    assert isinstance(snippet, UltiSnipsSnippetDefinition)
    assert snippet._value == """let ${1} = require('${0:$1}');"""
