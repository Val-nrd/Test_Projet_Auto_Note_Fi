import io

def test_upload_pdf(client):
    dummy_pdf = io.BytesIO(b"%PDF-1.4\n%fake pdf content")
    dummy_pdf.name = "test.pdf"

    response = client.post(
        "/upload/",
        files={"files": ("test.pdf", dummy_pdf, "application/pdf")}
    )
    assert response.status_code == 200

    data = response.json()
    assert "extraits" in data
    assert len(data["extraits"]) == 1
    assert data["extraits"][0]["filename"] == "test.pdf"
