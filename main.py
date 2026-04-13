"""
main.py — Camada HTTP (FastAPI).
Responsabilidade única: receber requisições, chamar ia.py e database.py,
devolver respostas. Nenhuma lógica de negócio aqui.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ia import classificar
from database import init_db, salvar_atendimento, buscar_atendimentos


# ──────────────────────────────────────────────
# Modelos de entrada/saída
# ──────────────────────────────────────────────
class MensagemCliente(BaseModel):
    cliente_id: str
    texto: str


# ──────────────────────────────────────────────
# Lifespan (substitui @app.on_event)
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # startup
    yield
    # (coloque aqui código de shutdown se precisar)


# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
app = FastAPI(title="Sistema de Atendimento Inteligente", lifespan=lifespan)


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────
@app.post("/atendimento")
async def receber_atendimento(msg: MensagemCliente):
    try:
        resultado = classificar(msg.texto)

        registro = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente":   msg.cliente_id,
            "mensagem":  msg.texto,
            **resultado,
        }

        registro["id"] = salvar_atendimento(registro)
        return registro

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {e}")


@app.get("/atendimentos")
async def listar_atendimentos(limit: int = 50):
    return buscar_atendimentos(limit)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)