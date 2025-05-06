# tests/conftest.py

import sys
import os

# 1) Ajouter la racine du projet au PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 2) Définir une clé OpenAI factice avant d’importer backend.main
#    (c’est impératif pour que backend.main puisse créer son client)
os.environ["OPENAI_API_KEY"] = "test_key_for_pytest"

import shutil
import pytest
from fastapi.testclient import TestClient

# 3) Maintenant que PYTHONPATH et OPENAI_API_KEY sont en place,
#    on peut importer l’API
from backend.main import app, UPLOAD_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    # Avant chaque test, on vide puis recrée le dossier d’uploads
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    # Après chaque test, on nettoie à nouveau
    shutil.rmtree(UPLOAD_DIR)
