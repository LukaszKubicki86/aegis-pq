from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GenerateKeyResult:
    profile_name: str
    profile_description: str
    algorithm_name: str
    backend_algorithm_name: str
    public_key_hex: str
    private_key_hex: str
    public_key_path: str
    private_key_path: str
    public_key_fingerprint: str
    public_key_size: int
    private_key_size: int


@dataclass
class KeyDetailsResult:
    file_path: str
    key_kind: str
    storage_mode: str
    format_version: str | None
    signature_standard: str | None
    signature_family: str | None
    algorithm_name: str | None
    backend_algorithm_name: str | None
    profile_name: str | None
    profile_description: str | None
    address: str | None
    public_key_fingerprint: str | None
    public_key_hex: str
    public_key_size: int
    private_key_present: bool
    private_key_encrypted: bool
    key_status: str | None
    key_created_at_utc: str | None
    rotated_from: str | None
    rotation_reason: str | None
    rotation_policy_name: str | None
    rotation_policy_state: str | None
    rotation_policy_message: str | None
    recommended_rotation_after_days: int | None
    key_age_days: int | None
    rotation_due_at_utc: str | None
    rotation_days_until_due: int | None


@dataclass
class FileSignResult:
    file_path: str
    signature_path: str
    profile_name: str
    profile_description: str
    signature_standard: str
    signature_family: str
    algorithm_name: str
    backend_algorithm_name: str
    file_hash_algorithm: str
    file_hash_hex: str
    public_key_fingerprint: str
    signature_size: int
    created_at_utc: str


@dataclass
class FileVerifyResult:
    file_path: str
    signature_path: str
    is_valid: bool
    profile_name: str | None
    profile_description: str | None
    signature_standard: str | None
    signature_family: str | None
    algorithm_name: str | None
    backend_algorithm_name: str | None
    file_hash_algorithm: str | None
    file_hash_hex: str | None
    actual_file_hash_hex: str
    public_key_fingerprint: str | None
    signature_size: int | None
    created_at_utc: str | None
    message: str


@dataclass
class RotateKeyResult:
    old_private_key_path: str
    updated_old_private_key_path: str
    new_private_key_path: str
    new_public_key_path: str
    old_address: str
    new_address: str
    profile_name: str
    profile_description: str
    algorithm_name: str
    backend_algorithm_name: str
    public_key_fingerprint: str
    key_status: str
    key_created_at_utc: str | None
    rotated_from: str | None
    rotation_reason: str | None
    new_private_key_encrypted: bool