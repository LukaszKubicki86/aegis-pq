from signer_app.services.file_sign_service import sign_file_with_private_key
from signer_app.services.file_verify_service import verify_file_signature
from signer_app.services.key_service import generate_pq_keypair


def test_verify_file_signature_valid(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice",
        profile_name="hardened",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    sign_result = sign_file_with_private_key(
        file_path=input_file,
        private_key_path=key_result.private_key_path,
    )

    verify_result = verify_file_signature(
        file_path=input_file,
        signature_path=sign_result.signature_path,
    )

    assert verify_result.is_valid is True
    assert verify_result.backend_algorithm_name == "ML-DSA-65"
    assert verify_result.message == "Signature valid."


def test_verify_file_signature_invalid_after_file_change(tmp_path):
    key_result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice",
        profile_name="hardened",
    )

    input_file = tmp_path / "demo.txt"
    input_file.write_text("hello aegis", encoding="utf-8")

    sign_result = sign_file_with_private_key(
        file_path=input_file,
        private_key_path=key_result.private_key_path,
    )

    input_file.write_text("hello aegis modified", encoding="utf-8")

    verify_result = verify_file_signature(
        file_path=input_file,
        signature_path=sign_result.signature_path,
    )

    assert verify_result.is_valid is False
    assert "changed" in verify_result.message.lower()