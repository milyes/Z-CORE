# SAHBI-SA V6.2 DUAL GOLD | Z-PUCE-1line | Python 3.10+ | DENY_ALL_EXCEPT_VERIFIED
import hmac, hashlib, os, time
deny_list = {"*"}; z_core = [None]; z_puce = [0]

def boot():  # Boot: charge la clé 256 bits locale, fail-closed
    t = time.perf_counter_ns(); k = bytes.fromhex(os.environ.get("Z_KEY", ""))
    if len(k) != 32: raise SystemExit("DENY")
    z_core[0] = k; z_puce[0] = time.perf_counter_ns() - t; return z_puce[0]

def verify(uid: bytes, tag: bytes) -> bool:  # Verify: HMAC-SHA256 temps constant, refus par défaut
    return z_core[0] is not None and hmac.compare_digest(hmac.new(z_core[0], uid, hashlib.sha256).digest(), tag)

def encrypt(uid: bytes, tag: bytes, data: bytes, aad: bytes = b"") -> bytes:  # Encrypt: AES-256-GCM, nonce 96 bits aléatoire
    if not verify(uid, tag): raise PermissionError("DENY_ALL_EXCEPT_VERIFIED")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # FIPS: exige un OpenSSL validé
    n = os.urandom(12); return n + AESGCM(z_core[0]).encrypt(n, data, aad)

if __name__ == "__main__": print(boot(), "ns")  # Test
