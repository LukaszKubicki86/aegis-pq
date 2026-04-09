from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.pq_real_wallet import PQRealWallet
from signer_app.models import FileVerifyResult


def _sha256_file(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as handle:
        while chunk := handle.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_file_signature(
    file_path: str | Path,
    signature_path: str | Path,
) -> FileVerifyResult:
    input_file = Path(file_path)
    signature_file = Path(signature_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not signature_file.exists():
        raise FileNotFoundError(f"Signature file not found: {signature_file}")

    signature_data = json.loads(signature_file.read_text(encoding="utf-8"))

    required_fields = [
        "format_version",
        "signature_standard",
        "signature_family",
        "algorithm_name",
        "backend_algorithm_name",
        "profile_name",
        "profile_description",
        "file_hash_algorithm",
        "file_hash_hex",
        "public_key_fingerprint",
        "public_key_hex",
        "signature_hex",
        "signature_size",
        "created_at_utc",
    ]
    for field in required_fields:
        if field not in signature_data:
            raise ValueError(f"Signature file missing field: {field}")

    if signature_data["format_version"] != "1.0":
        raise ValueError(f"Unsupported signature format version: {signature_data['format_version']}")

    if signature_data["file_hash_algorithm"] != "sha256":
        raise ValueError(f"Unsupported hash algorithm: {signature_data['file_hash_algorithm']}")

    actual_file_hash_hex = _sha256_file(input_file)
    expected_file_hash_hex = signature_data["file_hash_hex"]

    if actual_file_hash_hex != expected_file_hash_hex:
        return FileVerifyResult(
            file_path=str(input_file),
            signature_path=str(signature_file),
            is_valid=False,
            profile_name=signature_data.get("profile_name"),
            profile_description=signature_data.get("profile_description"),
            signature_standard=signature_data.get("signature_standard"),
            signature_family=signature_data.get("signature_family"),
            algorithm_name=signature_data.get("algorithm_name"),
            backend_algorithm_name=signature_data.get("backend_algorithm_name"),
            file_hash_algorithm=signature_data.get("file_hash_algorithm"),
            file_hash_hex=expected_file_hash_hex,
            actual_file_hash_hex=actual_file_hash_hex,
            public_key_fingerprint=signature_data.get("public_key_fingerprint"),
            signature_size=signature_data.get("signature_size"),
            created_at_utc=signature_data.get("created_at_utc"),
            message="The file has changed or the signature metadata does not match.",
        )

    verifier_wallet = PQRealWallet(
        algorithm_name=signature_data["algorithm_name"],
        backend_algorithm_name=signature_data["backend_algorithm_name"],
        private_key_hex="",
        public_key_hex=signature_data["public_key_hex"],
        address=PQRealWallet.derive_address(signature_data["public_key_hex"]),
        profile_name=signature_data.get("profile_name"),
        profile_description=signature_data.get("profile_description"),
    )

    is_valid = verifier_wallet.verify_message(
        bytes.fromhex(actual_file_hash_hex),
        bytes.fromhex(signature_data["signature_hex"]),
    )

    return FileVerifyResult(
        file_path=str(input_file),
        signature_path=str(signature_file),
        is_valid=is_valid,
        profile_name=signature_data.get("profile_name"),
        profile_description=signature_data.get("profile_description"),
        signature_standard=signature_data.get("signature_standard"),
        signature_family=signature_data.get("signature_family"),
        algorithm_name=signature_data.get("algorithm_name"),
        backend_algorithm_name=signature_data.get("backend_algorithm_name"),
        file_hash_algorithm=signature_data.get("file_hash_algorithm"),
        file_hash_hex=expected_file_hash_hex,
        actual_file_hash_hex=actual_file_hash_hex,
        public_key_fingerprint=signature_data.get("public_key_fingerprint"),
        signature_size=signature_data.get("signature_size"),
        created_at_utc=signature_data.get("created_at_utc"),
        message="Signature valid." if is_valid else "Signature invalid.",
    )