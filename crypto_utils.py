"""Password hashing and symmetric encryption helpers."""

import base64
import hashlib

from cryptography.fernet import Fernet

PBKDF2_ITERATIONS = 390_000


def derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    """Derive a urlsafe-base64 Fernet key from a password and salt via PBKDF2-HMAC-SHA256."""
    raw = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)
    return base64.urlsafe_b64encode(raw)


def hash_password(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    """Derive a raw PBKDF2 hash suitable for storing/verifying a login password."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)


def encrypt_bytes(key: bytes, plaintext: bytes) -> bytes:
    return Fernet(key).encrypt(plaintext)


def decrypt_bytes(key: bytes, token: bytes) -> bytes:
    return Fernet(key).decrypt(token)
