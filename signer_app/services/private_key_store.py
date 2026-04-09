from __future__ import annotations

from typing import Any

from app.private_key_store import (
    PrivateKeyDecryptionError,
    PrivateKeyPasswordRequiredError,
    build_private_key_payload as core_build_private_key_payload,
    decrypt_private_key_payload,
    extract_private_key_hex,
    public_key_fingerprint,
)


def build_plaintext_private_key_payload(
    *,
    algorithm_name: str,
    backend_algorithm_name: str,
    profile_name: str | None,
    profile_description: str | None,
    address: str,
    public_key_hex: str,
    private_key_hex: str,
    public_key_fingerprint: str,
) -> dict[str, Any]:
    payload = {
        "format_version": "2.0",
        "signature_standard": "FIPS 204",
        "signature_family": "ML-DSA",
        "algorithm_name": algorithm_name,
        "backend_algorithm_name": backend_algorithm_name,
        "profile_name": profile_name,
        "profile_description": profile_description,
        "address": address,
        "public_key_hex": public_key_hex,
        "public_key_fingerprint": public_key_fingerprint,
    }
    payload.update(
        core_build_private_key_payload(
            private_key_hex=private_key_hex,
            password=None,
        )
    )
    return payload


def build_encrypted_private_key_payload(
    *,
    algorithm_name: str,
    backend_algorithm_name: str,
    profile_name: str | None,
    profile_description: str | None,
    address: str,
    public_key_hex: str,
    private_key_hex: str,
    public_key_fingerprint: str,
    password: str,
) -> dict[str, Any]:
    payload = {
        "format_version": "2.0",
        "signature_standard": "FIPS 204",
        "signature_family": "ML-DSA",
        "algorithm_name": algorithm_name,
        "backend_algorithm_name": backend_algorithm_name,
        "profile_name": profile_name,
        "profile_description": profile_description,
        "address": address,
        "public_key_hex": public_key_hex,
        "public_key_fingerprint": public_key_fingerprint,
    }
    payload.update(
        core_build_private_key_payload(
            private_key_hex=private_key_hex,
            password=password,
        )
    )
    return payload


def build_private_key_payload(
    *,
    algorithm_name: str,
    backend_algorithm_name: str,
    profile_name: str | None,
    profile_description: str | None,
    address: str,
    public_key_hex: str,
    private_key_hex: str,
    public_key_fingerprint: str,
    password: str | None = None,
) -> dict[str, Any]:
    if password:
        return build_encrypted_private_key_payload(
            algorithm_name=algorithm_name,
            backend_algorithm_name=backend_algorithm_name,
            profile_name=profile_name,
            profile_description=profile_description,
            address=address,
            public_key_hex=public_key_hex,
            private_key_hex=private_key_hex,
            public_key_fingerprint=public_key_fingerprint,
            password=password,
        )

    return build_plaintext_private_key_payload(
        algorithm_name=algorithm_name,
        backend_algorithm_name=backend_algorithm_name,
        profile_name=profile_name,
        profile_description=profile_description,
        address=address,
        public_key_hex=public_key_hex,
        private_key_hex=private_key_hex,
        public_key_fingerprint=public_key_fingerprint,
    )


__all__ = [
    "PrivateKeyDecryptionError",
    "PrivateKeyPasswordRequiredError",
    "build_plaintext_private_key_payload",
    "build_encrypted_private_key_payload",
    "build_private_key_payload",
    "decrypt_private_key_payload",
    "extract_private_key_hex",
    "public_key_fingerprint",
]