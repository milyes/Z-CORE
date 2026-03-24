# AIZ-CORE

> Stack privée auto-hébergée avec IA intégrée, SSO unifié et souveraineté numérique maximale.

---

## Résumé

AIZ-CORE est une infrastructure hybride construite par un dev IA solo. Elle combine un cœur 100% auto-hébergé (inférence LLM, mail, SSO, stockage) avec des outils cloud assistés (Claude Code, Claude.ai, Azure CLI) utilisés de façon consciente et délibérée.

**Philosophie** : zéro dépendance cloud forcée sur les données critiques. Les outils cloud externes restent des assistants, jamais des dépositaires.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZONE SOUVERAINE (auto-hébergé)               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      Z-CORE IA                          │    │
│  │   Ollama · LiteLLM · MLflow · MinIO · Prefect           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────┐   ┌──────────────────────────────┐    │
│  │         Mail         │   │             SSO              │    │
│  │  Stalwart · Nextcloud│   │   Authentik · IAM unifié     │    │
│  └──────────────────────┘   └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   ZONE CLOUD US (assistants)                    │
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │   Z-Claude.code   │  │    Z-Claude.ai    │                   │
│  │  Claude Code CLI  │  │   claude.ai web   │                   │
│  │  api.anthropic.com│  │  api.anthropic.com│                   │
│  └───────────────────┘  └───────────────────┘                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      Z-Azure.Cli                        │    │
│  │         Azure CLI · services cloud Microsoft            │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Composants

### Z-CORE IA — inférence et pipelines ML

| Service | Image Docker | Port | Rôle |
|---|---|---|---|
| Ollama | `ollama/ollama:latest` | 11434 | Inférence LLM locale |
| Open WebUI | `ghcr.io/open-webui/open-webui` | 3000 | Interface chat |
| LiteLLM | `ghcr.io/berriai/litellm` | 4000 | API proxy OpenAI-compatible |
| MLflow | `ghcr.io/mlflow/mlflow` | 5000 | Tracking expériences ML |
| MinIO | `minio/minio` | 9000/9001 | Stockage datasets S3-compatible |
| Prefect | `prefecthq/prefect:2-latest` | 4200 | Orchestration pipelines |

**Modèles actifs (CPU only, Q4_K_M)**

| Modèle | RAM | Vitesse | Usage |
|---|---|---|---|
| Mistral 7B | ~5 Go | ~8 tok/s | Généraliste |
| Llama 3 8B | ~6 Go | ~7 tok/s | Raisonnement |
| Phi-3 Mini | ~3 Go | ~15 tok/s | Réponses rapides |
| DeepSeek-R1 7B | ~6 Go | ~7 tok/s | Analyse technique |

---

### Mail — communication souveraine

| Service | Image Docker | Port | Rôle |
|---|---|---|---|
| Stalwart Mail | `stalwartlabs/mail-server` | 25/587/993/8080 | SMTP + IMAP + Admin |
| Nextcloud | `nextcloud:27-apache` | 8081 | Agenda · Contacts · Fichiers |
| Collabora | `collabora/code` | 9980 | Édition docs en ligne |

**Configuration DNS requise**

```
@           MX  10  mail.mondomaine.fr.
mail        A       <IP_SERVEUR>
@           TXT     "v=spf1 ip4:<IP_SERVEUR> ~all"
_dmarc      TXT     "v=DMARC1; p=quarantine; rua=mailto:postmaster@mondomaine.fr"
mail._domainkey TXT "v=DKIM1; k=rsa; p=<CLÉ_PUBLIQUE_STALWART>"
```

---

### SSO — identité unifiée

| Service | Image Docker | Port | Rôle |
|---|---|---|---|
| Authentik | `ghcr.io/goauthentik/server` | 9000 | SSO · OIDC · SAML · MFA |
| Caddy | `caddy:latest` | 80/443 | Reverse proxy + TLS auto |

