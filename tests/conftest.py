# tests/conftest.py

import os
import sys
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# 1) Fourni une clé factice pour l'API OpenAI (pour que backend.main puisse s'importer sans erreur)
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

# 2) Assure-toi que Python trouve le package `backend`
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

# 3) Importe l'application FastAPI et le répertoire d'uploads
from backend.main import app, UPLOAD_DIR  # noqa: E402

# 4) Définit la fixture `client` que tes tests utiliseront
@pytest.fixture
def client():
    """
    Fournit un TestClient(app) pour appeler tes endpoints.
    Usage : def test_xxx(client): ...
    """
    return TestClient(app)

# 5) Fixture autouse pour nettoyer UPLOAD_DIR avant et après chaque test
@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    if os.path.isdir(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)

