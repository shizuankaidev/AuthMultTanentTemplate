# Authentication API

Este documento explica como funciona o **módulo de autenticação** do CRMback, incluindo login, refresh de tokens, registro de usuários e perfil do usuário logado.

Todas as rotas estão sob `/api/auth/`.

---

## 🔹 Rotas Disponíveis

======================================================================================================

### 1. `POST /login/`

Autentica um usuário com **email** e **senha** e retorna um **token JWT**.

**Payload (JSON):**

```json
{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

Resposta (JSON):

```
{
  "refresh": "token_refresh_aqui",
  "access": "token_access_aqui",
  "user_type": "ADMIN",
  "email": "usuario@example.com",
  "is_verified": true
}
```

Permissão: Público (AllowAny)

======================================================================================================

### 2. `POST /refresh/`

Atualiza o token JWT usando o token de refresh.

Payload (JSON):

```json
{
  "refresh": "token_refresh_aqui"
}
```

Resposta (JSON):

```
{
  "access": "novo_token_access"
}
```

Permissão: Público (AllowAny)

======================================================================================================

### 3. `POST /register/`

Cria um novo usuário. Respeita a hierarquia de usuários:

ADMIN → pode criar qualquer tipo

EMPRESA → só pode criar Afiliado ou Cliente

AFILIADO → só pode criar Cliente

CLIENTE → não pode criar usuários

Payload (JSON):

```json
{
  "email": "novo@example.com",
  "username": "novousuario",
  "password": "senha123",
  "user_type": "AFILIADO"
}
```

Resposta (JSON):

```
{
  "id": 2,
  "email": "novo@example.com",
  "username": "novousuario",
  "user_type": "AFILIADO"
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 4. `GET /profile/`

Retorna os dados do usuário logado.

Resposta (JSON):

```json
{
  "id": 1,
  "email": "usuario@example.com",
  "username": "usuario",
  "user_type": "ADMIN",
  "is_active": true,
  "is_verified": true
}
```

Permissão: Autenticado (IsAuthenticated)

======================================================================================================
