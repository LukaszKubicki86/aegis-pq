from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from app.key_rotation_policy import enforce_rotation_policy_for_signing
from app.pq_real_wallet import PQRealWallet
from signer_app.models import FileSignResult
from signer_app.services.private_key_store import extract_private_key_hex


def _fingerprint_from_public_key(public_key_hex: str) -> str:
    digest = hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:16]
    return f"APQFP_{digest}"


def _sha256_file(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as handle:
        while chunk := handle.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def sign_file_with_private_key(
    file_path: str | Path,
    private_key_path: str | Path,
    signature_path: str | Path | None = None,
    password: str | None = None,
) -> FileSignResult:
    input_file = Path(file_path)
    private_key_file = Path(private_key_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not private_key_file.exists():
        raise FileNotFoundError(f"Private key file not found: {private_key_file}")

    private_key_data = json.loads(private_key_file.read_text(encoding="utf-8"))

    required_fields = [
        "algorithm_name",
        "backend_algorithm_name",
        "profile_name",
        "profile_description",
        "address",
        "public_key_hex",
    ]
    for field in required_fields:
        if field not in private_key_data:
            raise ValueError(f"Private key file missing field: {field}")

    enforce_rotation_policy_for_signing(private_key_data)

    private_key_hex = extract_private_key_hex(private_key_data, password=password)

    wallet = PQRealWallet(
        algorithm_name=private_key_data["algorithm_name"],
        backend_algorithm_name=private_key_data["backend_algorithm_name"],
        private_key_hex=private_key_hex,
        public_key_hex=private_key_data["public_key_hex"],
        address=private_key_data["address"],
        profile_name=private_key_data.get("profile_name"),
        profile_description=private_key_data.get("profile_description"),
        key_status=private_key_data.get("key_status", "active"),
        key_created_at_utc=private_key_data.get("key_created_at_utc") or "",
        rotated_from=private_key_data.get("rotated_from"),
        rotation_reason=private_key_data.get("rotation_reason"),
    )

    file_hash_hex = _sha256_file(input_file)
    message_bytes = bytes.fromhex(file_hash_hex)
    signature_bytes = wallet.sign_message(message_bytes)
    signature_hex = signature_bytes.hex()

    created_at_utc = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    output_signature_path = (
        input_file.with_suffix(input_file.suffix + ".sig")
        if signature_path is None
        else Path(signature_path)
    )

    signature_payload = {
        "format_version": "1.0",
        "signature_standard": "FIPS 204",
        "signature_family": "ML-DSA",
        "algorithm_name": wallet.algorithm_name,
        "backend_algorithm_name": wallet.backend_algorithm_name,
        "profile_name": wallet.profile_name,
        "profile_description": wallet.profile_description,
        "file_name": input_file.name,
        "file_hash_algorithm": "sha256",
        "file_hash_hex": file_hash_hex,
        "public_key_fingerprint": _fingerprint_from_public_key(wallet.public_key_hex),
        "public_key_hex": wallet.public_key_hex,
        "signature_hex": signature_hex,
        "signature_size": len(signature_bytes),
        "created_at_utc": created_at_utc,
    }

    output_signature_path.write_text(
        json.dumps(signature_payload, indent=2),
        encoding="utf-8",
    )

    return FileSignResult(
        file_path=str(input_file),
        signature_path=str(output_signature_path),
        profile_name=wallet.profile_name or "unknown",
        profile_description=wallet.profile_description or "",
        signature_standard="FIPS 204",
        signature_family="ML-DSA",
        algorithm_name=wallet.algorithm_name,
        backend_algorithm_name=wallet.backend_algorithm_name,
        file_hash_algorithm="sha256",
        file_hash_hex=file_hash_hex,
        public_key_fingerprint=_fingerprint_from_public_key(wallet.public_key_hex),
        signature_size=len(signature_bytes),
        created_at_utc=created_at_utc,
    )