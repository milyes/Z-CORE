# Z-CORE v3.1.0 — Sovereign Isolated Core System

**Z-CORE v3.1.0** est une architecture souveraine, autonome et isolée, conçue spécifiquement pour les environnements restreints (Termux / Linux). Elle intègre un bus de données 100% volatile (RAM-only), des métriques temps réel et une interface API REST embarquée.

---

## 🏛️ Architecture Système

| Module / Script | Rôle & Fonctionnalité | Type d'Exécution |
| :--- | :--- | :--- |
| **`ZCoreKernel.py`** | Noyau central d'orchestration et battement de cœur | Python 3 / Kernel Native |
| **`IAInnovia.py`** | Moteur de synchronisation de contexte 100% Volatile (Zero Disk Trace) | Flux RAM Mémoire Vive |
| **`IA_REDORER.py`** | Module de diagnostic, métriques système et optimisation | Télémétrie & Nettoyage |
| **`ZCoreServer.py`** | Serveur HTTP & API REST JSON (`/api/status`, `/api/logs`) sur le port 8085 | API / Dashboard Web |
| **`ZCoreTunnel.py`** | Service de tunneling et gestion des flux réseau | Proxification Isolée |
| **`master_orchestrator.sh`** | Orchestrateur maître du cycle de vie des services | Pipeline Bash |
| **`deploy_ghpages.sh`** | Agent de synchronisation automatisée vers GitHub | Pipeline Git Distant |
| **`autostart.sh`** | Intégration du démarrage automatique dans `~/.bashrc` | Persistence Shell |

---

## 🚀 Utilisation & Commandes

### 1. Démarrage Global
Pour diagnostiquer, initialiser la RAM et démarrer le serveur Web/API en tâche de fond :
```bash
./master_orchestrator.sh

