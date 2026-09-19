import sys
import time

class IAInnoviaVolatile:
    def __init__(self):
        self.module_name = "IA_INNOVIA_RAM"
        # Dictionnaire en mémoire vive uniquement
        self._ram_state = {}

    def synchroniser_variable(self, cle, valeur):
        # Stockage pur en RAM
        self._ram_state[cle] = {
            "valeur": valeur,
            "timestamp": time.time()
        }
        print(f"[✓] INNOVIA Volatile (RAM Only) : [{cle}] -> {valeur}")

    def lire_variable(self, cle):
        return self._ram_state.get(cle, {}).get("valeur", None)

if __name__ == "__main__":
    innovia = IAInnoviaVolatile()
    innovia.synchroniser_variable("SYS_STATUS", "ISOLATED_ACTIVE_VOLATILE")
    print(f"[*] Vérification RAM : SYS_STATUS = {innovia.lire_variable('SYS_STATUS')}")
