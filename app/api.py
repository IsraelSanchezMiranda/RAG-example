"""API REST. Arranque: uvicorn app.api:app --reload"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import asistente, config, db, llm

app = FastAPI(title="Asistente de la Distribuidora")


class Pregunta(BaseModel):
    pregunta: str


@app.get("/salud")
def salud():
    estado = {"api": "ok"}
    try:
        modelos = llm.modelos_instalados()
        estado["ollama"] = "ok"
        estado["modelos_faltantes"] = [m for m in (config.LLM_MODEL, config.EMBED_MODEL)
                                       if not any(x.split(":")[0] == m.split(":")[0] for x in modelos)]
    except Exception as e:
        estado["ollama"] = f"error: {e}"
    try:
        with db.conectar() as con:
            estado["chunks"] = con.execute("SELECT count(*) AS n FROM chunks").fetchone()["n"]
        estado["postgres"] = "ok"
    except Exception as e:
        estado["postgres"] = f"error: {e}"
    return estado


@app.post("/chat")
def chat(p: Pregunta):
    try:
        return asistente.responder(p.pregunta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
