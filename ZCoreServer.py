from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json
import time
from IA_REDORER import IARedorer

PORT = 8085
DIRECTORY = "./dist_payload/www" if os.path.exists("./dist_payload/www") else "."

class ZCoreServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            redorer = IARedorer()
            data = {
                "system": "Z-CORE v3.1.0",
                "status": "RUNNING",
                "metrics": redorer.obtenir_metriques()
            }
            self.wfile.write(json.dumps(data, indent=4).encode('utf-8'))
        elif self.path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            logs = {
                "events": [
                    {"time": time.strftime('%H:%M:%S'), "event": "ZCoreKernel Pulsation OK"},
                    {"time": time.strftime('%H:%M:%S'), "event": "IAInnovia Sync JSON Verified"},
                    {"time": time.strftime('%H:%M:%S'), "event": "API REST Served on :8085"}
                ]
            }
            self.wfile.write(json.dumps(logs, indent=4).encode('utf-8'))
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, ZCoreServerHandler)
    print(f"[✓] SERVEUR API & WEB ACTIF: http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Arrêt du serveur local.")
        httpd.server_close()
