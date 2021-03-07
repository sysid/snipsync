import configparser
import json
import logging
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import List, Dict

import typer

from snipsync.settings import CONFIG_TEMPLATE
from snipsync.ultisnip import UltiSnipsFileSource
from snipsync.xml_snippet import XmlSnippet, read_ultisnips

_log = logging.getLogger(__name__)
app = typer.Typer(help="Awesome snippet synchronization from Ultisnips to Intelij")

APP_NAME = "snipsync"


@app.callback()
def setup(
        ctx: typer.Context,
):
    """ Global setup """
    app_dir = typer.get_app_dir(APP_NAME)
    ctx.obj = dict(
        app_dir=Path(app_dir),
        config_path=Path(app_dir) / "config.ini",
    )
    typer.echo(f"About to execute command: {ctx.invoked_subcommand}")


@app.command()
def dir(
        ctx: typer.Context,
):
    """
    Show the location of the configuration file
    """
    app_dir = ctx.obj.get("app_dir")
    config_path = ctx.obj.get("config_path")

    if not config_path.is_file():
        typer.echo(f"Config file {config_path} doesn't exist yet, creating...")
        Path(app_dir).mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as textfile:
            print(CONFIG_TEMPLATE, file=textfile)

    typer.edit(CONFIG_TEMPLATE, filename=config_path)
    typer.echo(f"Config file is: {config_path}")

    ctx.obj = parse_config(config_path, ctx)
    _ = None


def parse_config(config_path) -> Dict:
    cfg = dict()
    config = configparser.ConfigParser(strict=True)
    config.read(config_path)

    # ultisnips = Path(config['DEFAULT']['ultisnips']).resolve()
    # live_templates = Path(config['DEFAULT']['live_templates']).resolve()

    # cfg['ultisnips'] = ultisnips
    # cfg['live_templates'] = live_templates
    cfg['init'] = config['GLOBAL'].getboolean('init', fallback=False)
    cfg['snip'] = defaultdict(dict)

    for section in config.sections():
        if 'SNIP' not in section:
            continue
        type_ = section.split('.')[-1]
        cfg['snip'][type_]['source'] = config[section].get('ultisnips')
        cfg['snip'][type_]['target'] = config[section].get('live_templates')
    return cfg


@app.command()
def auto_sync(
        ctx: typer.Context,
        verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose"),
        save: bool = typer.Option(False, "--save", "-s", help="save it to InteliJ"),
        context: List[str] = typer.Option(
            ..., "--context", "-c", help="scope/context in InteliJ"
        ),
        ultisnip_file: Path = typer.Argument(..., help="ultisnips source", exists=True),
        xmlsnip_file: Path = typer.Argument(..., help="xmlsnip target", exists=True),
):
    """
    Synchronizes Ultisnip snippets to InteliJ Live Templates
    """
    typer.secho(f"-M- Syncing {ultisnip_file}", fg="green")

    ultisnips = ctx.obj.get("ultisnips")
    templates = ctx.obj.get("templates")
    files = ctx.obj.get("files")

    xml_snippets = XmlSnippet(xmlsnip_file)

@app.command()
def sync(
        ctx: typer.Context,
        verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose"),
        save: bool = typer.Option(False, "--save", "-s", help="save it to InteliJ"),
        context: List[str] = typer.Option(
            ..., "--context", "-c", help="scope/context in InteliJ"
        ),
        ultisnip_file: Path = typer.Argument(..., help="ultisnips source", exists=True),
        xmlsnip_file: Path = typer.Argument(..., help="xmlsnip target", exists=True),
):
    """
    Synchronizes Ultisnip snippets to InteliJ Live Templates
    """
    typer.secho(f"-M- Syncing {ultisnip_file}", fg="green")

    ultisnips = ctx.obj.get("ultisnips")
    templates = ctx.obj.get("templates")
    files = ctx.obj.get("files")

    xml_snippets = XmlSnippet(xmlsnip_file)

    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(read_ultisnips(ultisnip_file), source)
    for snippet_type, (snippet_definition,) in data:
        # xml_snippet = xml_snippets.create_xml(snippet_definition)
        xml_snippets.upsert(snippet_definition, context=context)

    if verbose:
        ET.indent(xml_snippets.et)
        ET.dump(xml_snippets.et)

    # p = Path(TEMPLATES) / 'user.xml'  # TODO: save copy and bkp original
    p = xmlsnip_file
    if save:
        typer.secho(f"-M- Saving to {p}", fg="green")
        ET.indent(xml_snippets.et)
        xml_snippets.et.write(p)
    else:
        typer.secho(f"-W- Not saved to {p}", fg="cyan")


if __name__ == "__main__":
    log_fmt = (
        r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
    )
    logging.basicConfig(format=log_fmt, level=logging.DEBUG)
    app()
