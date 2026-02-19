# app/utils.py
import subprocess
from pathlib import Path

# ----------------------------------------------------------------------
# Répertoire contenant les trois fichiers texte
# ----------------------------------------------------------------------
PYCASO_PROMPT_DIR = Path("/home/jmguilbert/pycasso/prompts")

PROMPT_FILE   = PYCASO_PROMPT_DIR / "prompts.txt"
SUBJECTS_FILE = PYCASO_PROMPT_DIR / "subjects.txt"
ARTISTS_FILE  = PYCASO_PROMPT_DIR / "artists.txt"   # ← renommé

# ----------------------------------------------------------------------
def _write_file(path: Path, content: str) -> None:
    """Écrase le fichier avec le texte fourni (une ligne terminée par '\\n')."""
    path.write_text(content.strip() + "\n", encoding="utf-8")


# ----------------------------------------------------------------------
# Fonctions d’enregistrement des mots‑clefs
# ----------------------------------------------------------------------
def save_prompt(text: str) -> dict:
    _write_file(PROMPT_FILE, text)
    return {"file": str(PROMPT_FILE), "content": text.strip()}


def save_subjects(text: str) -> dict:
    _write_file(SUBJECTS_FILE, text)
    return {"file": str(SUBJECTS_FILE), "content": text.strip()}


def save_artists(text: str) -> dict:
    _write_file(ARTISTS_FILE, text)
    return {"file": str(ARTISTS_FILE), "content": text.strip()}


# ----------------------------------------------------------------------
# Redémarrage du service Pycasso via systemd
# ----------------------------------------------------------------------
def restart_pycasso_service() -> dict:
    """
    Relance le service Pycasso en utilisant systemd.
    Nécessite que l'utilisateur qui exécute le serveur FastAPI ait les droits sudo
    pour la commande suivante :
        sudo systemctl restart pycasso
    (sans demander de mot de passe – configurez `/etc/sudoers` en conséquence).
    """
    try:
        subprocess.run(
            ["sudo", "-n", "systemctl", "restart", "pycasso"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return {"status": "success", "message": "Service Pycasso relancé via systemd."}
    except subprocess.CalledProcessError as exc:
        err_msg = exc.stderr.decode().strip() or str(exc)
        return {"status": "error", "message": f"Erreur lors du redémarrage : {err_msg}"}
