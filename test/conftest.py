import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from snipsync.ultisnip import UltiSnipsFileSource, UltiSnipsSnippetDefinition


@pytest.fixture()
def xmlsnips_file():
    return Path("../data/user.xml")


@pytest.fixture()
def ultisnips_file():
    return Path("../data/sh.snippets")


@pytest.fixture()
def ultisnips(ultisnips_file):
    with open(ultisnips_file, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture()
def arr_snip_value():
    return '${1:arr}=(\n\t"foo"\n\t"bar"\n)\necho "Array: ${${0:$1}[@]}"\necho "Index: ${!${0:$1}[@]}"\necho "Size: ${#${0:$1}[@]}"\nfor el in "${${0:$1}[@]}"; do\n\techo $el\ndone'


@pytest.fixture()
def snip_xml():
    return ET.XML(
        """
          <template name="case" value="case &quot;$1&quot; in&#10;    $actuator$)&#10;        ActuatorAgent&#10;        ;;&#10;    $debugger$)&#10;        Debugger&#10;        ;;&#10;    *)&#10;        echo &quot;Usage: {$actuator$|$debugger$}&quot;&#10;        exit 1&#10;esac" description="" toReformat="true" toShortenFQNames="true">
            <variable name="actuator" expression="" defaultValue="" alwaysStopAt="true" />
            <variable name="debugger" expression="" defaultValue="" alwaysStopAt="true" />
            <context>
              <option name="Bash" value="true" />
              <option name="SHELL_SCRIPT" value="true" />
            </context>
          </template>
        """
    )


@pytest.fixture()
def arr_snip(ultisnips) -> UltiSnipsSnippetDefinition:
    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(ultisnips, ultisnips_file)
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    return next(data)[1][0]
