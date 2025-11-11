# TODO: Criar estrutura base para as rotas no Tracer
## Notas:
- Estrutura base criada com Express, TypeScript, MongoDB/Mongoose e Pino.
- Dependências instaladas: mongoose, pino, @types/pino.
- Servidor escuta na porta definida em .env (padrão 6964).
- Rotas: POST /logs (criar log), GET /logs (listar logs), GET /health (status).
- Middleware de autenticação com API_KEY implementado, mas pode ser ajustado.
- O tracer não inicia sem MongoDB rodando; erro: "The `uri` parameter to `openUri()` must be a string, got "undefined"" resolvido criando .env, mas MongoDB precisa estar ativo.
