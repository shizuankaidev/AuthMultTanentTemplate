# 🏢 CompanyAdmin API

Este documento descreve o **módulo de gerenciamento de Companies**, incluindo CRUD completo e atribuição de owner.  

Todas as rotas estão sob:  
`/api/company/`

Acesso restrito a usuários **Admin** ou **superuser**.

---

## 🔹 Rotas Disponíveis

---

======================================================================================================

### 1. `GET / – Listar Companies`

Retorna todas as Companies cadastradas.

**Resposta (JSON):**
```json
[
  {
    "id": 1,
    "name": "Empresa Exemplo",
    "owner": 2
  },
  {
    "id": 2,
    "name": "Outra Empresa",
    "owner": null
  }
]
```
Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 2. `GET /<pk>/ – Detalhes da Company`

Retorna os dados de uma Company específica.

```Resposta (JSON):

{
  "id": 1,
  "name": "Empresa Exemplo",
  "owner": 2
}
```

======================================================================================================

### 3.  `POST / – Criar Company`


Cria uma nova Company.

Payload (JSON):

```
{
  "name": "shizu Eterprises",
  "slug": "shizu-eterprises",
  "cnpj": "12.345.678/0001-99"
}
```

```Resposta (JSON):
{
  "id": 3,
  "name": "Nova Empresa",
  "owner": null
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================


Permissão: Autenticado + Admin (IsAdmin)

### 4. `PUT /<pk>/ – Atualizar Company`

Atualiza todos os campos de uma Company.

```Payload (JSON):

{
  "name": "Empresa Atualizada"
}
```

```Resposta (JSON):

{
  "id": 1,
  "name": "Empresa Atualizada",
  "owner": 2
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 5. PATCH /<pk>/ – Atualização Parcial

Atualiza parcialmente os campos de uma Company.

```Payload (JSON) exemplo:

{
  "name": "Novo Nome Parcial"
}
```

```Resposta (JSON):

{
  "id": 1,
  "name": "Novo Nome Parcial",
  "owner": 2
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 6. `DELETE /<pk>/ – Deletar Company`

Remove uma Company.

```Resposta (JSON):

{
  "detail": "Company deletada com sucesso."
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 7. `POST /<pk>/owner/ – Definir Owner`

Define um usuário do tipo EMPRESA como owner da Company.

```Payload (JSON):

{
  "user_id": 5
}
```

Respostas possíveis:

```// Sucesso
{
  "detail": "Owner definido com sucesso."
}
```

```// Erro: user_id ausente
{
  "detail": "user_id é obrigatório."
}
```

```// Erro: tipo incorreto
{
  "detail": "Apenas usuários do tipo EMPRESA podem ser owner."
}
```

```// Erro: já é owner de outra empresa
{
  "detail": "Usuário já é owner de outra empresa."
}
```

Permissão: Autenticado + Admin (IsAdmin)

======================================================================================================

### 8. `DELETE /<pk>/owner/ – Revogar Owner`

Remove o owner atual da Company.

```Resposta (JSON):

{
  "detail": "Owner removido com sucesso."
}
```

Permissão: Autenticado + Admin (IsAdmin)