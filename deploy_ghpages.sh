#!/bin/bash

REPO_URL="https://github.com/milyes/Z-CORE.git"

echo "=== [Z-CORE] AGENT DISTANT GIT ACTIF ==="

if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REPO_URL"
fi

git config user.name "milyes"
git add .
git commit -m "Core(update): Orchestrateur maître et suite Z-CORE v3.1.0 complète"
git branch -M main
git push -u origin main --force && echo "[✓] Chantier Z-CORE synchronisé sur github.com/milyes/Z-CORE"
