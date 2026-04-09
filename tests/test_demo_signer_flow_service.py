import pytest

from signer_app.services.demo_signer_flow_service import run_demo_signer_flow
from signer_app.services.private_key_store import PrivateKeyDecryptionError


def test_run_demo_signer_flow_hardened(tmp_path):
    result = run_demo_signer_flow(
        work_dir=tmp_path,
        profile_name="hardened",
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"

    assert result.key_result.profile_name == "hardened"
    assert result.sign_result.profile_name == "hardened"

    assert result.verify_before_result.is_valid is True
    assert result.verify_before_result.message == "Signature valid."

    assert result.verify_after_result.is_valid is False
    assert "changed" in result.verify_after_result.message.lower()


def test_run_demo_signer_flow_max(tmp_path):
    result = run_demo_signer_flow(
        work_dir=tmp_path,
        profile_name="max",
    )

    assert result.profile_name == "max"
    assert result.backend_algorithm_name == "ML-DSA-87"
    assert result.verify_before_result.is_valid is True
    assert result.verify_after_result.is_valid is False


def test_run_demo_signer_flow_with_encrypted_private_key(tmp_path):
    result = run_demo_signer_flow(
        work_dir=tmp_path,
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"
    assert result.verify_before_result.is_valid is True
    assert result.verify_after_result.is_valid is False


def test_run_demo_signer_flow_with_invalid_password_fails(tmp_path):
    from signer_app.services.key_service import generate_pq_keypair
    from signer_app.services.file_sign_service import sign_file_with_private_key

    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="demo_user",
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis signer", encoding="utf-8")

    with pytest.raises(PrivateKeyDecryptionError):
        sign_file_with_private_key(
            file_path=input_file,
            private_key_path=key_result.private_key_path,
            password="wrong-password",
        )