# tests/test_upload.py

import io

def test_upload_pdf(client):
    # Prépare un faux PDF en mémoire
    dummy_pdf = io.BytesIO(b"%PDF-1.4\n%fake pdf content")
    dummy_pdf.name = "test.pdf"

    # Envoie à l’endpoint /upload/
    response = client.post(
        "/upload/",
        files={"files": ("test.pdf", dummy_pdf, "application/pdf")}
    )
    assert response.status_code == 200

    data = response.json()
    # Vérifie que l’extrait est bien renvoyé
    assert "extraits" in data
    assert len(data["extraits"]) == 1
    assert data["extraits"][0]["filename"] == "test.pdf"
