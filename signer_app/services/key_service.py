from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.pq_policy import get_pq_profile
from app.pq_real_wallet import PQRealWallet
from signer_app.models import GenerateKeyResult
from signer_app.services.private_key_store import (
    build_encrypted_private_key_payload,
    build_plaintext_private_key_payload,
)


def _fingerprint_from_public_key(public_key_hex: str) -> str:
    digest = hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:16]
    return f"APQFP_{digest}"


def generate_pq_keypair(
    output_dir: str | Path,
    name: str,
    profile_name: str = "standard",
    password: str | None = None,
) -> GenerateKeyResult:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    profile = get_pq_profile(profile_name)

    wallet = PQRealWallet.create(
        profile.backend_algorithm,
        profile_name=profile.name,
        profile_description=profile.description,
    )

    public_key_fingerprint = _fingerprint_from_public_key(wallet.public_key_hex)

    public_key_path = output_path / f"{name}.pub.json"
    private_key_path = output_path / f"{name}.priv.json"

    public_key_payload = {
        "format_version": "1.1",
        "signature_standard": "FIPS 204",
        "signature_family": "ML-DSA",
        "algorithm_name": wallet.algorithm_name,
        "backend_algorithm_name": wallet.backend_algorithm_name,
        "profile_name": wallet.profile_name,
        "profile_description": wallet.profile_description,
        "address": wallet.address,
        "public_key_hex": wallet.public_key_hex,
        "public_key_fingerprint": public_key_fingerprint,
        "key_status": wallet.key_status,
        "key_created_at_utc": wallet.key_created_at_utc,
        "rotated_from": wallet.rotated_from,
        "rotation_reason": wallet.rotation_reason,
    }

    if password:
        private_key_payload = build_encrypted_private_key_payload(
            algorithm_name=wallet.algorithm_name,
            backend_algorithm_name=wallet.backend_algorithm_name,
            profile_name=wallet.profile_name,
            profile_description=wallet.profile_description,
            address=wallet.address,
            public_key_hex=wallet.public_key_hex,
            private_key_hex=wallet.private_key_hex,
            public_key_fingerprint=public_key_fingerprint,
            password=password,
        )
    else:
        private_key_payload = build_plaintext_private_key_payload(
            algorithm_name=wallet.algorithm_name,
            backend_algorithm_name=wallet.backend_algorithm_name,
            profile_name=wallet.profile_name,
            profile_description=wallet.profile_description,
            address=wallet.address,
            public_key_hex=wallet.public_key_hex,
            private_key_hex=wallet.private_key_hex,
            public_key_fingerprint=public_key_fingerprint,
        )

    private_key_payload["key_status"] = wallet.key_status
    private_key_payload["key_created_at_utc"] = wallet.key_created_at_utc
    private_key_payload["rotated_from"] = wallet.rotated_from
    private_key_payload["rotation_reason"] = wallet.rotation_reason

    public_key_path.write_text(json.dumps(public_key_payload, indent=2), encoding="utf-8")
    private_key_path.write_text(json.dumps(private_key_payload, indent=2), encoding="utf-8")

    return GenerateKeyResult(
        profile_name=profile.name,
        profile_description=profile.description,
        algorithm_name=wallet.algorithm_name,
        backend_algorithm_name=wallet.backend_algorithm_name,
        public_key_hex=wallet.public_key_hex,
        private_key_hex=wallet.private_key_hex,
        public_key_path=str(public_key_path),
        private_key_path=str(private_key_path),
        public_key_fingerprint=public_key_fingerprint,
        public_key_size=len(bytes.fromhex(wallet.public_key_hex)),
        private_key_size=len(bytes.fromhex(wallet.private_key_hex)),
    )