import subprocess
from pathlib import Path

# Chemin absolu du répertoire contenant les trois fichiers texte
PYCASO_PROMPT_DIR = Path("/home/jmguilbert/pycasso/prompts")

PROMPT_FILE   = PYCASO_PROMPT_DIR / "prompts.txt"
SUBJECTS_FILE = PYCASO_PROMPT_DIR / "subjects.txt"
ARTISTS_FILE  = PYCASO_PROMPT_DIR / "artistes.txt"


def _write_file(path: Path, content: str) -> None:
    """Écrase le fichier avec le texte fourni (une ligne terminée par \\n)."""
    path.write_text(content.strip() + "\n", encoding="utf-8")


def save_prompt(content: str) -> dict:
    _write_file(PROMPT_FILE, content)
    return {"file": str(PROMPT_FILE), "content": content.strip()}


def save_subjects(content: str) -> dict:
    _write_file(SUBJECTS_FILE, content)
    return {"file": str(SUBJECTS_FILE), "content": content.strip()}


def save_artists(content: str) -> dict:
    _write_file(ARTISTS_FILE, content)
    return {"file": str(ARTISTS_FILE), "content": content.strip()}


def restart_pycasso_service() -> dict:
    """
    Lance le script `run_pycasso.sh` qui doit se charger d’arrêter
    (si besoin) puis de redémarrer le service Pycasso.
    """
    try:
        subprocess.run(
            ["./run_pycasso.sh"],
            cwd=str(Path(__file__).resolve().parent.parent),  # racine du projet
            check=True,
        )
        return {"status": "success", "message": "Service Pycasso relancé."}
    except subprocess.CalledProcessError as exc:
        return {"status": "error", "message": f"Erreur : {exc}"}
