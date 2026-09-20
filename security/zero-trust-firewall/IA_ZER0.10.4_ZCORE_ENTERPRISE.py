#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 Z-CORE H202 – Zero-Trust Prompt Firewall
 Version : v0.10.4-ENTERPRISE (Gold Master)
 Certification : NSP-LAW-AI-2026
 Agent : Z-CORE-H202 / NANS-V9
 
 Description :
 Pare-feu d'inférence IA local, déterministe, 0-dépendance (Stdlib Python).
 Analyse multicritère : SSRF, Jailbreak, Obfuscation Base64, Entropie Shannon,
 PII, Adresses IP privées. Journalisation WAL append-only & HMAC-SHA256.
===============================================================================
"""

import sys
import os
import re
import json
import math
import time
import hashlib
import hmac
import base64
import argparse
import ipaddress
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# -----------------------------------------------------------------------------
# CONFIGURATION GLOBALE & CONSTANTES
# -----------------------------------------------------------------------------
VERSION = "v0.10.4-ENTERPRISE"
CERTIFICATION = "NSP-LAW-AI-2026"
AGENT = "Z-CORE-H202 / NANS-V9"

SECRET_KEY = os.environ.get("ZCORE_SECRET_KEY", "ZCORE_H202_DEFAULT_SECRET_KEY_NSP2026").encode('utf-8')
API_KEY = os.environ.get("ZCORE_API_KEY", None)
WAL_FILE = "zcore_audit.wal"

# Lock global pour écriture WAL et Rate Limiter
WAL_LOCK = threading.Lock()

# -----------------------------------------------------------------------------
# MOTS-CLÉS & PATTERNS REGEX DE SÉCURITÉ
# -----------------------------------------------------------------------------
# SSRF Critiques (Metadonnées Cloud, Localhost, IP Internes)
SSRF_CRITICAL_PATTERNS = [
    r"169\.254\.169\.254",
    r"metadata\.google\.internal",
    r"100\.100\.100\.100",
    r"localhost",
    r"127\.0\.0\.1",
    r"0\.0\.0\.0",
    r"::1",
    r"http://\[::\]",
    r"http://0/"
]

# SSRF Standards (Protocole non-HTTP, ports sensibles)
SSRF_STANDARD_PATTERNS = [
    r"file://", r"gopher://", r"dict://", r"ftp://", r"tftp://", r"ldap://",
    r":22\b", r":23\b", r":25\b", r":3306\b", r":5432\b", r":6379\b", r":11211\b", r":27017\b"
]

# Injections & Jailbreaks
JAILBREAK_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+all\s+prior\s+rules",
    r"you\s+are\s+now\s+in\s+DAN\s+mode",
    r"developer\s+mode\s+enabled",
    r"override\s+system\s+prompt",
    r"jailbreak",
    r"act\0?\s+as\s+an?\s+unrestricted",
    r"bypass\s+safety\s+filters",
    r"reveal\s+your\s+system\s+prompt"
]

# Données Personnelles (PII)
PII_EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PII_PHONE_PATTERN = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
PII_CREDIT_CARD = r"\b(?:\d[ -]*?){13,16}\b"
PII_NIR_FR = r"\b[12]\s?\d{2}\s?(?:0[1-9]|1[0-2])\s?(?:2[AB]|\d{2})\s?\d{3}\s?\d{3}\s?\d{2}\b"

# Détection d'adresses IP v4/v6
IP_REGEX = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

# -----------------------------------------------------------------------------
# RATE LIMITER (TOKEN BUCKET)
# -----------------------------------------------------------------------------
class TokenBucket:
    def __init__(self, capacity=20, fill_rate=10.0):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.fill_rate = float(fill_rate)  # jetons par seconde
        self.last_update = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens=1):
        with self.lock:
            now = time.time()
            delta = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + delta * self.fill_rate)
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

GLOBAL_RATE_LIMITER = TokenBucket(capacity=20, fill_rate=10.0)

# -----------------------------------------------------------------------------
# FONCTIONS UTILITAIRES DE SÉCURITÉ
# -----------------------------------------------------------------------------
def calculate_shannon_entropy(data: str) -> float:
    """Calcule l'entropie de Shannon d'une chaîne de caractères."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    occ = {}
    for char in data:
        occ[char] = occ.get(char, 0) + 1
    for count in occ.values():
        p = count / length
        entropy -= p * math.log2(p)
    return round(entropy, 4)

def check_and_redact_private_ips(text: str) -> tuple:
    """Détecte et caviarde uniquement les adresses IP privées / link-local / loopback."""
    redacted_text = text
    found_private = False
    
    matches = re.findall(IP_REGEX, text)
    for match in matches:
        try:
            ip_obj = ipaddress.ip_address(match)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                found_private = True
                redacted_text = redacted_text.replace(match, "[REDACTED_PRIVATE_IP]")
        except ValueError:
            continue
            
    return redacted_text, found_private

