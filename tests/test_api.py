import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

import ia_sarah.core.interfaces.api.server as server
import ia_sarah.core.use_cases.controllers as controllers
import ia_sarah.core.adapters.utils.config_manager as cm


def test_api_crud(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    controllers.init_app()
    client = TestClient(server.app)

    # create
    resp = client.post("/students", json={"nome": "Ana", "email": "ana@test.com"})
    assert resp.status_code == 201
    aluno_id = resp.json()["id"]

    # list
    resp = client.get("/students")
    assert resp.status_code == 200
    data = resp.json()
    assert any(a["id"] == aluno_id for a in data)

    # get
    resp = client.get(f"/students/{aluno_id}")
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Ana"

    # delete
    resp = client.delete(f"/students/{aluno_id}")
    assert resp.status_code == 204


def test_config_api(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    cm.CONFIG_FILE = tmp_path / "conf.json"
    controllers.init_app()
    client = TestClient(server.app)

    resp = client.get("/config")
    assert resp.status_code == 200
    assert resp.json() == {}

    resp = client.post("/theme", json={"theme": "flat"})
    assert resp.status_code == 204
    assert cm.load_theme() == "flat"

    resp = client.get("/theme")
    assert resp.status_code == 200
    assert resp.json()["theme"] == "flat"

    resp = client.post("/config", json={"foo": "bar"})
    assert resp.status_code == 204
    assert cm.load_config()["foo"] == "bar"
