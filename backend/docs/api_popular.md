# 📊 Tutorial de Uso da API `/api/popular`

Essa rota serve pra **buscar os itens mais populares** do sistema, com base no usuário e em um limite definido.

## 🧩 Endpoint
```
GET http://127.0.0.1:8000/api/popular
```

## 🧠 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|------------|------|--------------|------------|
| `user_id`  | `number` | ✅ Sim | ID do usuário que está fazendo a requisição (para personalização dos resultados). |
| `limit`    | `number` | ⚙️ Opcional | Quantidade máxima de resultados que a API deve retornar. Padrão: `10`. |

### 🔍 Exemplo de requisição
```bash
GET http://127.0.0.1:8000/api/popular?user_id=2&limit=10
```

### 📦 Exemplo de Resposta
```json
[
  {
    "id": 5,
    "title": "Poke - Upload Test",
    "artist_id": 1,
    "likes": 0,
    "posted_at": "2025-10-09T23:16:17.447257+00:00"
  },
  {
    "id": 4,
    "title": "Música de Teste - Poke",
    "artist_id": 1,
    "likes": 0,
    "posted_at": "2025-10-09T23:10:39.05294+00:00"
  }
]
```

## ⚛️ Exemplo em React (com useEffect)
```JS
import { useEffect, useState } from "react";

export default function PopularList() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    async function fetchPopular() {
      const res = await fetch("http://127.0.0.1:8000/api/popular?user_id=2&limit=10");
      const json = await res.json();
      setItems(json.data);
    }

    fetchPopular();
  }, []);

  return (
    <div>
      <h2>🔥 Itens Populares</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.title}</strong> — {item.category}
          </li>
        ))}
      </ul>
    </div>
  );
}
```