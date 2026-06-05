"""
Camada de acesso a dados — suporta PostgreSQL (psycopg2) e SQLite.

Altere USE_POSTGRES para False para usar SQLite sem nenhuma outra mudança.

──────────────────────────────────────────────────────────────────────────────
COMPARATIVO: PostgreSQL vs SQLite no contexto deste sistema
──────────────────────────────────────────────────────────────────────────────

GANHOS ao usar SQLite (em vez de PostgreSQL):
  ✔ Zero configuração: não precisa instalar servidor, criar usuário ou banco.
  ✔ Portabilidade: o banco é um único arquivo .db — fácil de copiar/backup.
  ✔ Ideal para ambiente de desenvolvimento e prototipagem rápida.
  ✔ Sem dependências externas: módulo sqlite3 já vem na biblioteca padrão Python.
  ✔ Suficiente para poucos usuários simultâneos (instituição de pequeno porte).

PERDAS ao usar SQLite (em comparação com PostgreSQL):
  ✘ Acesso concorrente limitado: SQLite bloqueia escritas simultâneas; em cenários
    multiusuário (vários secretários acessando ao mesmo tempo) pode gerar erros.
  ✘ Sem gerenciamento de usuários/permissões nativos (qualquer um com acesso ao
    arquivo .db pode ler tudo).
  ✘ Recursos avançados ausentes: stored procedures, replicação, full-text search
    avançado, etc.
  ✘ Sem suporte a conexão remota nativa — banco fica preso à máquina local.
  ✘ Menos adequado para escalar: se a instituição crescer e precisar de um sistema
    web acessível por múltiplos usuários, migrar para PostgreSQL será necessário.

RECOMENDAÇÃO para este projeto:
  • Desenvolvimento/entrega da atividade → SQLite (simplicidade).
  • Produção real em rede → PostgreSQL (robustez e concorrência).
──────────────────────────────────────────────────────────────────────────────
"""

import sqlite3
import os

# ── Configuração ──────────────────────────────────────────────────────────────
USE_POSTGRES = False   # Altere para True e configure abaixo para usar PostgreSQL

PG_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "registro_notas",
    "user":     "postgres",
    "password": "sua_senha_aqui",
}

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "registro_notas.db")

# Rótulo exibido na interface
BACKEND_LABEL = "Backend: PostgreSQL" if USE_POSTGRES else "Backend: SQLite"


# ── Conexão ───────────────────────────────────────────────────────────────────
def _get_connection():
    if USE_POSTGRES:
        try:
            import psycopg2
            return psycopg2.connect(**PG_CONFIG)
        except ImportError:
            raise RuntimeError(
                "psycopg2 não encontrado. Instale com: pip install psycopg2-binary"
            )
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def _placeholder():
    """Retorna o placeholder correto para cada backend (%s ou ?)."""
    return "%s" if USE_POSTGRES else "?"


# ── Inicialização do banco ────────────────────────────────────────────────────
def inicializar_banco():
    """Cria tabela se não existir."""
    conn = _get_connection()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id         SERIAL PRIMARY KEY,
                nome       VARCHAR(150) NOT NULL,
                matricula  VARCHAR(20)  NOT NULL UNIQUE,
                disciplina VARCHAR(100) NOT NULL,
                nota1      NUMERIC(4,2) NOT NULL,
                nota2      NUMERIC(4,2) NOT NULL,
                nota3      NUMERIC(4,2) NOT NULL
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nome       TEXT    NOT NULL,
                matricula  TEXT    NOT NULL UNIQUE,
                disciplina TEXT    NOT NULL,
                nota1      REAL    NOT NULL,
                nota2      REAL    NOT NULL,
                nota3      REAL    NOT NULL
            );
        """)

    conn.commit()
    cur.close()
    conn.close()


# ── Helpers ───────────────────────────────────────────────────────────────────
def _calcular_media(n1, n2, n3):
    return round((n1 + n2 + n3) / 3, 2)


def _situacao(media):
    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperação"
    return "Reprovado"


def _formatar_registros(rows):
    resultado = []
    for r in rows:
        row = dict(r) if hasattr(r, "keys") else {
            "id": r[0], "nome": r[1], "matricula": r[2],
            "disciplina": r[3], "nota1": r[4], "nota2": r[5], "nota3": r[6]
        }
        media = _calcular_media(row["nota1"], row["nota2"], row["nota3"])
        resultado.append((
            row["id"],
            row["nome"],
            row["matricula"],
            row["disciplina"],
            f'{row["nota1"]:.1f}',
            f'{row["nota2"]:.1f}',
            f'{row["nota3"]:.1f}',
            f"{media:.2f}",
            _situacao(media),
        ))
    return resultado


# ── CRUD ──────────────────────────────────────────────────────────────────────
def inserir_aluno(nome, matricula, disciplina, nota1, nota2, nota3):
    p = _placeholder()
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO alunos (nome, matricula, disciplina, nota1, nota2, nota3) "
        f"VALUES ({p},{p},{p},{p},{p},{p})",
        (nome, matricula, disciplina, nota1, nota2, nota3)
    )
    conn.commit()
    cur.close()
    conn.close()


def listar_alunos():
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos ORDER BY nome")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return _formatar_registros(rows)


def buscar_alunos(termo):
    p = _placeholder()
    conn = _get_connection()
    cur = conn.cursor()
    like = f"%{termo}%"
    cur.execute(
        f"SELECT * FROM alunos WHERE nome LIKE {p} OR matricula LIKE {p} "
        f"OR disciplina LIKE {p} ORDER BY nome",
        (like, like, like)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return _formatar_registros(rows)


def atualizar_aluno(aluno_id, nome, matricula, disciplina, nota1, nota2, nota3):
    p = _placeholder()
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE alunos SET nome={p}, matricula={p}, disciplina={p}, "
        f"nota1={p}, nota2={p}, nota3={p} WHERE id={p}",
        (nome, matricula, disciplina, nota1, nota2, nota3, aluno_id)
    )
    conn.commit()
    cur.close()
    conn.close()


def excluir_aluno(aluno_id):
    p = _placeholder()
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM alunos WHERE id={p}", (aluno_id,))
    conn.commit()
    cur.close()
    conn.close()