def decode_base64_recursive(text: str, max_depth=3) -> tuple:
    """Décode de manière récursive les sous-chaînes Base64 détectées."""
    current_text = text
    b64_found = False
    decoded_segments = []
    
    # Pattern recherchant des blocs Base64 potentiels (longueur >= 16)
    b64_pattern = r"[A-Za-z0-9+/]{16,}={0,2}"
    
    for _ in range(max_depth):
        matches = re.findall(b64_pattern, current_text)
        if not matches:
            break
        
        any_decoded = False
        for m in matches:
            try:
                decoded_bytes = base64.b64decode(m, validate=True)
                decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                if len(decoded_str.strip()) > 4:
                    b64_found = True
                    any_decoded = True
                    decoded_segments.append(decoded_str)
                    current_text = current_text.replace(m, decoded_str)
            except Exception:
                continue
        if not any_decoded:
            break
            
    return current_text, b64_found, decoded_segments

def generate_hmac_signature(data_str: str) -> str:
    """Génère la signature HMAC-SHA256 pour traçabilité et non-répudiation."""
    return hmac.new(SECRET_KEY, data_str.encode('utf-8'), hashlib.sha256).hexdigest()

# -----------------------------------------------------------------------------
# MOTEUR D'INSPECTION ZERO-TRUST
# -----------------------------------------------------------------------------
def inspect_prompt(prompt: str) -> dict:
    """
    Exécute l'analyse multicritère et calcule le score de risque.
    Niveaux : LOW (0-14.9), MEDIUM (15-39.9), HIGH (40-69.9), CRITICAL (70-100)
    """
    score = 0.0
    flags = []
    sanitized_prompt = prompt

    # 1. Analyse Obfuscation Base64 & Décodage
    decoded_prompt, b64_detected, decoded_segments = decode_base64_recursive(prompt)
    if b64_detected:
        score += 25.0
        flags.append("BASE64_OBFUSCATION_DETECTED")

    # Texte de travail pour les injections (inclut le contenu décodé)
    analysis_target = prompt + " " + decoded_prompt

    # 2. Entropie de Shannon
    entropy = calculate_shannon_entropy(prompt)
    if entropy > 4.8 and len(prompt) > 30:
        score += 15.0
        flags.append(f"HIGH_SHANNON_ENTROPY ({entropy})")

    # 3. Vecteurs SSRF Critiques
    for pattern in SSRF_CRITICAL_PATTERNS:
        if re.search(pattern, analysis_target, re.IGNORECASE):
            score += 70.0
            flags.append(f"SSRF_CRITICAL_VECTOR ({pattern})")
            break

    # 4. Vecteurs SSRF Standards
    for pattern in SSRF_STANDARD_PATTERNS:
        if re.search(pattern, analysis_target, re.IGNORECASE):
            score += 30.0
            flags.append(f"SSRF_STANDARD_VECTOR ({pattern})")
            break

    # 5. Injections & Jailbreaks
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, analysis_target, re.IGNORECASE):
            score += 45.0
            flags.append(f"JAILBREAK_PATTERN_DETECTED ({pattern})")
            break

    # 6. Adresses IP Privées & Caviardage
    sanitized_prompt, has_private_ip = check_and_redact_private_ips(sanitized_prompt)
    if has_private_ip:
        score += 20.0
        flags.append("PRIVATE_IP_EXPOSURE")

    # 7. Données Personnelles (PII) & Caviardage
    if re.search(PII_EMAIL_PATTERN, sanitized_prompt):
        score += 20.0
        flags.append("PII_EMAIL_DETECTED")
        sanitized_prompt = re.sub(PII_EMAIL_PATTERN, "[REDACTED_EMAIL]", sanitized_prompt)

    if re.search(PII_CREDIT_CARD, sanitized_prompt):
        score += 35.0
        flags.append("PII_CREDIT_CARD_DETECTED")
        sanitized_prompt = re.sub(PII_CREDIT_CARD, "[REDACTED_CARD]", sanitized_prompt)

    if re.search(PII_NIR_FR, sanitized_prompt):
        score += 30.0
        flags.append("PII_NIR_FR_DETECTED")
        sanitized_prompt = re.sub(PII_NIR_FR, "[REDACTED_NIR]", sanitized_prompt)

    # Plafonnement du score de risque [0.0, 100.0]
    final_score = min(100.0, round(score, 2))

    # Matrice de Décision à 4 niveaux
    if final_score < 15.0:
        decision = "ALLOW"
        action = "PASS_INTACT"
        output_payload = prompt
    elif final_score < 40.0:
        decision = "SANITIZE_PASS"
        action = "PASS_SANITIZED"
        output_payload = sanitized_prompt
    elif final_score < 70.0:
        decision = "QUARANTINE"
        action = "FLAG_FOR_AUDIT"
        output_payload = sanitized_prompt
    else:
        decision = "BLOCK"
        action = "REJECT_PAYLOAD"
        output_payload = "[BLOCKED BY Z-CORE H202 FIREWALL: HIGH RISK THREAT DETECTED]"

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    # Audit Payload pour Signature HMAC
    audit_data = {
        "timestamp": timestamp,
        "score": final_score,
        "decision": decision,
        "flags": flags,
        "prompt_hash": hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    }
    
    signature = generate_hmac_signature(json.dumps(audit_data, sort_keys=True))

    result = {
        "status": "SUCCESS",
        "agent": AGENT,
        "certification": CERTIFICATION,
        "version": VERSION,
        "timestamp": timestamp,
        "risk_score": final_score,
        "decision": decision,
        "action": action,
        "flags": flags,
        "metrics": {
            "shannon_entropy": entropy,
            "base64_detected": b64_detected
        },
        "processed_prompt": output_payload,
        "hmac_signature": signature
    }

    # Logging WAL (Append-Only)
    write_wal_entry(result)

    return result

