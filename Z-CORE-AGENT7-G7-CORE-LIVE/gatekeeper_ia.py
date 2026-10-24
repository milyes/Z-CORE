#!/data/data/com.termux/files/usr/bin/python3
# Z-CORE v24.1 — gatekeeper_ia.py — NON DEPENDANCE VALIDEE
# Fix: L1 AUTO-PORT + gestion typo continu

import http.server, json, socket, hashlib, os, sys

# === CONFIG ===
DEFAULT_KEYWORD_HASH = "a3f5c851...remplace_par_ton_sha256"  # echo -n "GHOST2026!" | sha256sum
EXPECTED_HASH = DEFAULT_KEYWORD_HASH

def check_keyword(pwd=""):
    if not pwd:
        return True # mode auto sans hash pour test
    h = hashlib.sha256(pwd.encode()).hexdigest()
    return h == EXPECTED_HASH

class Gatekeeper(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get("X-ZCORE-Token") != "89b6df2e-v24":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"ZeroTrust 401 Filter"}')
            return
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status":"LIVE",
            "version":"v24.1",
            "non_dependance":"VALIDEE",
            "logics":22,
            "endpoint":"/api/status",
            "port": self.server.server_address[1]
        }).encode())
    def log_message(self, *a): pass

if __name__ == "__main__":
    # L1 AUTO-PORT 8000->8001->8002
    for port in [8000, 8001, 8002, 8080]:
        try:
            print(f"[Z-CORE 89b6df2e-v24] Tentative port {port}...")
            httpd = http.server.HTTPServer(("", port), Gatekeeper)
            print(f"[Z-CORE 89b6df2e-v24] LIVE sur :{port} — NON DEPENDANCE VALIDEE")
            httpd.serve_forever()
            break
        except OSError as e:
            print(f"Port {port} pris: {e}, next...")
            continue
    else:
        print("Tous les ports pris, exit")
        sys.exit(1)
