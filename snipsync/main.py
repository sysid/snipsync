import configparser
import json
import logging
import xml.etree.ElementTree as ET
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Dict, List

import typer

from snipsync.environment import (
    CONFIG_TEMPLATE,
    INTELIJ_CONFIG_DIR,
    USER_XML_TEMPLATE,
    IdeEnum,
)
from snipsync.ultisnip import UltiSnipsFileSource
from snipsync.xml_snippet import XmlSnippet, read_ultisnips

_log = logging.getLogger(__name__)
app = typer.Typer(help="Awesome snippet synchronization from Ultisnips to Intelij")

APP_NAME = "snipsync"


@app.callback()
def setup(
    ctx: typer.Context,
):
    """Global setup"""
    app_dir = typer.get_app_dir(APP_NAME)
    ctx.obj = dict(
        app_dir=Path(app_dir),
        config_path=Path(app_dir) / "config.cfg",
    )
    # typer.echo(f"About to execute command: {ctx.invoked_subcommand}")


@app.command()
def dir(
    ctx: typer.Context,
):  # pragma: no cover
    """
    Open/create configuration file for potential adjustment.
    """
    app_dir = ctx.obj.get("app_dir")
    config_path = ctx.obj.get("config_path")

    if not config_path.is_file():
        typer.echo(f"Config file {config_path} doesn't exist yet, creating...")
        Path(app_dir).mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as textfile:
            print(CONFIG_TEMPLATE, file=textfile)

    typer.edit(CONFIG_TEMPLATE, filename=config_path)
    typer.echo(f"-M- Config file is: {config_path}")
    _ = None


def parse_config(config_path) -> Dict:
    cfg = dict()
    config = configparser.ConfigParser(strict=True, allow_no_value=True)
    config.read(config_path)

    # ultisnips = Path(config['DEFAULT']['ultisnips']).resolve()
    # live_templates = Path(config['DEFAULT']['live_templates']).resolve()

    cfg["init"] = config["GLOBAL"].getboolean("init", fallback=False)

    # if live_templates_path := config["DEFAULT"].get("live_templates_path") is None:
    #     live_templates_path = f"{INTELIJ_CONFIG_DIR}/jba_config/templates"
    cfg["live_templates_path"] = Path(
        config["DEFAULT"].get("live_templates_path")
    ).expanduser()
    cfg["ultisnips_path"] = Path(config["DEFAULT"].get("ultisnips_path")).expanduser()

    cfg["snip"] = defaultdict(dict)

    for section in config.sections():
        if "SNIP" not in section:
            continue
        type_ = section.split(".")[-1]
        cfg["snip"][type_]["source"] = config[section].get("ultisnips")
        cfg["snip"][type_]["target"] = config[section].get("live_templates")
        contexts = config[section].get("live_templates_contexts")
        cfg["snip"][type_]["contexts"] = json.loads(contexts)
    return cfg


def check_intellij_installation(p: Path) -> bool:
    """
    Check whether valid and latest InteliJ IDE is target for user.xml
    :param p: path to the user.xml
    :raises if not valid or outdated
    """
    if not p.is_dir():
        typer.secho(f"{p} is not a valid directory.", color=typer.colors.RED)
        raise typer.Abort()

    for ide in IdeEnum:
        if ide.value.lower() in str(p).lower():
            break
    else:
        typer.secho(
            f"Given path {p} invalid. Must contain one of: {[ide.value for ide in IdeEnum]}",
            color=typer.colors.RED,
        )
        raise typer.Abort()

    root = f"{str(p).split('JetBrains')[0]}JetBrains"
    GLOB = f"*"

    dirs = [d for d in Path(root).glob(GLOB) if d.is_dir()]
    dirs = [d for d in dirs if ide.value in str(d)]
    if len(dirs) == 0:
        typer.secho(
            f"No installation {ide.value} found in {root}", color=typer.colors.RED
        )
        raise typer.Abort()

    latest_installation = sorted(dirs)[-1]

    if latest_installation not in p.parents:
        typer.secho(
            f"There seems to be a newer version of Intellij: {latest_installation} ",
            color=typer.colors.RED,
        )
        typer.secho(
            f"Please check your snipsync configuration.", color=typer.colors.RED
        )
        raise typer.Abort()

    return True  # for pytest assertions


