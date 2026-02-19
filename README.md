# Pycasso‑Web – Interface Web pour le projet Pycasso
# Realisé par Jean-Marc Guilbert avec l'aide de Lumo

## Description
Petite interface web (FastAPI + HTML/JS) permettant depuis un Raspberry Pi A+ :
- d’envoyer trois listes de mots‑clefs (`prompts.txt`, `subjects.txt`, `artists.txt`);
- de relancer le service Pycasso via `systemd` (`sudo systemctl restart pycasso`);
- le tout sans dépendre d’un script externe.

Le front‑end se compose d’une page HTML simple avec trois zones de texte et un bouton de redémarrage.

---

## Prérequis sur le Raspberry Pi

| Élément | Version/minimum |
|---------|-----------------|
| OS | Raspberry Pi OS (Buster/Bookworm) |
| Python | 3.11 (installé avec `sudo apt install python3 python3-venv`) |
| Git | `git` |
| Service Pycasso | Doit être installé séparément dans `/home/jmguilbert/pycasso` et exposé via un service systemd nommé **`pycasso`**. |

---

## Installation

```bash
# 1️⃣ Cloner le dépôt dans un repertoire "pycasso-web
git clone https://github.com/<votre‑utilisateur>/pycasso-web.git
cd pycasso-web

# 2️⃣ Créer le virtualenv
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Installer les dépendances Python
pip install -r requirements.txt

# 4️⃣ Vérifier que le répertoire static existe
ls static/index.html   # doit afficher le fichier

# 5️⃣ (Optionnel) Tester le serveur manuellement
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Ouvrez http://<IP_PI>:8000/ dans un navigateur – vous devez voir l’interface.

# 6️⃣ Configuration du redémarrage via systemd
# Copiez le fichier de service dans /etc/systemd/system (requiert sudo)
sudo cp pycasso-web.service /etc/systemd/system/

# Rechargez systemd et activez le service au boot
sudo systemctl daemon-reload
sudo systemctl enable pycasso-web.service

# Démarrez immédiatement
sudo systemctl start pycasso-web.service

# Vérifiez le statut
sudo systemctl status pycasso-web.service
