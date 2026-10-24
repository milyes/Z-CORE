# SAHBI-SA V6.2 DUAL GOLD | Z-PUCE-1line | Python 3.10+
# Version défendable TELUS #AidonsNosPME 2026 - NetSecurePro
# 100% local · Aucune donnée ne sort · Fail-Closed: DENY_ALL_EXCEPT_VERIFIED
# Builds FAST et FIPS avec OpenSSL
# Cibles : ~1,3 µs à chaud (en cours de mesure) · État interne ≤ 872 octets (objectif de conception)
# Conçu pour faciliter la conformité à la Loi 25
# Aucune allégation FIPS 140-3 validée CMVP - Compatible FIPS via module OpenSSL validé requis

import hmac, hashlib, os, time
from typing import Optional

# État interne visé ≤ 872 octets (objectif) = clé 32o + métriques minimales, pas RAM process
z_core: list[Optional[bytes]] = [None]
z_puce_ns: list[int] = [0]

def boot() -> int:
    """Boot fail-closed: charge clé locale 32o depuis Z_KEY env. Si absent/invalide -> DENY."""
    t0 = time.perf_counter_ns()
    hex_key = os.environ.get("Z_KEY", "").strip()
    try:
        k = bytes.fromhex(hex_key)
    except ValueError:
        raise SystemExit("DENY - Z_KEY hex invalide")
    if len(k) != 32:
        raise SystemExit("DENY - Z_KEY doit être 32 octets (64 hex)")
    z_core[0] = k
    dt = time.perf_counter_ns() - t0
    z_puce_ns[0] = dt
    return dt  # Retourne ns pour bench, ne pas publier comme RECORD sans protocole

def verify(uid: bytes, tag: bytes) -> bool:
    """Verify HMAC-SHA256 temps constant. Refus par défaut si non booté."""
    key = z_core[0]
    if key is None:
        return False
    # hmac.compare_digest = protection timing-attack
    expected = hmac.new(key, uid, hashlib.sha256).digest()
    return hmac.compare_digest(expected, tag)

def encrypt(uid: bytes, tag: bytes, data: bytes, aad: bytes = b"") -> bytes:
    """
    Encrypt AES-256-GCM, nonce 96 bits aléatoire.
    Fail-Closed: DENY_ALL_EXCEPT_VERIFIED si verify() échoue.
    Dépendance: cryptography -> OpenSSL. Mode FIPS = compatible FIPS 140-3 via OpenSSL
    si le module OpenSSL sous-jacent est validé CMVP sur la plateforme cible (non revendiqué ici).
    """
    if not verify(uid, tag):
        raise PermissionError("DENY_ALL_EXCEPT_VERIFIED")
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        raise RuntimeError("Dépendance manquante: pip install cryptography")
    key = z_core[0]
    assert key is not None
    nonce = os.urandom(12)
    # AESGCM utilise AES-256-GCM
    ct = AESGCM(key).encrypt(nonce, data, aad if aad else None)
    return nonce + ct  # Format: nonce(12) || ciphertext+tag(16)

if __name__ == "__main__":
    # Test local uniquement - ne mesure PAS encore la cible 1,3 µs à chaud (bench séparé requis)
    try:
        ns = boot()
        print(f"boot() OK - {ns} ns (mesure ponctuelle, pas RECORD)")
        print(f"État interne: clé={len(z_core[0])}o - objectif ≤872o pour z_state complet")
    except SystemExit as e:
        print(e)
