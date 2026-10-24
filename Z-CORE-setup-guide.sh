# 1. TUE tout ce qui bloque 8000
pkill -f gatekeeper
pkill -f zcore_orchestrator
pkill -f "http.server"
lsof -ti:8000 | xargs kill -9 2>/dev/null; lsof -ti:8001 | xargs kill -9 2>/dev/null
sleep 1

# 2. Récupère les fichiers que je viens de fixer
# Tu es dans Termux, pas dans /mnt/data — faut les télécharger depuis ici
# → Télécharge ces 2 fichiers depuis le chat :

# gatekeeper_ia.py -> [FICHIER CI-DESSOUS]
# gatekeeper.sh -> [FICHIER CI-DESSOUS]

# 3. Une fois placés dans ~/ :
chmod +x ~/gatekeeper.sh
chmod +x ~/gatekeeper_ia.py

# 4. Lance (sans --auto pour test)
python ~/gatekeeper_ia.py