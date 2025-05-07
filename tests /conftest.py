# tests/conftest.py

import os
import sys
import shutil
import pytest
from fastapi.testclient import TestClient

# 1) injecter une clé factice pour OPENAI
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

# 2) s'assurer que Python trouve le package `backend`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

BACKEND_PATH = os.path.join(ROOT, "backend")
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# 3) importer l'app FastAPI et le dossier d'uploads
from backend.main import app, UPLOAD_DIR

# 4) fixture pour obtenir le client HTTP
@pytest.fixture
def client():
    """Client HTTP pour tester les routes FastAPI."""
    return TestClient(app)

# 5) fixture pour nettoyer le dossier d’uploads avant/après chaque test
@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)
