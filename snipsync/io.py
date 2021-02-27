import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from snipsync.ultisnip import UltiSnipsSnippetDefinition


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
    def create_xml(snip: UltiSnipsSnippetDefinition) -> ET.Element:
        # root = ET.Element('templateSet')

        snip_attr = dict(
            name=snip.trigger,
            value=snip._value,
            description=snip._description,
            toReformat="true",
            toShortenFQNames="true",
        )
        template = ET.Element('template', attrib=snip_attr)

        # variables not used yet
        # var_attr = dict(
        #     name="xxx",
        #     expression="",
        #     defaultValue="",
        #     alwaysStopAt="true",
        # )
        # variable = ET.SubElement(template, 'variable', attrib=var_attr)

        context = ET.SubElement(template, 'context')
        option = ET.SubElement(context, 'option', attrib=dict(name="Bash", value="true"))
        option = ET.SubElement(context, 'option', attrib=dict(name="SHELL_SCRIPT", value="true"))
        return template

    def insert(self, snip: ET.Element):
        root = self.et.getroot()
        root.insert(len(root), snip)
