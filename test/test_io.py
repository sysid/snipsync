import xml.etree.ElementTree as ET

import pytest

from snipsync.xml_snippet import read_ultisnips, XmlSnippet


def test_read_ultisnips(ultisnips_file):
    data = read_ultisnips(ultisnips_file)
    print(data)


def test_xxx(snip_xml):
    print(snip_xml)


def test_read_xmlsnips(xmlsnips_file):
    et = XmlSnippet.read_xmlsnips(xmlsnips_file)
    ET.dump(et)


class TestXmlSnippet:
    @pytest.fixture(autouse=True)
    def xml(self, xmlsnips_file):
        self.xml = XmlSnippet(xmlsnips_file)

    def test_exists_xxx(self):
        assert self.xml.exists("xxx")

    def test_not_exists_zzz(self):
        assert not self.xml.exists("zzz")

    def test_create_xml(self, arr_snip):
        snip_xml = XmlSnippet.create_xml(arr_snip, context=('Bash', 'SHELL_SCRIPT'))
        assert len(snip_xml.findall(".//option[@name='Bash']")) == 1
        assert len(snip_xml.findall(".//option[@name='SHELL_SCRIPT']")) == 1
        ET.indent(snip_xml)  # pretty printing
        ET.dump(snip_xml)
        # assert snips[0].attrib.get('value') == 'xxx'

    def test_insert_snip(self, arr_snip):
        snip_xml = self.xml.create_xml(arr_snip, context=('Bash', 'SHELL_SCRIPT'))
        self.xml.insert(snip_xml)

        assert self.xml.exists("arr")
        ET.indent(self.xml.et)
        ET.dump(self.xml.et)

    def test_upsert_snip_new(self, arr_snip):
        self.xml.upsert(arr_snip, context=('Bash', 'SHELL_SCRIPT'))

        assert self.xml.exists("arr")
        ET.indent(self.xml.et)
        ET.dump(self.xml.et)

    def test_upsert_snip_existing(self, arr_snip):
        # given an existing snippet
        arr_snip._trigger = 'xxx'
        assert not self.xml.exists("arr")
        assert self.xml.exists("xxx")

        # when value of snippet changes
        arr_snip._value = 'xxx'
        self.xml.upsert(arr_snip, context=('Bash', 'SHELL_SCRIPT'))

        # then: snippet has been updated
        snips = self.xml.et.findall("template[@name='xxx']")
        assert snips[0].attrib.get('value') == 'xxx'
        ET.indent(self.xml.et)
        ET.dump(self.xml.et)
