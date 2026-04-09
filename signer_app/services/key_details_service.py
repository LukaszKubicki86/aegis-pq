from __future__ import annotations

import json
from pathlib import Path

from app.key_rotation_policy import evaluate_rotation_policy_from_metadata
from signer_app.models import KeyDetailsResult


def _read_key_payload(file_path: str | Path) -> dict:
    path = Path(file_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Key file must contain a JSON object.")
    return data


def _private_key_present(payload: dict) -> bool:
    return any(
        key in payload
        for key in (
            "private_key_hex",
            "private_key_encrypted",
            "is_encrypted",
            "ciphertext_b64",
            "encryption",
        )
    )


def _private_key_encrypted(payload: dict) -> bool:
    return bool(
        payload.get("private_key_encrypted")
        or payload.get("is_encrypted")
        or "ciphertext_b64" in payload
        or "encryption" in payload
    )


def _detect_key_kind(payload: dict) -> str:
    return "private" if _private_key_present(payload) else "public"


def _detect_storage_mode(payload: dict) -> str:
    if _private_key_encrypted(payload):
        return "encrypted"
    if "private_key_hex" in payload:
        return "plaintext"
    return "public-only"


def inspect_key_file(file_path: str | Path) -> KeyDetailsResult:
    path = Path(file_path)
    payload = _read_key_payload(path)

    public_key_hex = payload.get("public_key_hex")
    if not public_key_hex:
        raise ValueError("Key file does not contain public_key_hex.")

    key_kind = _detect_key_kind(payload)
    storage_mode = _detect_storage_mode(payload)
    public_key_size = len(bytes.fromhex(public_key_hex))

    policy = evaluate_rotation_policy_from_metadata(payload)

    return KeyDetailsResult(
        file_path=str(path),
        key_kind=key_kind,
        storage_mode=storage_mode,
        format_version=payload.get("format_version"),
        signature_standard=payload.get("signature_standard"),
        signature_family=payload.get("signature_family"),
        algorithm_name=payload.get("algorithm_name"),
        backend_algorithm_name=payload.get("backend_algorithm_name"),
        profile_name=payload.get("profile_name"),
        profile_description=payload.get("profile_description"),
        address=payload.get("address"),
        public_key_fingerprint=payload.get("public_key_fingerprint"),
        public_key_hex=public_key_hex,
        public_key_size=public_key_size,
        private_key_present=_private_key_present(payload),
        private_key_encrypted=_private_key_encrypted(payload),
        key_status=payload.get("key_status"),
        key_created_at_utc=payload.get("key_created_at_utc"),
        rotated_from=payload.get("rotated_from"),
        rotation_reason=payload.get("rotation_reason"),
        rotation_policy_name=policy.policy_name,
        rotation_policy_state=policy.state,
        rotation_policy_message=policy.message,
        recommended_rotation_after_days=policy.recommended_rotation_after_days,
        key_age_days=policy.age_days,
        rotation_due_at_utc=policy.due_at_utc,
        rotation_days_until_due=policy.days_until_due,
    )


def export_public_key_from_key_file(
    source_key_path: str | Path,
    output_path: str | Path | None = None,
) -> str:
    source_path = Path(source_key_path)
    payload = _read_key_payload(source_path)

    public_key_hex = payload.get("public_key_hex")
    if not public_key_hex:
        raise ValueError("Key file does not contain public_key_hex.")

    public_payload = {
        "format_version": "1.1",
        "signature_standard": payload.get("signature_standard", "FIPS 204"),
        "signature_family": payload.get("signature_family", "ML-DSA"),
        "algorithm_name": payload.get("algorithm_name"),
        "backend_algorithm_name": payload.get("backend_algorithm_name"),
        "profile_name": payload.get("profile_name"),
        "profile_description": payload.get("profile_description"),
        "address": payload.get("address"),
        "public_key_hex": public_key_hex,
        "public_key_fingerprint": payload.get("public_key_fingerprint"),
        "key_status": payload.get("key_status", "active"),
        "key_created_at_utc": payload.get("key_created_at_utc"),
        "rotated_from": payload.get("rotated_from"),
        "rotation_reason": payload.get("rotation_reason"),
    }

    if output_path:
        destination = Path(output_path)
    else:
        if source_path.name.endswith(".priv.json"):
            destination = source_path.with_name(source_path.name.replace(".priv.json", ".pub.json"))
        elif source_path.name.endswith(".pub.json"):
            destination = source_path
        else:
            destination = source_path.with_suffix(".pub.json")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(public_payload, indent=2), encoding="utf-8")
    return str(destination)