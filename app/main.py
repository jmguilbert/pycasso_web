from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .utils import (
    save_prompt,
    save_subjects,
    save_artists,
    restart_pycasso_service,
)

app = FastAPI(title="Interface Web Pycasso (Raspberry Pi)")


class TextPayload(BaseModel):
    text: str = Field(..., description="Contenu à écrire dans le fichier")


@app.post("/api/prompt")
def api_prompt(payload: TextPayload):
    try:
        result = save_prompt(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/subjects")
def api_subjects(payload: TextPayload):
    try:
        result = save_subjects(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/artists")
def api_artists(payload: TextPayload):
    try:
        result = save_artists(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/restart")
def api_restart():
    result = restart_pycasso_service()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return {"status": "ok", "detail": result["message"]}


# Servir le front‑end statique
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="../static", html=True), name="static")
