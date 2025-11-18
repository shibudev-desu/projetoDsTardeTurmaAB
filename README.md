# 🎨🎶 SingerSwipe – Descubra novos artistas de forma divertida

## 📌 Introdução

O **SingerSwipe** é um aplicativo inspirado na dinâmica do Tinder, mas voltado para a **descoberta de artistas independentes e pouco reconhecidos**.  
A proposta é oferecer uma experiência envolvente e intuitiva, ajudando os usuários a conhecerem novos talentos e, ao mesmo tempo, dando mais **visibilidade para artistas emergentes**.

## 🎯 Objetivos

- Criar uma plataforma interativa para conectar fãs a artistas independentes.  
- Oferecer uma experiência divertida e viciante de “swipe de descobertas”.  
- Ampliar a visibilidade de músicos e artistas visuais em início de carreira.  
- Facilitar o acesso a links de redes sociais, portfólios e plataformas de streaming.  

## 🚀 Funcionalidades

- Sistema de **swipe** para descobrir artistas (direita = gostei, esquerda = pular).  
- Filtros personalizados (gênero musical, estilo de arte, região, vibe etc.).  
- Exibição de **cards interativos** com foto, nome, descrição e prévia da obra.  
- Página de detalhes do artista com informações adicionais e links externos.  
- Integração com plataformas como **Spotify** e redes sociais.  

## 🛠️ Tecnologias

- **Backend:** [Python](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/)  
- **Frontend Mobile:** [React Native](https://reactnative.dev/) com [Expo](https://expo.dev/)  
- **Banco de Dados:** [PostgreSQL](https://postgresql.org/)
- **Autenticação:** JWT ou OAuth2 (planejado)  
- **Outros:** Integrações com APIs externas (ex.: Spotify API)  

## ⚙️ Instalação e Execução

## 🗄️ Banco de Dados (PostgreSQL)

O projeto utiliza **PostgreSQL** rodando no SUPABASE.  

## Tutorial no youtube de como utilizar

<https://youtu.be/vXIJ2t6O8QU?si=11NeaYQ7K9PGJ7cp>

### 🔹 Backend (FastAPI)

1. Clone o repositório:
  
  ```cmd
  git clone https://github.com/ensismoebius/projetoDsTardeTurmaAB.git
  
  cd projetoDsTardeTurmaAB/backend
  ```

<br>

2. Ative o ambiente virtual:

  ```cmd
  python -m venv venv

  ./venv/Scripts/Activate.ps1
  ```

<br>

3. Instale as dependências:

  ```cmd
  pip install -r requirements.txt
  ```

<br>

### 🔹 Frontend (React Native + Expo)

1. Acesse a pasta do frontend:
  cd singerswipe/frontend

2. Instale as dependências:
  npm install

3. Execute o app com Expo:
  npx expo start

4. Escaneie o QR Code no aplicativo Expo Go para abrir no celular.

## Endpoints

### Rotas

- GET /: Retorna a lista de usuários do banco de dados falso.
- GET /{user_id}: Retorna um usuário específico pelo ID.
- POST /: Cria um novo usuário e o adiciona ao banco de dados falso.
- PUT /{user_id}: Atualiza o nome de um usuário existente pelo ID.
- DELETE /{user_id}: Remove um usuário do banco de dados falso pelo ID.

### Funções

- get_users(): Retorna todos os usuários.
- get_user(user_id): Retorna um usuário pelo ID, ou None se não encontrado.
- create_user(user): Cria um novo usuário com nome fornecido.
- update_user(user_id, user): Atualiza o nome do usuário pelo ID.
- delete_user(user_id): Remove o usuário pelo ID.

## 📚 Referências Bibliográficas

- **TIAÑOLO**, Sebastián Ramírez. FastAPI Documentation. Disponível em: <https://fastapi.tiangolo.com/>
- **EXPO. Getting Started with Expo.** Disponível em: <https://docs.expo.dev/>
- **REACT NATIVE. Official Documentation.** Disponível em: <https://reactnative.dev/>

## 👨‍💻 Créditos

Projeto desenvolvido pelo 3ºMDS de 2025.

Inspirado na ideia de unir arte, música e tecnologia para promover novos talentos.

## 📄 Licença

Este projeto está licenciado sob a licença MIT – veja o arquivo LICENSE para mais detalhes.
