# tests/conftest.py

import os
import sys
import shutil
import pytest
from fastapi.testclient import TestClient

# ————— 1) Injecter une clé OpenAI factice avant tout import de backend.main —————
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

# ————— 2) Ajouter la racine du projet au PYTHONPATH —————
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ————— 3) Ajouter aussi backend/ pour résoudre les imports relatifs —————
BACKEND_PATH = os.path.join(ROOT, "backend")
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# ————— 4) Importer l'app FastAPI et le dossier d'uploads —————
from backend.main import app, UPLOAD_DIR

# ————— 5) Préparer un client de test pour FastAPI —————
_test_client = TestClient(app)

@pytest.fixture
def client():
    """Client HTTP pour tester les routes FastAPI."""
    return _test_client

# ————— 6) Fixture pour nettoyer le dossier d’upload avant/après chaque test —————
@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)