**Domaines exposés**

```
cloud.mondomaine.fr   → Nextcloud
mail.mondomaine.fr    → Stalwart Admin
auth.mondomaine.fr    → Authentik
ai.mondomaine.fr      → Open WebUI
api.mondomaine.fr     → LiteLLM
```

---

### Monitoring

| Service | Image Docker | Port | Rôle |
|---|---|---|---|
| Uptime Kuma | `louislam/uptime-kuma` | 3001 | Surveillance ports/services |
| Netdata | `netdata/netdata` | 19999 | Métriques système live |
| Gotify | `gotify/server` | 8090 | Push notifications souverain |

**Alertes configurées**

- SMTP port 25 — check toutes les 60s
- IMAP port 993 — check toutes les 60s
- Submission port 587 — check toutes les 60s
- Open WebUI — check HTTP toutes les 120s
- LiteLLM API — check HTTP toutes les 120s
- Disque > 80% — alerte Gotify immédiate
- RAM > 90% — alerte Gotify immédiate

---

### Assistants cloud (Z-Claude.code · Z-Claude.ai · Z-Azure.Cli)

> Ces composants sont des outils d'assistance au développement, pas des dépositaires de données.

| Composant | Fournisseur | Endpoint | Données transmises |
|---|---|---|---|
| Z-Claude.code | Anthropic (US) | api.anthropic.com | Prompts de code uniquement |
| Z-Claude.ai | Anthropic (US) | claude.ai | Prompts de développement |
| Z-Azure.Cli | Microsoft (US/EU) | management.azure.com | Commandes d'administration |

**Règles d'usage**

- Aucune donnée personnelle utilisateur ne transite via ces composants
- Aucun secret, credential ou clé API n'est inclus dans les prompts
- Les modèles de production restent sur Z-CORE IA (Ollama)
- Claude API = assistance développement uniquement, jamais inférence de production

---

## Analyse de souveraineté

| Couche | Composant | Souveraineté | Juridiction | Risque |
|---|---|---|---|---|
| IA / inférence | Z-CORE IA (Ollama) | ✅ Totale | Ton serveur | Nul |
| Mail | Stalwart + Nextcloud | ✅ Totale | Ton serveur | Nul |
| Identité | Authentik | ✅ Totale | Ton serveur | Nul |
| Stockage | MinIO | ✅ Totale | Ton serveur | Nul |
| Dev assistant IA | Z-Claude.code / Z-Claude.ai | ⚠️ Partielle | USA (Cloud Act) | Faible (prompts dev) |
| Infra cloud | Z-Azure.Cli | ⚠️ Partielle | USA/EU (Cloud Act) | Moyen (commandes admin) |

**Score souveraineté global : 7/10**

Données critiques (mails, fichiers, modèles, datasets) : 100% souveraines.
Flux de travail développement : dépendance consciente et maîtrisée aux assistants cloud.

---

## Plan de dérisquage (si souveraineté 10/10 requise)

### Remplacer Z-Claude.code / Z-Claude.ai

```bash
# Option 1 : Continue (serveur de code auto-hébergé)
docker run -d --name continue \
  -p 65432:65432 \
  -v ~/.continue:/root/.continue \
  continuedev/continue:latest

# Option 2 : Tâche dédiée dans LiteLLM (déjà dans Z-CORE IA)
# Pointer Continue vers http://localhost:4000 (LiteLLM)
# Modèle : deepseek-r1:7b ou mistral pour le code
```

```json
// ~/.continue/config.json
{
  "models": [{
    "title": "Z-CORE IA (local)",
    "provider": "openai",
    "model": "deepseek-r1",
    "apiBase": "http://localhost:4000",
    "apiKey": "sk-VOTRE_CLE_LITELLM"
  }]
}
```

### Remplacer Z-Azure.Cli

