import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

import typer

from snipsync.io import read_ultisnips, XmlSnippet
from snipsync.ultisnip import UltiSnipsFileSource

_log = logging.getLogger(__name__)
app = typer.Typer()

TEMPLATES = "/Users/Q187392/Library/Application Support/JetBrains/PyCharm2020.3/jba_config/templates"
ULTISNIPS = "/Users/Q187392/dev/binx/vim-config/UltiSnips"


@app.command()
def sync_to_intelij(
        verbose: bool = typer.Option(False, '--verbose', '-v', help="verbose"),
        save: bool = typer.Option(False, '--save', '-s', help="save it to InteliJ"),
        context: List[str] = typer.Option(..., '--context', '-c', help="scope/context in InteliJ"),
        ultisnip_file: Path = typer.Argument(default=None, help="ultisnips source", exists=True),
        xmlsnip_file: Path = typer.Argument(default=None, help="xmlsnip target", exists=True),
):
    typer.secho(f"-M- Syncing {ultisnip_file}", fg="green")
    xml_snippets = XmlSnippet(xmlsnip_file)

    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(read_ultisnips(ultisnip_file), source)
    for snippet_type, (snippet_definition,) in data:
        # xml_snippet = xml_snippets.create_xml(snippet_definition)
        xml_snippets.upsert(snippet_definition, context=context)

    if verbose:
        ET.indent(xml_snippets.et)
        ET.dump(xml_snippets.et)

    p = Path(TEMPLATES) / 'user.xml'
    if save:
        typer.secho(f"-M- Saving to {p}", fg='green')
        xml_snippets.et.write(p)
    else:
        typer.secho(f"-W- Not saved to {p}", fg='cyan')


if __name__ == "__main__":
    log_fmt = r'%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s'
    logging.basicConfig(format=log_fmt, level=logging.DEBUG)
    app()
