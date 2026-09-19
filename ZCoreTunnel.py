import time

class ZCoreTunnel:
    def __init__(self, endpoint="127.0.0.1", port=8021):
        self.endpoint = endpoint
        self.port = port
        self.is_active = False

    def open_tunnel(self):
        print(f"[*] [OPEN] Initialisation du tunnel sur {self.endpoint}:{self.port}...")
        time.sleep(1)
        self.is_active = True

    def lancer_flux(self):
        if not self.is_active:
            return False
        print("[✓] [LAUNCH] Tunnel opérationnel et routé.")
        return True

    def recevoir_rt(self, duree=3):
        print("\n=== [RECEIVE RT] CAPTATION FLUX LIVE ===")
        for i in range(1, duree + 1):
            print(f" -> [RT_STREAM] Pulsation {i} | OK", end="\r")
            time.sleep(1)

    def close_tunnel(self):
        self.is_active = False
        print("\n[✓] [CLOSE] Tunnel fermé. Confinement 100% rétabli.")

if __name__ == "__main__":
    tunnel = ZCoreTunnel()
    tunnel.open_tunnel()
    if tunnel.lancer_flux():
        tunnel.recevoir_rt()
        tunnel.close_tunnel()
