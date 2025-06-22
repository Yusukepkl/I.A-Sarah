import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import utils.config_manager as cm


def test_config_crud(tmp_path):
    cm.CONFIG_FILE = tmp_path / "conf.json"
    cm.save_config({"theme": "flat"})
    data = cm.load_config()
    assert data["theme"] == "flat"
    cm.save_config({"theme": "dark"})
    assert cm.load_theme() == "dark"
    cm.delete_config()
    assert cm.CONFIG_FILE.exists() is False
