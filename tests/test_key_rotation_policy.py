from app.key_rotation_policy import (
    enforce_rotation_policy_for_signing,
    evaluate_rotation_policy_from_metadata,
)


def test_rotation_policy_ok_for_fresh_active_key():
    metadata = {
        "profile_name": "hardened",
        "key_status": "active",
        "key_created_at_utc": "2026-04-08T00:00:00Z",
        "rotation_reason": None,
    }

    result = evaluate_rotation_policy_from_metadata(metadata)
    assert result.state in {"ok", "due_soon"}


def test_rotation_policy_blocks_rotated_key_for_signing():
    metadata = {
        "profile_name": "hardened",
        "key_status": "rotated",
        "key_created_at_utc": "2026-04-08T00:00:00Z",
        "rotation_reason": "scheduled rotation",
    }

    try:
        enforce_rotation_policy_for_signing(metadata)
    except ValueError as exc:
        assert "does not satisfy AEGIS_KEY_ROTATION_V1 for signing" in str(exc)
        assert "State=rotated" in str(exc)
    else:
        raise AssertionError("Expected rotated key to be rejected for signing")


def test_rotation_policy_blocks_missing_creation_date_for_signing():
    metadata = {
        "profile_name": "hardened",
        "key_status": "active",
        "key_created_at_utc": None,
        "rotation_reason": None,
    }

    try:
        enforce_rotation_policy_for_signing(metadata)
    except ValueError as exc:
        assert "State=unknown" in str(exc)
    else:
        raise AssertionError("Expected key with missing creation date to be rejected")