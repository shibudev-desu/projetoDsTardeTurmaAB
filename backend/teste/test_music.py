from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_music():
    """Testa a criação de uma música (POST /api/musics/)"""
    music = {
        "title": "Balada Nova",
        "description": "Um novo hit",
        "artist_id": 1,
        "duration": "3:45",
        "posted_at": "2025-09-20"
    }

    response = client.post("/api/musics/", json=music)
    
    if response.status_code == 404:
        print("\n Erro 404! A rota /api/musics/ não foi encontrada.")
        print("Resposta do servidor:", response.json())
        assert False, "Rota /api/musics/ não está registrada no app principal."
        return

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Balada Nova"
    assert data["artist_id"] == 1
    assert "id" in data
