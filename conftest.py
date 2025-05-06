# tests/conftest.py

import os
import shutil
import pytest
from fastapi.testclient import TestClient
from backend.main import app, UPLOAD_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    # Avant chaque test, on vide le dossier d'uploads
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)
