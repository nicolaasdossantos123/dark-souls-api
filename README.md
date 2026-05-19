# ⚔️ Dark Souls API

API inspirada em Dark Souls desenvolvida com **Python**, **FastAPI** e **SQLite**.

Projeto criado para praticar conceitos de backend, CRUD, banco de dados, modelagem de dados e criação de APIs REST.

---

## 🚀 Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- Pydantic

---

## ✨ Funcionalidades

### 👤 Personagens
- Criar personagens
- Escolher classe
- Atributos automáticos por classe:
  - Guerreiro
  - Mago
  - Ladrao
  - Clerigo
  - Arqueiro

### ⚔️ Armamentos
- Escolha de armamentos iniciais
- Tipos disponíveis:
  - Espada
  - Adaga

### 👹 Bosses
- Cadastro de bosses
- Informações como:
  - Vida
  - Dano
  - Região
  - Dificuldade
  - Status (Vivo / Derrotado)
  - Item Drop

### 📋 Listagem
- Listagem dinâmica com filtros
- Paginação usando `limit` e `offset`

---

## 📌 Endpoints

### Classes disponíveis

```http
GET /classes
```

### Criar personagem

```http
POST /personagem
```

Exemplo:

```json
{
    "nome": "Nicolaas",
    "classe": "mago"
}
```

### Escolher armamento

```http
POST /armamento
```

Exemplo:

```json
{
    "tipo_arma": "espada"
}
```

### Criar boss

```http
POST /bosses
```

Exemplo:

```json
{
    "nome": "artorias",
    "vivo_derrotado": true
}
```

---

## ▶️ Como executar

Instale as dependências:

```bash
pip install fastapi uvicorn
```

Execute o servidor:

```bash
python -m uvicorn darksouls_api:app --reload
```

Abrir documentação automática:

```plaintext
http://127.0.0.1:8000/docs
```

---

## 📚 Objetivo do projeto

Este projeto foi desenvolvido com foco em aprendizado prático de:

- APIs REST
- FastAPI
- SQLite
- Queries SQL
- CRUD
- Modelagem de dados
- Organização de backend em Python

---

Projeto em evolução 🚀
