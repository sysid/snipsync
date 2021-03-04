import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union, Iterable, Dict

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
        text = snip._value

        intelij_vars = XmlSnippet.create_variables(text)

        xml_text = XmlSnippet.replace_tabstop(intelij_vars, text)
        xml_text = XmlSnippet.replace_mirror(intelij_vars, xml_text)

        snip_attr = dict(
            name=snip.trigger,
            value=xml_text,
            description=snip._description,
            toReformat="true",
            toShortenFQNames="true",
        )
        template = ET.Element("template", attrib=snip_attr)

        for _, var_attr in intelij_vars.items():
            variable = ET.SubElement(template, 'variable', attrib=var_attr)

        context_tag = ET.SubElement(template, "context")
        for c in context:
            option = ET.SubElement(
                context_tag, "option", attrib=dict(name=c, value="true")
            )
        return template

    @staticmethod
    def replace_mirror(intelij_vars, text):
        _MIRROR = re.compile(r"\$(\d+)")
        _NUMBER = re.compile(r"\$(\d+)")

        mo = _MIRROR.search(text)
        n = 0
        while mo:
            match = mo.group()
            token_number = int(_NUMBER.findall(match)[0])
            _log.debug(f"{n}: {mo}: match: {match}, token_number: {token_number}")

            var_attrs = intelij_vars.get(token_number)
            if var_attrs is not None:
                text = mo.string[: mo.start()] + f"${var_attrs['name']}$" + mo.string[mo.end():]
            else:
                # this is required to ensure finite loop (search pattern must be removed from text)
                text = mo.string[: mo.start()] + f"_parameter_to_change_" + mo.string[mo.end():]

            mo = _MIRROR.search(text)
            n += 1
        text = text.replace(r'\$', '$$')  # adjust dollar escaping to intelij
        return text

    @staticmethod
    def replace_tabstop(intelij_vars, text):
        # mo = re.search("\\${\\d+[:}].*?}", text)
        _TABSTOP = re.compile(r"\${\d+[:]?.*?}")
        _NUMBER = re.compile(r"\${(\d+).*?}")
        _MIRROR = re.compile(r"\$(\d+)")

        mo = _TABSTOP.search(text)
        n = 0
        while mo:
            match = mo.group()
            token_number = int(_NUMBER.findall(match)[0])
            _log.debug(f"{n}: {mo}: match: {match}, token_number: {token_number}")

            var_attrs = intelij_vars.get(token_number)
            if var_attrs is not None:
                text = mo.string[: mo.start()] + f"${var_attrs['name']}$" + mo.string[mo.end():]
            else:
                # this is required to ensure finite loop (search pattern must be removed from text)
                text = mo.string[: mo.start()] + f"_parameter_to_change_" + mo.string[mo.end():]

            mo = _TABSTOP.search(text)
            n += 1
        text = text.replace(r'\$', '$$')  # adjust dollar escaping to intelij
        return text

    @staticmethod
    def create_variables(text: str) -> Dict:
        offset = Position(line=0, col=0)
        _INDENT = re.compile(r"^[ \t]*")
        indent = _INDENT.match("").group(0)
        tokens = list(tokenize(text, indent, offset, ALLOWED_TOKENS))
        # create the parameters
        intelij_params = dict()
        for token in tokens:
            if not isinstance(token, TabStopToken):
                continue
            param_name = f"param{token.number}"
            intelij_params[token.number] = dict(
                name=param_name,
                expression="",
                defaultValue=token.initial_text,
                alwaysStopAt="true",
            )
            # variable = ET.SubElement(template, 'variable', attrib=var_attr)
        return intelij_params

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
