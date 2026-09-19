import os
import json

class IAInnovia:
    def __init__(self, zone_echange="/tmp/innovia_core.json"):
        self.zone_echange = zone_echange
        self.contexte_partage = {}
        self.charger_contexte()

    def charger_contexte(self):
        if os.path.exists(self.zone_echange):
            with open(self.zone_echange, 'r', encoding='utf-8') as f:
                self.contexte_partage = json.load(f)

    def synchroniser_variable(self, cle, valeur):
        self.contexte_partage[cle] = valeur
        with open(self.zone_echange, 'w', encoding='utf-8') as f:
            json.dump(self.contexte_partage, f, indent=4)
        print(f"[✓] INNOVIA Sync : [{cle}] -> {valeur}")

if __name__ == "__main__":
    innovia = IAInnovia()
    innovia.synchroniser_variable("SYS_STATUS", "ISOLATED_ACTIVE")
