import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union, Iterable

from snipsync.lexer import tokenize, TabStopToken
from snipsync.position import Position
from snipsync.settings import ALLOWED_TOKENS
from snipsync.ultisnip import UltiSnipsSnippetDefinition, UltiSnipsFileSource

_log = logging.getLogger(__name__)


def read_ultisnips(file: Path) -> str:
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


class XmlSnippet:
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

        self.et = self.read_xmlsnips(path)

    @staticmethod
    def read_xmlsnips(file: Path) -> ET:
        return ET.parse(file)

    def exists(self, snip: str):
        snips = self.et.findall(f"template[@name='{snip}']")
        return len(snips) > 0

    @staticmethod
    def create_xml(snip: UltiSnipsSnippetDefinition, context: Iterable[str]) -> ET.Element:
        offset = Position(line=0, col=0)
        _INDENT = re.compile(r"^[ \t]*")
        text = snip._value
        indent = _INDENT.match("").group(0)
        tokens = list(tokenize(text, indent, offset, ALLOWED_TOKENS))

        # create the parameters
        intelij_params = dict()
        for token in tokens:
            if not isinstance(token, TabStopToken):
                continue
            param_name = f"param{token.number}"
            intelij_params[param_name] = dict(
                name=param_name,
                expression="",
                defaultValue=token.initial_text,
                alwaysStopAt="true",
            )
            # variable = ET.SubElement(template, 'variable', attrib=var_attr)

        # mo = re.search("\\${\\d+[:}].*?}", text)
        _TABSTOP = re.compile(r"\${\d+[:}].*?}")
        mo = _TABSTOP.search(text)
        n = 0
        while mo:
            print(f"{n}: {mo}")
            # text = re.sub("\\${\\d+[:}].*?}", lambda mo: f"{n}.....", text)
            text = mo.string[: mo.start()] + f"...{n}..." + mo.string[mo.end():]
            match = mo.group()
            print(f"match: {match}")

            print(text)
            mo = _TABSTOP.search(text)
            n += 1

        snip_attr = dict(
            name=snip.trigger,
            value=snip._value,
            description=snip._description,
            toReformat="true",
            toShortenFQNames="true",
        )
        template = ET.Element("template", attrib=snip_attr)


        context_tag = ET.SubElement(template, "context")
        for c in context:
            option = ET.SubElement(
                context_tag, "option", attrib=dict(name=c, value="true")
            )
        return template

    def insert(self, snip: ET.Element):
        root = self.et.getroot()
        root.insert(len(root), snip)

    def update(self, snip: ET.Element):
        name = snip.attrib.get('name')
        snips = self.et.findall(f"template[@name='{name}']")
        assert len(snips) == 1, f"{name} ambiguous or non-existent, cannot update."

    def upsert(self, snip: UltiSnipsSnippetDefinition, context: Iterable[str]):
        snip_xml = self.create_xml(snip, context=context)
        if self.exists(snip.trigger):
            root = self.et.getroot()
            snips = self.et.findall(f"template[@name='{snip.trigger}']")
            assert len(snips) == 1, f"{snip.trigger} ambiguous, cannot update."
            root.remove(snips[0])
            _log.info(f"Removed snippet: {snip.trigger}")
        self.insert(snip_xml)
        _log.info(f"Inserted snippet: {snip.trigger}")


if __name__ == '__main__':
    p = Path("../data/sh.snippets")
    with open(p, "r", encoding="utf-8") as f:
        ultisnips = f.read()
    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(ultisnips, p)
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    _ = next(data)[1][0]
    arr_snip = next(data)[1][0]
    snip_xml = XmlSnippet.create_xml(arr_snip, context=('Bash', 'SHELL_SCRIPT'))
    assert len(snip_xml.findall(".//option[@name='Bash']")) == 1
    assert len(snip_xml.findall(".//option[@name='SHELL_SCRIPT']")) == 1
    ET.indent(snip_xml)  # pretty printing
    ET.dump(snip_xml)
