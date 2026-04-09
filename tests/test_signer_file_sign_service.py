import json

import pytest

from signer_app.services.file_sign_service import sign_file_with_private_key
from signer_app.services.key_service import generate_pq_keypair
from signer_app.services.private_key_store import (
    PrivateKeyDecryptionError,
    PrivateKeyPasswordRequiredError,
)


def test_sign_file_creates_sig_json_with_plaintext_private_key(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice",
        profile_name="hardened",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    result = sign_file_with_private_key(
        file_path=input_file,
        private_key_path=key_result.private_key_path,
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"
    assert result.signature_size > 0

    sig_path = tmp_path / "demo.txt.sig"
    assert sig_path.exists()

    sig_data = json.loads(sig_path.read_text(encoding="utf-8"))
    assert sig_data["signature_standard"] == "FIPS 204"
    assert sig_data["signature_family"] == "ML-DSA"
    assert sig_data["profile_name"] == "hardened"
    assert sig_data["backend_algorithm_name"] == "ML-DSA-65"
    assert sig_data["signature_size"] > 0
    assert sig_data["signature_hex"]


def test_sign_file_creates_sig_json_with_encrypted_private_key_and_password(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice_secure",
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    result = sign_file_with_private_key(
        file_path=input_file,
        private_key_path=key_result.private_key_path,
        password="Correct-Horse-Battery-Staple",
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"
    assert result.signature_size > 0

    sig_path = tmp_path / "demo.txt.sig"
    assert sig_path.exists()

    sig_data = json.loads(sig_path.read_text(encoding="utf-8"))
    assert sig_data["signature_hex"]
    assert sig_data["signature_size"] > 0


def test_sign_file_with_encrypted_private_key_requires_password(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice_secure",
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    with pytest.raises(PrivateKeyPasswordRequiredError):
        sign_file_with_private_key(
            file_path=input_file,
            private_key_path=key_result.private_key_path,
        )


def test_sign_file_with_encrypted_private_key_rejects_invalid_password(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice_secure",
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    with pytest.raises(PrivateKeyDecryptionError):
        sign_file_with_private_key(
            file_path=input_file,
            private_key_path=key_result.private_key_path,
            password="wrong-password",
        )