def write_wal_entry(entry: dict):
    """Écrit le résultat dans le fichier Journal WAL JSONL de manière atomique."""
    with WAL_LOCK:
        try:
            with open(WAL_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            sys.stderr.write(f"[WAL ERROR] Impossible d'écrire dans l'audit WAL: {e}\n")

# -----------------------------------------------------------------------------
# SERVEUR HTTP MULTI-THREADÉ
# -----------------------------------------------------------------------------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Serveur HTTP gérant les requêtes de manière concurrente."""
    daemon_threads = True

class ZCoreRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Formatage propre des logs serveur sur stderr
        sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}\n")

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-ZCORE-KEY")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            response = {
                "status": "ONLINE",
                "system": "Z-CORE H202 Prompt Firewall",
                "version": VERSION,
                "certification": CERTIFICATION,
                "agent": AGENT,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Introuvable")

    def do_POST(self):
        if self.path == "/inspect":
            # 1. Vérification Rate Limiting
            if not GLOBAL_RATE_LIMITER.consume(1):
                self.send_response(429)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                err_resp = {"error": "Rate limit exceeded (10 req/s, burst 20)"}
                self.wfile.write(json.dumps(err_resp).encode('utf-8'))
                return

            # 2. Vérification Authentification API (si activée)
            if API_KEY:
                client_key = self.headers.get("X-ZCORE-KEY")
                if client_key != API_KEY:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json")
                    self._send_cors_headers()
                    self.end_headers()
                    err_resp = {"error": "Accès non autorisé: Clé API invalide"}
                    self.wfile.write(json.dumps(err_resp).encode('utf-8'))
                    return

            # 3. Extraction du Payload
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Payload vide"}).encode('utf-8'))
                return

            raw_body = self.rfile.read(content_length).decode('utf-8', errors='ignore')
            try:
                data = json.loads(raw_body)
                prompt = data.get("prompt", "")
            except Exception:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "JSON Invalide"}).encode('utf-8'))
                return

            # 4. Traitement par le moteur Z-CORE
            try:
                result = inspect_prompt(prompt)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Erreur interne du moteur: {str(e)}"}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Introuvable")

# -----------------------------------------------------------------------------
# POINT D'ENTRÉE CLI & DÉMARRAGE
# -----------------------------------------------------------------------------
def run_server(port=8080):
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, ZCoreRequestHandler)
    print(f"[Z-CORE-H202] Serveur HTTP actif sur le port {port}...")
    print(f"[Z-CORE-H202] Mode Zero-Trust [OK] | Certification : {CERTIFICATION}")
    print(f"[Z-CORE-H202] WAL Log File : {WAL_FILE}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Z-CORE-H202] Arrêt du serveur HTTP.")
        httpd.server_close()

def main():
    parser = argparse.ArgumentParser(description="Z-CORE H202 – Zero-Trust Prompt Firewall")
    parser.add_argument("--eval", type=str, help="Évalue immédiatement une chaîne de prompt en CLI")
    parser.add_argument("--server", action="store_true", help="Lance le serveur HTTP d'inspection")
    parser.add_argument("--port", type=int, default=8080, help="Port d'écoute du serveur HTTP (défaut: 8080)")

    args = parser.parse_args()

    if args.eval:
        result = inspect_prompt(args.eval)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.server:
        run_server(port=args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
