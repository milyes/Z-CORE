from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8080
DIRECTORY = "./dist_payload/www" if os.path.exists("./dist_payload/www") else "."

class ZCoreServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def log_message(self, format, *args):
        pass 

if __name__ == "__main__":
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, ZCoreServerHandler)
    print(f"[✓] SERVEUR ACTIF: http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Arrêt du serveur local.")
        httpd.server_close()
