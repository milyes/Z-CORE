#!/data/data/com.termux/files/usr/bin/bash
# Z-CORE v24.1 — gatekeeper.sh — NON DEPENDANCE VALIDEE
# Fix: sans ss (permission denied) + kill + auto-port

set -e

# 1. Kill anciens serveurs qui bloquent 8000
echo "[*] Nettoyage ports 8000/8001/8002..."
pkill -f "gatekeeper_ia.py" 2>/dev/null || true
pkill -f "http.server 8000" 2>/dev/null || true
pkill -f "http.server 8001" 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 1

PORT=8000
TOKEN="89b6df2e-v24"

# 2. Trouve port libre sans ss
for p in 8000 8001 8002 8080; do
  if ! (echo > /dev/tcp/127.0.0.1/$p) >/dev/null 2>&1; then
    PORT=$p
    break
  fi
done

# 3. IMMORTAL .bashrc (une seule fois)
grep -q "gatekeeper.sh" ~/.bashrc 2>/dev/null || echo "nohup ~/gatekeeper.sh >/dev/null 2>&1 &" >> ~/.bashrc

echo "[Z-CORE $TOKEN] LIVE sur :$PORT — NON DEPENDANCE VALIDEE"

# 4. Lance python gatekeeper sans boucle infinie si port pris
python3 ~/gatekeeper_ia.py