| Service Azure | Alternatif souverain | Hébergeur |
|---|---|---|
| Azure VMs | VPS Hetzner / Scaleway | DE / FR |
| Azure Storage | MinIO (déjà dans Z-CORE) | Ton serveur |
| Azure Container Apps | Coolify (self-hosted) | Ton serveur |
| Azure DevOps | Gitea + Woodpecker CI | Ton serveur |
| Azure AD | Authentik (déjà dans Z-CORE) | Ton serveur |

---

## Infrastructure matérielle

```
CPU    : x86_64 multi-core (≥ 8 cœurs physiques recommandés)
RAM    : 32 Go (20 Go alloués à Ollama, 12 Go aux autres services)
Disque : SSD NVMe ≥ 200 Go (modèles LLM : ~25 Go, données : variable)
Swap   : 16 Go SSD (sécurité OOM)
OS     : Debian 12 (Bookworm)
Réseau : IP fixe dédiée, PTR configuré
```

**Optimisations système actives**

```bash
vm.swappiness=10
vm.vfs_cache_pressure=50
OLLAMA_NUM_THREAD=8
OLLAMA_MAX_LOADED_MODELS=2
OLLAMA_KEEP_ALIVE=10m
```

---

## Backup

```bash
# Fréquence : quotidien à 02h00
# Rétention : 14 jours
# Destination : /var/backups/ + réplication optionnelle Hetzner StorageBox

Périmètre :
- /opt/stalwart-mail/data        (mails)
- /var/lib/docker/volumes/       (tous les volumes Docker)
- /opt/stalwart-mail/etc/dkim/   (clés DKIM)
- /etc/caddy/                    (config reverse proxy)
```

---

## Démarrage rapide

```bash
# 1. Cloner la config
git clone git@monrepo.fr:aiz-core/infra.git
cd infra

# 2. Copier et adapter les variables d'environnement
cp .env.example .env
nano .env   # Renseigner les mots de passe et domaines

# 3. Démarrer le cœur souverain
docker compose -f docker-compose.yml up -d

# 4. Démarrer le monitoring
docker compose -f docker-compose.monitoring.yml up -d

# 5. Télécharger les modèles LLM
docker exec ollama ollama pull mistral
docker exec ollama ollama pull phi3
docker exec ollama ollama pull deepseek-r1:7b

# 6. Vérifier l'état
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Checklist de mise en production

```
Infra
[ ] PTR (reverse DNS) configuré chez l'hébergeur
[ ] UFW actif (ports 25/587/993/80/443 uniquement)
[ ] Fail2ban installé et configuré

Mail
[ ] SPF publié en DNS
[ ] DKIM généré et publié en DNS
[ ] DMARC en mode quarantine
[ ] Score mail-tester.com ≥ 9/10

IA
[ ] LiteLLM API testée (curl /v1/models)
[ ] MLflow accessible (http://localhost:5000)
[ ] MinIO buckets créés (datasets, models)

SSO
[ ] Authentik admin créé
[ ] Applications OIDC configurées (Nextcloud, Open WebUI)
[ ] MFA activé sur le compte admin

Monitoring
[ ] Uptime Kuma monitors actifs (25/587/993)
[ ] Gotify push testé sur mobile
[ ] Alerte disque > 80% configurée

Backup
[ ] Premier backup manuel exécuté et vérifié
[ ] Cron backup actif
[ ] Test de restauration effectué
```

---

## Versions

| Composant | Version | Dernière vérification |
|---|---|---|
| Stalwart Mail | latest | 2026-03 |
| Nextcloud | 27-apache | 2026-03 |
| Authentik | latest | 2026-03 |
| Ollama | latest | 2026-03 |
| LiteLLM | main-latest | 2026-03 |
| MLflow | latest | 2026-03 |
| MinIO | latest | 2026-03 |
| Uptime Kuma | latest | 2026-03 |
| Caddy | latest | 2026-03 |

---

## Licence

Usage privé. Infrastructure personnelle. Non destinée à la distribution.
