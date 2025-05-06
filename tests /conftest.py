# tests/conftest.py

import sys
import os

# 1) S’assurer que la racine du projet est dans sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 2) Injecter une clé OpenAI factice pour éviter l’erreur d’API key
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

import shutil
import pytest
from fastapi.testclient import TestClient

# 3) Maintenant que PYTHONPATH et OPENAI_API_KEY sont OK, on importe le backend
from backend.main import app, UPLOAD_DIR

# 4) Créer un client TestClient pour simuler les requêtes HTTP
client = TestClient(app)

# 5) Fixture automatique pour nettoyer le dossier d’upload avant et après chaque test
@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)