@app.command()
def auto_sync(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose"),
    save: bool = typer.Option(False, "--save", "-s", help="save it to InteliJ"),
):
    """
    Synchronizes Ultisnip snippets to InteliJ Live Templates controlled by config-file
    """
    app_dir = ctx.obj.get("app_dir")
    config_path = ctx.obj.get("config_path")

    if not config_path.exists():
        typer.secho(f"-E- No config found: {config_path}", fg="red")
        typer.secho(f"-E- Run command <dir> first to create configuration.", fg="red")
        raise typer.Abort()

    typer.secho(f"-M- Configuration: {config_path}", fg=None)
    config = parse_config(config_path)
    check_intellij_installation(config.get("live_templates_path"))

    # TODO: expand to work for arbitrary xml file not only user.xml
    user_xml_template_path = config.get("live_templates_path") / "user.xml"
    if config.get("init") or not Path(user_xml_template_path).is_file():
        typer.secho(f"-M- Initializing : {user_xml_template_path}", fg=None)

        with open(user_xml_template_path, "w") as textfile:
            print(USER_XML_TEMPLATE, file=textfile)

    for type_, v in config.get("snip").items():
        source = Path(v.get("source")).expanduser()
        target = Path(v.get("target")).expanduser()
        contexts = v.get("contexts")
        if verbose:
            typer.secho(f"-D- Syncing {source} -> {target}", fg=None)

        xml_snippets = live_template_upsert(
            context=contexts, ultisnip_file=source, xmlsnip_file=target
        )
        ET.indent(xml_snippets.et)
        xml_snippets.et.write(target)

        typer.secho(f"-M- Done snippets for {type_} -> {target}", fg=None)

    typer.secho(f"-M- Done.", fg="green")


@app.command()
def sync(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose"),
    save: bool = typer.Option(False, "--save", "-s", help="save it to InteliJ"),
    context: List[str] = typer.Option(
        ..., "--context", "-c", help="scope/context in InteliJ"
    ),
    ultisnip_file: Path = typer.Argument(..., help="ultisnips source", exists=False),
    xmlsnip_file: Path = typer.Argument(..., help="xmlsnip target", exists=False),
):
    """
    Synchronizes Ultisnip snippets file to InteliJ Live Templates and sets the corresponding Live Template context
    """
    ultisnip_file = ultisnip_file.expanduser()
    if not ultisnip_file.exists():
        typer.secho(f"-E- Invalid UltiSnips source: {ultisnip_file}", fg="red")
        raise typer.Abort()

    check_intellij_installation(xmlsnip_file.parent)
    xmlsnip_file = xmlsnip_file.expanduser()

    typer.secho(f"-M- Syncing {ultisnip_file} -> {xmlsnip_file}", fg=None)

    # TODO: what happens if xml does not exist
    # TODO: init xml option
    xml_snippets = live_template_upsert(context, ultisnip_file, xmlsnip_file)

    if verbose or not save:
        ET.indent(xml_snippets.et)
        ET.dump(xml_snippets.et)

    # p = Path(TEMPLATES) / 'user.xml'  # TODO: save copy and bkp original
    if save:
        typer.secho(f"-M- Saving to {xmlsnip_file}", fg=None)
        ET.indent(xml_snippets.et)
        xml_snippets.et.write(xmlsnip_file)
        typer.secho(f"-M- Done.", fg="green")
    else:
        typer.secho(
            f"-W- This is a test run. LiveTemplate file has NOT been updated yet.",
            fg="cyan",
        )
        typer.secho(
            f"-W- Run with 'save' flag in order to really update {xmlsnip_file}.",
            fg="cyan",
        )


def live_template_upsert(
    context: List[str], ultisnip_file: Path, xmlsnip_file: Path
) -> XmlSnippet:
    xml_snippets = XmlSnippet(xmlsnip_file)

    source = UltiSnipsFileSource()
    data = source.parse_snippet_file(read_ultisnips(ultisnip_file), source)

    for snippet_type, (snippet_definition,) in data:
        xml_snippets.upsert(snippet_definition, context=context)
    return xml_snippets


if __name__ == "__main__":
    log_fmt = (
        r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
    )
    logging.basicConfig(format=log_fmt, level=logging.DEBUG)
    app()
