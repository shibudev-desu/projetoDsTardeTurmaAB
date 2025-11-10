# 🤝 Tutorial de Uso da API `/api/colab`

Rota para obter recomendações colaborativas (users-based) — sugere músicas que usuários parecidos gostaram.

## Endpoint
```
GET http://127.0.0.1:8000/api/colab
```

## Parâmetros

| Parâmetro    | Tipo     | Obrigatório | Descrição |
|--------------|----------|-------------|----------|
| `user_id`    | number   | ✅ Sim      | ID do usuário alvo (para quem geramos recomendações). |
| `limit`      | number   | Não         | Quantidade máxima de resultados retornados. Padrão: `10`. |
| `neigh_limit`| number   | Não         | Quantidade máxima de vizinhos (usuários similares) a considerar. Padrão: `200`. |

### Observações sobre erros
- 404 User not found — quando `user_id` não existe.
- 404 Music Ratings not found — quando o usuário não tem avaliações/likes.
- 404 Candidates not found / Jaccard failed / Tracker failed — quando não há dados suficientes para recomendar.
- 500 — erros internos; verifique logs ou resposta com detalhe para depuração.

## Exemplo de requisição
```bash
GET http://127.0.0.1:8000/api/colab?user_id=2&limit=10&neigh_limit=200
```

## Exemplo de resposta
```json
[
  {
    "id": 12,
    "title": "Música Recomendada A",
    "artist_id": 3,
    "score": 2.354
  },
  {
    "id": 7,
    "title": "Música Recomendada B",
    "artist_id": 5,
    "score": 1.880
  }
]
```

- `score`: valor numérico que representa a força da recomendação (soma ponderada de similaridades).

## Exemplo em React (useEffect)
```js
import { useEffect, useState } from "react";

export default function ColabList({ userId }) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    async function fetchColab() {
      const res = await fetch(`http://127.0.0.1:8000/api/colab?user_id=${userId}&limit=10`);
      const json = await res.json();
      setItems(json); // endpoint retorna um array direto
    }
    fetchColab();
  }, [userId]);

  return (
    <div>
      <h2>🤝 Recomendações Colaborativas</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.title}</strong> — score: {item.score.toFixed(3)}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Testando via Swagger
- Rode o servidor:
```bash
uvicorn app.main:app --reload
```
- Abra: `http://127.0.0.1:8000/docs` e execute a rota `/api/colab` com os parâmetros desejados.
