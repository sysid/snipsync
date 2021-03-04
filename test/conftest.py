import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

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
def snip2_xml():
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


# select shell arr snippet
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


@pytest.fixture()
def intelij_vars() -> Dict:
    return {
        0: dict(
            name='param0',
            expression="",
            defaultValue='default0',
            alwaysStopAt="true",
        ),
        1: dict(
            name='param1',
            expression="",
            defaultValue='default1',
            alwaysStopAt="true",
        ),
        2: dict(
            name='param2',
            expression="",
            defaultValue='default2',
            alwaysStopAt="true",
        ),
    }


# Attention: TABS must be explicit
@pytest.fixture()
def snippets():
    return (
        """\
            snippet arr "array template"
            ${1:arr}=(
            \t"foo"
            \t"bar"
            )
            echo "Array: ${${0:$1}[@]}"
            echo "Index: ${!${0:$1}[@]}"
            echo "Size: ${#${0:$1}[@]}"
            for el in "${${0:$1}[@]}"; do
            \techo $el
            done
            endsnippet
        """,
        """\
            snippet req "require a module" b
            let ${1} = require('${0:$1}');
            endsnippet
        """,
        """\
            snippet read
            read -p "Enter: " ${1:input}
            echo "-M- \\$$1"
            endsnippet
        """,
        """\
            snippet if "if ... then (if)"
            if ${2:[[ ${1:condition} ]]}; then
                    ${0:#statements}
            fi
            endsnippet
        """,
        """\
            snippet -z
            # Assert there is at least one tag provided
            test -z "\$${1:var}" && echo "-E- tag required." 1>&2 && exit 1
            endsnippet
        """
    )

# print(dedent(snippets[0]))
# print(snippets[0])
