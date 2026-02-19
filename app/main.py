# app/main.py
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles

# Import des fonctions utilitaires
from .utils import (
    save_prompt,
    save_subjects,
    save_artists,
    restart_pycasso_service,
)

# --------------------------------------------------------------
# FastAPI instance
# --------------------------------------------------------------
app = FastAPI(title="Interface Web Pycasso (Raspberry Pi)")

# --------------------------------------------------------------
# Payload model
# --------------------------------------------------------------
class TextPayload(BaseModel):
    """Texte à enregistrer dans le fichier ciblé."""
    text: str = Field(..., description="Texte à sauvegarder")


# --------------------------------------------------------------
# API – écriture des trois fichiers
# --------------------------------------------------------------
@app.post("/api/prompt")
def api_prompt(payload: TextPayload):
    try:
        result = save_prompt(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/subjects")
def api_subjects(payload: TextPayload):
    try:
        result = save_subjects(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/artists")
def api_artists(payload: TextPayload):
    try:
        result = save_artists(payload.text)
        return {"status": "ok", "detail": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# --------------------------------------------------------------
# API – redémarrage du service Pycasso via systemd
# --------------------------------------------------------------
@app.post("/api/restart")
def api_restart():
    result = restart_pycasso_service()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return {"status": "ok", "detail": result["message"]}


# --------------------------------------------------------------
# Montage du répertoire static (front‑end)
# --------------------------------------------------------------
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

if not STATIC_DIR.is_dir():
    raise RuntimeError(f"Directory '{STATIC_DIR}' does not exist")

app.mount(
    "/",                                 # URL racine
    StaticFiles(directory=str(STATIC_DIR), html=True),
    name="static",
)
