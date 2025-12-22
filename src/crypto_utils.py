# src/crypto_utils.py

"""
Phase 2: Cryptography utilities for Shadow-Pixel

Implements:
- Password-based key derivation (PBKDF2)
- AES-256-GCM authenticated encryption
- Deterministic binary-safe output for steganography

No image logic exists here.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import os


# -----------------------------
# Key Derivation
# -----------------------------

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit AES key from a password using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,               # 256-bit key
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))


# -----------------------------
# Encryption
# -----------------------------

def encrypt_message(plaintext: str, password: str) -> bytes:
    """
    Encrypt plaintext using AES-256-GCM.

    Output format:
    [16 bytes salt][12 bytes nonce][ciphertext + tag]
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext.encode("utf-8"),
        None
    )

    return salt + nonce + ciphertext


def decrypt_message(encrypted_data: bytes, password: str) -> str:
    """
    Decrypt AES-256-GCM encrypted data.
    """
    if len(encrypted_data) < 28:
        raise ValueError("Encrypted data too short")

    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ciphertext = encrypted_data[28:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")
