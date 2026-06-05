# 📚 Sistema de Registro de Notas

**Disciplina:** Desenvolvimento Rápido de Aplicações em Python  
**Curso:** CCP / ADS  
**Professor:** Ralfh V Ansuattigui
**Alunos:** Leonardo Muniz 202407187188
            Leonardo Fernandes 202503104026
            João Gabriel Teixeira 202502518269
            Kaio Côrtes do Valle 202502281943
            Bruno Conceição Pereira de Souza 202502367848

---

## 📁 Estrutura do projeto

```
sistema_notas/
├── app.py          # Interface gráfica Tkinter + lógica da aplicação
├── database.py     # Camada de acesso a dados (PostgreSQL ou SQLite)
├── schema.sql      # Script SQL para PostgreSQL
└── README.md       # Este arquivo
```

---

## ⚙️ Requisitos

- Python 3.8+
- Tkinter (já incluso no Python padrão)
- SQLite (já incluso no Python padrão) **ou**
- PostgreSQL + `psycopg2-binary`

---

## 🚀 Como executar

### Opção A — SQLite (recomendado para testes, sem instalação extra)

1. Certifique-se de ter Python 3.8+:
   ```bash
   python --version
   ```

2. Execute diretamente:
   ```bash
   python app.py
   ```

O arquivo `registro_notas.db` será criado automaticamente na mesma pasta.

---

### Opção B — PostgreSQL

1. Instale o driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Crie o banco no PostgreSQL:
   ```bash
   psql -U postgres -f schema.sql
   ```
   Ou manualmente:
   ```sql
   CREATE DATABASE registro_notas;
   \c registro_notas
   \i schema.sql
   ```

3. Edite `database.py`:
   ```python
   USE_POSTGRES = True

   PG_CONFIG = {
       "host":     "localhost",
       "port":     5432,
       "dbname":   "registro_notas",
       "user":     "postgres",
       "password": "sua_senha",
   }
   ```

4. Execute:
   ```bash
   python app.py
   ```

---

## 🖥️ Funcionalidades (CRUD)

| Operação | Como usar |
|---|---|
| **Cadastrar** | Preencha o formulário → clique **Cadastrar** |
| **Listar** | Todos os alunos são exibidos ao abrir o sistema |
| **Buscar** | Digite nome, matrícula ou disciplina → **Buscar** |
| **Atualizar** | Clique em um aluno na tabela → edite os campos → **Atualizar** |
| **Excluir** | Clique em um aluno na tabela → **Excluir** |

---

## 📊 Cálculo de média e situação

| Média | Situação |
|---|---|
| ≥ 7,0 | ✅ Aprovado |
| ≥ 5,0 | ⚠️ Recuperação |
| < 5,0 | ❌ Reprovado |

---

## 🔄 SQLite vs PostgreSQL — comparativo

### Ganhos com SQLite
- ✔ Zero configuração de servidor
- ✔ Arquivo único portátil (`.db`)
- ✔ Sem dependências externas
- ✔ Ideal para prototipagem e pequenas instalações

### Perdas com SQLite
- ✘ Acesso concorrente limitado (problemas com múltiplos usuários simultâneos)
- ✘ Sem gerenciamento de permissões por usuário
- ✘ Sem conexão remota nativa
- ✘ Sem stored procedures, replicação e recursos avançados

**Conclusão:** Para a atividade e uso em laboratório, SQLite é suficiente e mais prático. Em produção real com rede e múltiplos operadores, PostgreSQL é a escolha correta.

---

## 👥 Entrega

- Código-fonte no GitHub (entrega individual, nota em grupo)
- Prazo 1ª entrega: **08/05**
- Prazo 2ª entrega: **29/05**
