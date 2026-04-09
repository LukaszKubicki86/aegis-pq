from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.pq_real_wallet import PQRealWallet
from signer_app.models import RotateKeyResult
from signer_app.services.private_key_store import (
    build_private_key_payload,
    extract_private_key_hex,
)


def _fingerprint_from_public_key(public_key_hex: str) -> str:
    digest = hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:16]
    return f"APQFP_{digest}"


def _build_public_payload(wallet: PQRealWallet, public_key_fingerprint: str) -> dict:
    return {
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


def _build_private_payload(
    wallet: PQRealWallet,
    *,
    public_key_fingerprint: str,
    password: str | None,
) -> dict:
    payload = {
        "format_version": "2.0",
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
    payload.update(
        build_private_key_payload(
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
    )
    return payload


def rotate_key_file(
    *,
    private_key_path: str | Path,
    new_key_name: str,
    output_dir: str | Path | None = None,
    password: str | None = None,
    new_password: str | None = None,
    rotation_reason: str | None = None,
) -> RotateKeyResult:
    source_path = Path(private_key_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Private key file not found: {source_path}")

    payload = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Private key file must contain a JSON object.")

    required_fields = [
        "algorithm_name",
        "backend_algorithm_name",
        "profile_name",
        "profile_description",
        "address",
        "public_key_hex",
    ]
    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Private key file missing field: {field}")

    private_key_hex = extract_private_key_hex(payload, password=password)

    old_wallet = PQRealWallet(
        algorithm_name=payload["algorithm_name"],
        backend_algorithm_name=payload["backend_algorithm_name"],
        private_key_hex=private_key_hex,
        public_key_hex=payload["public_key_hex"],
        address=payload["address"],
        profile_name=payload.get("profile_name"),
        profile_description=payload.get("profile_description"),
        key_status=payload.get("key_status", "active"),
        key_created_at_utc=payload.get("key_created_at_utc") or "",
        rotated_from=payload.get("rotated_from"),
        rotation_reason=payload.get("rotation_reason"),
    )

    rotated_wallet = old_wallet.rotate(rotation_reason=rotation_reason)

    destination_dir = Path(output_dir) if output_dir else source_path.parent
    destination_dir.mkdir(parents=True, exist_ok=True)

    new_private_key_path = destination_dir / f"{new_key_name}.priv.json"
    new_public_key_path = destination_dir / f"{new_key_name}.pub.json"

    if new_private_key_path.exists() or new_public_key_path.exists():
        raise ValueError(f"Target key '{new_key_name}' already exists in {destination_dir}")

    old_fingerprint = payload.get("public_key_fingerprint") or _fingerprint_from_public_key(old_wallet.public_key_hex)
    new_fingerprint = _fingerprint_from_public_key(rotated_wallet.public_key_hex)

    old_payload_updated = _build_private_payload(
        old_wallet,
        public_key_fingerprint=old_fingerprint,
        password=password,
    )
    new_private_payload = _build_private_payload(
        rotated_wallet,
        public_key_fingerprint=new_fingerprint,
        password=new_password,
    )
    new_public_payload = _build_public_payload(
        rotated_wallet,
        public_key_fingerprint=new_fingerprint,
    )

    source_path.write_text(json.dumps(old_payload_updated, indent=2), encoding="utf-8")
    new_private_key_path.write_text(json.dumps(new_private_payload, indent=2), encoding="utf-8")
    new_public_key_path.write_text(json.dumps(new_public_payload, indent=2), encoding="utf-8")

    return RotateKeyResult(
        old_private_key_path=str(source_path),
        updated_old_private_key_path=str(source_path),
        new_private_key_path=str(new_private_key_path),
        new_public_key_path=str(new_public_key_path),
        old_address=old_wallet.address,
        new_address=rotated_wallet.address,
        profile_name=rotated_wallet.profile_name or "unknown",
        profile_description=rotated_wallet.profile_description or "",
        algorithm_name=rotated_wallet.algorithm_name,
        backend_algorithm_name=rotated_wallet.backend_algorithm_name,
        public_key_fingerprint=new_fingerprint,
        key_status=rotated_wallet.key_status,
        key_created_at_utc=rotated_wallet.key_created_at_utc,
        rotated_from=rotated_wallet.rotated_from,
        rotation_reason=rotated_wallet.rotation_reason,
        new_private_key_encrypted=bool(new_password),
    )