from __future__ import annotations

import base64
import hashlib
from secrets import token_bytes
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


class PrivateKeyPasswordRequiredError(ValueError):
    pass


class PrivateKeyDecryptionError(ValueError):
    pass


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def _b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def _derive_key(
    password: str,
    *,
    salt: bytes,
    length: int,
    iterations: int,
    lanes: int,
    memory_cost: int,
) -> bytes:
    password_bytes = password.encode("utf-8")
    kdf = Argon2id(
        salt=salt,
        length=length,
        iterations=iterations,
        lanes=lanes,
        memory_cost=memory_cost,
    )
    return kdf.derive(password_bytes)


def build_plaintext_private_key_payload(private_key_hex: str) -> dict[str, Any]:
    if not private_key_hex:
        raise ValueError("Private key hex is required.")

    return {
        "is_encrypted": False,
        "private_key_hex": private_key_hex,
    }


def build_encrypted_private_key_payload(private_key_hex: str, password: str) -> dict[str, Any]:
    if not password:
        raise PrivateKeyPasswordRequiredError("Password is required to encrypt private key.")
    if not private_key_hex:
        raise ValueError("Private key hex is required.")

    salt = token_bytes(16)
    nonce = token_bytes(12)

    kdf_length = 32
    kdf_iterations = 3
    kdf_lanes = 4
    kdf_memory_cost = 65536

    derived_key = _derive_key(
        password,
        salt=salt,
        length=kdf_length,
        iterations=kdf_iterations,
        lanes=kdf_lanes,
        memory_cost=kdf_memory_cost,
    )

    aesgcm = AESGCM(derived_key)
    ciphertext = aesgcm.encrypt(nonce, private_key_hex.encode("utf-8"), None)

    return {
        "is_encrypted": True,
        "encryption": {
            "kdf": {
                "name": "argon2id",
                "salt_b64": _b64encode(salt),
                "length": kdf_length,
                "iterations": kdf_iterations,
                "lanes": kdf_lanes,
                "memory_cost": kdf_memory_cost,
            },
            "cipher": {
                "name": "aes-256-gcm",
                "nonce_b64": _b64encode(nonce),
            },
            "ciphertext_b64": _b64encode(ciphertext),
        },
    }


def build_private_key_payload(
    *,
    private_key_hex: str,
    password: str | None = None,
) -> dict[str, Any]:
    if password:
        return build_encrypted_private_key_payload(private_key_hex, password)
    return build_plaintext_private_key_payload(private_key_hex)


def decrypt_private_key_payload(payload: dict[str, Any], password: str | None) -> str:
    if not password:
        raise PrivateKeyPasswordRequiredError("Password is required to decrypt private key.")

    encryption = payload.get("encryption")
    if not isinstance(encryption, dict):
        raise PrivateKeyDecryptionError("Encrypted private key payload is missing encryption metadata.")

    kdf_data = encryption.get("kdf")
    cipher_data = encryption.get("cipher")
    ciphertext_b64 = encryption.get("ciphertext_b64")

    if not isinstance(kdf_data, dict) or not isinstance(cipher_data, dict) or not isinstance(ciphertext_b64, str):
        raise PrivateKeyDecryptionError("Encrypted private key payload is incomplete.")

    if kdf_data.get("name") != "argon2id":
        raise PrivateKeyDecryptionError(f"Unsupported KDF: {kdf_data.get('name')}")

    if cipher_data.get("name") != "aes-256-gcm":
        raise PrivateKeyDecryptionError(f"Unsupported cipher: {cipher_data.get('name')}")

    try:
        salt = _b64decode(kdf_data["salt_b64"])
        nonce = _b64decode(cipher_data["nonce_b64"])
        ciphertext = _b64decode(ciphertext_b64)

        derived_key = _derive_key(
            password,
            salt=salt,
            length=int(kdf_data["length"]),
            iterations=int(kdf_data["iterations"]),
            lanes=int(kdf_data["lanes"]),
            memory_cost=int(kdf_data["memory_cost"]),
        )

        aesgcm = AESGCM(derived_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        private_key_hex = plaintext.decode("utf-8")
    except InvalidTag as exc:
        raise PrivateKeyDecryptionError(
            "Failed to decrypt private key. The password may be invalid."
        ) from exc
    except KeyError as exc:
        raise PrivateKeyDecryptionError(
            f"Encrypted private key payload missing field: {exc.args[0]}"
        ) from exc
    except Exception as exc:
        raise PrivateKeyDecryptionError(f"Failed to decrypt private key: {type(exc).__name__}") from exc

    return private_key_hex


def extract_private_key_hex(payload: dict[str, Any], password: str | None = None) -> str:
    is_encrypted = bool(payload.get("is_encrypted", False))

    if is_encrypted:
        return decrypt_private_key_payload(payload, password)

    private_key_hex = payload.get("private_key_hex")
    if not isinstance(private_key_hex, str) or not private_key_hex:
        raise ValueError("Private key payload missing plaintext private_key_hex.")

    return private_key_hex


def public_key_fingerprint(public_key_hex: str) -> str:
    digest = hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:16]
    return f"APQFP_{digest}"