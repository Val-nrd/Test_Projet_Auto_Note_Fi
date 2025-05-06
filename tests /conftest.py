# tests/conftest.py

import os
import sys
import shutil
import pytest

# ——————— Pose la clé OPENAI avant tout import de backend.main ———————
os.environ.setdefault("OPENAI_API_KEY", "test_key_for_pytest")

# ——————— Ajoute la racine du projet au PYTHONPATH ———————
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ——————— Maintenant on peut importer backend.main sans erreur ———————
from fastapi.testclient import TestClient
from backend.main import app, UPLOAD_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    # Avant chaque test : on recrée le dossier d'upload propre
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    # Après chaque test : on nettoie
    shutil.rmtree(UPLOAD_DIR)

