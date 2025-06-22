import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from httpx import AsyncClient, ASGITransport

import ia_sarah.core.interfaces.api.server as server
import ia_sarah.core.use_cases.controllers as controllers
import ia_sarah.core.adapters.utils.config_manager as cm


@pytest.mark.asyncio
async def test_api_crud(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    controllers.init_app()
    transport = ASGITransport(app=server.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # create
        resp = await client.post("/students", json={"nome": "Ana", "email": "ana@test.com"})
        assert resp.status_code == 201
        aluno_id = resp.json()["id"]

        # list
        resp = await client.get("/students")
        assert resp.status_code == 200
        data = resp.json()
        assert any(a["id"] == aluno_id for a in data)

        # get
        resp = await client.get(f"/students/{aluno_id}")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Ana"

        # delete
        resp = await client.delete(f"/students/{aluno_id}")
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_config_api(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    cm.CONFIG_FILE = tmp_path / "conf.json"
    controllers.init_app()
    transport = ASGITransport(app=server.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/config")
        assert resp.status_code == 200
        assert resp.json() == cm.DEFAULT_CONFIG

        resp = await client.post("/theme", json={"theme": "flat"})
        assert resp.status_code == 204
        assert cm.load_theme() == "flat"

        resp = await client.get("/theme")
        assert resp.status_code == 200
        assert resp.json()["theme"] == "flat"

        resp = await client.post("/config", json={"foo": "bar"})
        assert resp.status_code == 204
        assert cm.load_config()["foo"] == "bar"
