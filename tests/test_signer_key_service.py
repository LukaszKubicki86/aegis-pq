import json

from signer_app.services.key_service import generate_pq_keypair


def test_generate_pq_keypair_creates_files_and_metadata(tmp_path):
    result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice",
        profile_name="hardened",
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"
    assert result.public_key_size > 0
    assert result.private_key_size > 0
    assert result.public_key_fingerprint.startswith("APQFP_")

    public_path = tmp_path / "alice.pub.json"
    private_path = tmp_path / "alice.priv.json"

    assert public_path.exists()
    assert private_path.exists()

    public_key_data = json.loads(public_path.read_text(encoding="utf-8"))
    private_key_data = json.loads(private_path.read_text(encoding="utf-8"))

    assert public_key_data["format_version"] == "1.1"
    assert public_key_data["key_status"] == "active"
    assert public_key_data["key_created_at_utc"]
    assert public_key_data["rotated_from"] is None
    assert public_key_data["rotation_reason"] is None

    assert private_key_data["is_encrypted"] is False
    assert private_key_data["private_key_hex"]
    assert private_key_data["public_key_fingerprint"].startswith("APQFP_")
    assert private_key_data["key_status"] == "active"
    assert private_key_data["key_created_at_utc"]
    assert private_key_data["rotated_from"] is None
    assert private_key_data["rotation_reason"] is None


def test_generate_pq_keypair_with_password_creates_encrypted_private_key_file(tmp_path):
    result = generate_pq_keypair(
        output_dir=tmp_path,
        name="alice_secure",
        profile_name="hardened",
        password="Correct-Horse-Battery-Staple",
    )

    assert result.profile_name == "hardened"
    assert result.backend_algorithm_name == "ML-DSA-65"

    private_key_data = json.loads((tmp_path / "alice_secure.priv.json").read_text(encoding="utf-8"))

    assert private_key_data["is_encrypted"] is True
    assert private_key_data["format_version"] == "2.0"
    assert "private_key_hex" not in private_key_data
    assert private_key_data["key_status"] == "active"
    assert private_key_data["key_created_at_utc"]

    encryption = private_key_data["encryption"]
    assert encryption["kdf"]["name"] == "argon2id"
    assert encryption["cipher"]["name"] == "aes-256-gcm"
    assert encryption["ciphertext_b64"]