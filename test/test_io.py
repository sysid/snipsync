import xml.etree.ElementTree as ET

import pytest

from snipsync.io import read_ultisnips, XmlSnippet


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
        assert self.xml.exists('xxx')

    def test_not_exists_zzz(self):
        assert not self.xml.exists('zzz')

    def test_create_xml(self, arr_snip):
        snip_xml = XmlSnippet.create_xml(arr_snip)
        ET.indent(snip_xml)  # pretty printing
        ET.dump(snip_xml)

    def test_insert_snip(self, arr_snip):
        snip_xml = self.xml.create_xml(arr_snip)
        self.xml.insert(snip_xml)

        assert self.xml.exists('arr')
        ET.indent(self.xml.et)
        ET.dump(self.xml.et)
