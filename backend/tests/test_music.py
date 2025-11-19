from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_music():
    """Testa a criação de uma música (POST /api/musics/)"""
    
    payload = {
        "title": "Balada Nova",
        "description": "Um novo hit",
        "artist_id": 1,
        "duration": "3:45",
        "posted_at": "2025-09-20"
    }

    response = client.post("/api/musics/", json=payload)

    # Valida se a rota realmente existe
    assert response.status_code != 404, (
        f"\n❌ ERRO 404 — A rota /api/musics/ não foi encontrada.\n"
        f"Resposta do servidor: {response.json()}"
    )

    # Valida se a requisição foi bem-sucedida
    assert response.status_code == 200, (
        f"\n❌ Código inesperado: {response.status_code}\n"
        f"Resposta: {response.json()}"
    )

    data = response.json()

    # Verificações de dados retornados
    assert data.get("title") == payload["title"], "O título retornado está incorreto."
    assert data.get("artist_id") == payload["artist_id"], "O artist_id retornado está incorreto."
    assert "id" in data, "A resposta não contém o campo 'id'."
