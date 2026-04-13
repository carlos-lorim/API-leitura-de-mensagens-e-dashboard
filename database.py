"""
database.py — Camada de acesso ao banco de dados.
Nenhum outro módulo deve importar sqlite3 diretamente.
"""

import sqlite3
import pandas as pd
from contextlib import contextmanager

DB_PATH = "atendimento.db"


# ──────────────────────────────────────────────
# Conexão
# ──────────────────────────────────────────────
@contextmanager
def get_conn():
    """Context manager: abre, entrega e fecha a conexão com segurança."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ──────────────────────────────────────────────
# Inicialização
# ──────────────────────────────────────────────
def init_db():
    """Cria a tabela se não existir. Chamado uma vez no startup da API."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS atendimentos (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp         TEXT NOT NULL,
                cliente           TEXT NOT NULL,
                mensagem          TEXT NOT NULL,
                intencao          TEXT NOT NULL,
                prioridade        TEXT NOT NULL,
                resposta_sugerida TEXT NOT NULL
            )
        """)
    print("[db] Banco inicializado.")


# ──────────────────────────────────────────────
# Escrita
# ──────────────────────────────────────────────
def salvar_atendimento(registro: dict) -> int:
    """Insere um registro e retorna o id gerado."""
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO atendimentos
                (timestamp, cliente, mensagem, intencao, prioridade, resposta_sugerida)
            VALUES
                (:timestamp, :cliente, :mensagem, :intencao, :prioridade, :resposta_sugerida)
        """, registro)
        return cursor.lastrowid


# ──────────────────────────────────────────────
# Leitura
# ──────────────────────────────────────────────
def buscar_atendimentos(limit: int = 50) -> list[dict]:
    """Retorna os últimos N atendimentos como lista de dicts."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM atendimentos ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def buscar_todos_como_df() -> pd.DataFrame:
    """Retorna todos os registros como DataFrame (usado pelo dashboard)."""
    with get_conn() as conn:
        df = pd.read_sql("SELECT * FROM atendimentos ORDER BY timestamp DESC", conn)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["data"] = df["timestamp"].dt.date
    return df