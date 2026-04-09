from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any


DEFAULT_ROTATION_WINDOWS_DAYS: dict[str, int] = {
    "standard": 365,
    "hardened": 365,
    "max": 548,  # ~18 months
}

BACKEND_TO_PROFILE: dict[str, str] = {
    "ML-DSA-44": "standard",
    "ML-DSA-65": "hardened",
    "ML-DSA-87": "max",
}

DUE_SOON_THRESHOLD_DAYS = 30
ALLOWED_SIGNING_POLICY_STATES = {"ok", "due_soon"}


@dataclass(frozen=True)
class RotationPolicyResult:
    policy_name: str
    profile_name: str | None
    key_status: str
    created_at_utc: str | None
    rotation_reason: str | None
    recommended_rotation_after_days: int | None
    age_days: int | None
    due_at_utc: str | None
    days_until_due: int | None
    state: str
    message: str


def _parse_utc_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)

    return parsed.astimezone(UTC)


def _format_utc(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _resolve_profile_name(metadata: dict[str, Any]) -> str | None:
    profile_name = metadata.get("profile_name")
    if profile_name and str(profile_name).strip().lower() != "custom":
        return str(profile_name).strip().lower()

    backend_algorithm_name = metadata.get("backend_algorithm_name")
    if backend_algorithm_name:
        mapped = BACKEND_TO_PROFILE.get(str(backend_algorithm_name).strip())
        if mapped:
            return mapped

    return str(profile_name).strip().lower() if profile_name else None


def _recommended_days_for_profile(profile_name: str | None) -> int | None:
    if not profile_name:
        return None
    return DEFAULT_ROTATION_WINDOWS_DAYS.get(profile_name.lower())


def evaluate_rotation_policy_from_metadata(metadata: dict[str, Any]) -> RotationPolicyResult:
    profile_name = _resolve_profile_name(metadata)
    key_status = str(metadata.get("key_status") or "active").strip().lower()
    created_at_raw = metadata.get("key_created_at_utc")
    rotation_reason = metadata.get("rotation_reason")

    recommended_days = _recommended_days_for_profile(profile_name)
    created_at = _parse_utc_datetime(created_at_raw)

    if key_status == "rotated":
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=recommended_days,
            age_days=None if created_at is None else (datetime.now(UTC) - created_at).days,
            due_at_utc=None if created_at is None or recommended_days is None else _format_utc(created_at + timedelta(days=recommended_days)),
            days_until_due=None,
            state="rotated",
            message="This key has already been rotated and must not be used for active signing.",
        )

    if key_status == "revoked":
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=recommended_days,
            age_days=None if created_at is None else (datetime.now(UTC) - created_at).days,
            due_at_utc=None,
            days_until_due=None,
            state="revoked",
            message="This key has been revoked and must not be used.",
        )

    if created_at is None:
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=recommended_days,
            age_days=None,
            due_at_utc=None,
            days_until_due=None,
            state="unknown",
            message="Rotation policy cannot be evaluated because the key creation date is missing or invalid.",
        )

    if recommended_days is None:
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=None,
            age_days=(datetime.now(UTC) - created_at).days,
            due_at_utc=None,
            days_until_due=None,
            state="unknown",
            message="Rotation policy cannot be evaluated because the profile is unknown.",
        )

    now = datetime.now(UTC)
    age_days = (now - created_at).days
    due_at = created_at + timedelta(days=recommended_days)
    days_until_due = (due_at - now).days

    if days_until_due < 0:
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=recommended_days,
            age_days=age_days,
            due_at_utc=_format_utc(due_at),
            days_until_due=days_until_due,
            state="overdue",
            message="This key is past the mandatory rotation window and must be rotated before further signing use.",
        )

    if days_until_due <= DUE_SOON_THRESHOLD_DAYS:
        return RotationPolicyResult(
            policy_name="AEGIS_KEY_ROTATION_V1",
            profile_name=profile_name,
            key_status=key_status,
            created_at_utc=created_at_raw,
            rotation_reason=rotation_reason,
            recommended_rotation_after_days=recommended_days,
            age_days=age_days,
            due_at_utc=_format_utc(due_at),
            days_until_due=days_until_due,
            state="due_soon",
            message="This key is approaching the mandatory rotation window.",
        )

    return RotationPolicyResult(
        policy_name="AEGIS_KEY_ROTATION_V1",
        profile_name=profile_name,
        key_status=key_status,
        created_at_utc=created_at_raw,
        rotation_reason=rotation_reason,
        recommended_rotation_after_days=recommended_days,
        age_days=age_days,
        due_at_utc=_format_utc(due_at),
        days_until_due=days_until_due,
        state="ok",
        message="This key is within the mandatory rotation window.",
    )


def enforce_rotation_policy_for_signing(metadata: dict[str, Any]) -> RotationPolicyResult:
    policy = evaluate_rotation_policy_from_metadata(metadata)

    if policy.state not in ALLOWED_SIGNING_POLICY_STATES:
        raise ValueError(
            f"Key does not satisfy {policy.policy_name} for signing. "
            f"State={policy.state}. {policy.message}"
        )

    return policy