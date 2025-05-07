# tests/conftest.py

import os
import sys
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# 1) mettre une clé factice pour que l’import de OpenAI dans backend.main ne plante pas
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

# 2) pointer pytest sur le dossier racine et sur backend/ pour que 'import backend.main' fonctionne
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

# 3) importer l’app et la constante UPLOAD_DIR
from backend.main import app, UPLOAD_DIR  # noqa: E402

# 4) fixture client
@pytest.fixture
def client():
    """Client HTTP pour tester les routes FastAPI."""
    return TestClient(app)

# 5) fixture cleanup pour vider le dossier d’uploads avant et après chaque test
@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    # supprime tout ce qui traîne
    if os.path.isdir(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)
