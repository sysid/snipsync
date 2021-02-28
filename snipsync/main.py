from pathlib import Path

import xml.etree.ElementTree as ET
import typer

from snipsync.io import read_ultisnips, XmlSnippet
from snipsync.ultisnip import UltiSnipsFileSource

app = typer.Typer()


@app.command()
def xxx(
        create_png: bool = typer.Option(False, help="create a png."),
        ultisnip_file: Path = typer.Argument(default=None, help="ultisnips source", exists=True),
        xmlsnip_file: Path = typer.Argument(default=None, help="xmlsnip target", exists=True),
):
    typer.echo(f"Hello {ultisnip_file}")
    xml_snippets = XmlSnippet(xmlsnip_file)

    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(read_ultisnips(ultisnip_file), source)
    for snippet_type, (snippet_definition,) in data:
        # xml_snippet = xml_snippets.create_xml(snippet_definition)
        xml_snippets.upsert(snippet_definition)

    ET.indent(xml_snippets.et)
    ET.dump(xml_snippets.et)

    xml_snippets.et.write('./data/xxx.xml')

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
