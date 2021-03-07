from snipsync.main import parse_config
from tests.conftest import ROOT_DIR


def test_parse_config():
    config_path = ROOT_DIR / 'data/config.cfg'
    cfg = parse_config(config_path)
    _ = None
    assert list(cfg['snip'].keys()) == ['SHELL', 'PYTHON']