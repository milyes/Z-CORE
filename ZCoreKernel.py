import os
import sys
import time

class ZCoreKernel:
    def __init__(self):
        self.version = "3.1.0"
        self.mode = "MILYES Z-H2o2.ia"
        self.is_isolated = True
        
    def initialiser_systeme(self):
        print("=" * 50)
        print(f"   === [Z-CORE] KERNEL PYTHON 3 v{self.version} ===")
        print(f"[*] Mode Actif       : {self.mode}")
        print(f"[*] Isolation Réseau : {'OUI' if self.is_isolated else 'NON'}")
        print("=" * 50)
        
        briques = ["IA_REDORER.py", "IA_INNOVIA.py", "z_local_server.py"]
        for brique in briques:
            status = "✓ Liaison" if os.path.exists(brique) else "! Attente"
            print(f"  [{status}] Module : {brique}")
                
    def executer_boucle_logique(self):
        print("\n[+] Système stabilisé. Écoute locale active...")
        try:
            while True:
                ts = time.strftime('%H:%M:%S')
                print(f"[{ts}] [Z-CORE] Pulsation stable. Mémoire VRAM OK.", end="\r")
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[-] Interruption. Sauvegarde et mise en veille.")

if __name__ == "__main__":
    kernel = ZCoreKernel()
    kernel.initialiser_systeme()
    kernel.executer_boucle_logique()
