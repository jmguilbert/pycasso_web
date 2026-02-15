#!/usr/bin/env bash
set -e

# Chemin vers le répertoire Pycasso
PYCASO_ROOT="/home/jmguilbert/pycasso"

# 1️⃣ Arrêt éventuel du processus existant
# Supposons que le serveur s’appelle pycasso_server.py
pkill -f "python.*pycasso_server.py" || true

# 2️⃣ Lancement du serveur (adapter la commande)
cd "$PYCASO_ROOT"
nohup python3 pycasso_server.py > pycasso.log 2>&1 &
echo "Pycasso relancé (PID $(pgrep -f pycasso_server.py))"
