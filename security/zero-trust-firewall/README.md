# Z-CORE H202 – Zero-Trust Prompt Firewall
Version Gold Master : v0.10.4-ENTERPRISE
Certification : NSP-LAW-AI-2026
Agent : Z-CORE-H202 / NANS-V9

1. Présentation
Z-CORE H202 est un pare-feu d’inférence IA local (Zero-Trust Prompt Firewall).
Module 100% local, 0 dépendance externe, déterministe, optimisé Termux/Android/Ubuntu.

Politique zero-trust sur :
- SSRF critiques et standards
- Jailbreak / prompt injection
- Obfuscation Base64 + entropie
- PII
- IP privées / link-local

2. Caractéristiques
- Scoring multidimensionnel (SSRF critique 70 / standard 30)
- 4 niveaux de décision : ALLOW / SANITIZE_PASS / QUARANTINE / BLOCK
- Redaction sélective des IP privées
- HMAC-SHA256 + journal WAL
- Rate limiting + API key optionnelle
- Serveur HTTP multi-threadé résilient
- 0 dépendance

3. Matrice de décision (STRICT)
0.0-14.9   LOW        → ALLOW
15.0-39.9  MEDIUM     → SANITIZE_PASS
40.0-69.9  HIGH       → QUARANTINE
70.0-100.0 CRITICAL   → BLOCK

4. Utilisation
Serveur : python IA_ZER0.10.4_ZCORE_ENTERPRISE.py --server --port 8080
Arrière-plan : nohup python IA_ZER0.10.4_ZCORE_ENTERPRISE.py --server --port 8080 > zcore_server.log 2>&1 &
CLI : python IA_ZER0.10.4_ZCORE_ENTERPRISE.py --eval "prompt"

5. API
Healthcheck : curl http://127.0.0.1:8080/
Inspect : curl -X POST http://127.0.0.1:8080/inspect -H "Content-Type: application/json" -d '{"prompt":"texte"}'

6. Certification
NSP-LAW-AI-2026 | Gold Master / Enterprise | Z-CORE-H202 / NANS-V9
NetSecurePro IA (MILYES-IA)
