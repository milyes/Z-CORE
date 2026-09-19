#!/bin/bash

export TMPDIR="${TMPDIR:-/tmp}"
SERVER_PORT=8085

echo "=================================================="
echo "    === [Z-CORE v3.1.0] ORCHESTRATEUR MAÎTRE ==="
echo "=================================================="

# 1. Diagnostic de santé initial
echo "[1/4] Lancement du diagnostic IA_REDORER..."
python3 IA_REDORER.py
echo ""

# 2. Synchronisation du contexte JSON
echo "[2/4] Initialisation du contexte IAInnovia..."
python3 IAInnovia.py
echo ""

# 3. Démarrage du serveur Web en arrière-plan
echo "[3/4] Démarrage du serveur Web local (port $SERVER_PORT)..."
python3 ZCoreServer.py > /dev/null 2>&1 &
SERVER_PID=$!
sleep 1

if ps -p $SERVER_PID > /dev/null; then
    echo "[✓] Serveur Web actif en arrière-plan (PID: $SERVER_PID)"
    echo "    -> Dashboard : http://127.0.0.1:$SERVER_PORT"
else
    echo "[!] Échec du démarrage du serveur Web."
fi
echo ""

# Fonction de nettoyage lors de l'arrêt
cleanup() {
    echo ""
    echo "=================================================="
    echo "[-] Arrêt de l'orchestration Z-CORE..."
    if kill -0 $SERVER_PID 2>/dev/null; then
        kill $SERVER_PID
        echo "[✓] Serveur Web (PID: $SERVER_PID) arrêté."
    fi
    echo "[✓] Confinement rétabli. Système en veille."
    echo "=================================================="
    exit 0
}

trap cleanup INT TERM

# 4. Lancement du Kernel principal
echo "[4/4] Démarrage du noyau ZCoreKernel..."
echo "Press Ctrl+C to stop all services."
echo "--------------------------------------------------"
python3 ZCoreKernel.py

cleanup
