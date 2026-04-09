from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.private_key_store import build_private_key_payload, extract_private_key_hex


def _utc_now_z() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass
class PQRealWallet:
    algorithm_name: str
    backend_algorithm_name: str
    private_key_hex: str
    public_key_hex: str
    address: str
    signature_algorithm: str = "MLDSA_REAL_V1"
    profile_name: str | None = None
    profile_description: str | None = None
    key_status: str = "active"
    key_created_at_utc: str = field(default_factory=_utc_now_z)
    rotated_from: str | None = None
    rotation_reason: str | None = None

    @staticmethod
    def derive_address(public_key_hex: str) -> str:
        """
        Address derivation must stay identical to the backend adapter path
        used by Wallet/Transaction verification for MLDSA_REAL_V1.

        Canonical project format:
        APQ_ + first 40 hex chars of sha256(public_key_hex encoded as utf-8)
        """
        digest = hashlib.sha256(public_key_hex.encode("utf-8")).hexdigest()
        return f"APQ_{digest[:40]}"

    @classmethod
    def create(
        cls,
        backend_algorithm_name: str,
        *,
        profile_name: str | None = None,
        profile_description: str | None = None,
    ) -> "PQRealWallet":
        import oqs

        signer = oqs.Signature(backend_algorithm_name)
        public_key = signer.generate_keypair()
        private_key = signer.export_secret_key()

        public_key_hex = public_key.hex()
        private_key_hex = private_key.hex()
        address = cls.derive_address(public_key_hex)

        return cls(
            algorithm_name="MLDSA_REAL_V1",
            backend_algorithm_name=backend_algorithm_name,
            private_key_hex=private_key_hex,
            public_key_hex=public_key_hex,
            address=address,
            signature_algorithm="MLDSA_REAL_V1",
            profile_name=profile_name,
            profile_description=profile_description,
            key_status="active",
            key_created_at_utc=_utc_now_z(),
            rotated_from=None,
            rotation_reason=None,
        )

    def sign_message(self, message: bytes) -> bytes:
        import oqs

        signer = oqs.Signature(self.backend_algorithm_name, bytes.fromhex(self.private_key_hex))
        return signer.sign(message)

    def verify_message(self, message: bytes, signature: bytes) -> bool:
        import oqs

        verifier = oqs.Signature(self.backend_algorithm_name)
        return verifier.verify(message, signature, bytes.fromhex(self.public_key_hex))

    def rotate(self, *, rotation_reason: str | None = None) -> "PQRealWallet":
        new_wallet = PQRealWallet.create(
            self.backend_algorithm_name,
            profile_name=self.profile_name,
            profile_description=self.profile_description,
        )
        new_wallet.rotated_from = self.address
        new_wallet.rotation_reason = rotation_reason
        new_wallet.key_status = "active"

        self.key_status = "rotated"
        self.rotation_reason = rotation_reason

        return new_wallet

    def to_dict(self, *, password: str | None = None) -> dict[str, Any]:
        data: dict[str, Any] = {
            "algorithm_name": self.algorithm_name,
            "backend_algorithm_name": self.backend_algorithm_name,
            "public_key_hex": self.public_key_hex,
            "address": self.address,
            "signature_algorithm": self.signature_algorithm,
            "profile_name": self.profile_name,
            "profile_description": self.profile_description,
            "key_status": self.key_status,
            "key_created_at_utc": self.key_created_at_utc,
            "rotated_from": self.rotated_from,
            "rotation_reason": self.rotation_reason,
        }

        data.update(
            build_private_key_payload(
                private_key_hex=self.private_key_hex,
                password=password,
            )
        )
        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        *,
        password: str | None = None,
    ) -> "PQRealWallet":
        private_key_hex = extract_private_key_hex(data, password=password)

        return cls(
            algorithm_name=data["algorithm_name"],
            backend_algorithm_name=data["backend_algorithm_name"],
            private_key_hex=private_key_hex,
            public_key_hex=data["public_key_hex"],
            address=data["address"],
            signature_algorithm=data.get("signature_algorithm", "MLDSA_REAL_V1"),
            profile_name=data.get("profile_name"),
            profile_description=data.get("profile_description"),
            key_status=data.get("key_status", "active"),
            key_created_at_utc=data.get("key_created_at_utc", _utc_now_z()),
            rotated_from=data.get("rotated_from"),
            rotation_reason=data.get("rotation_reason"),
        )

    def save_to_file(self, path: str | Path, *, password: str | None = None) -> None:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(
            json.dumps(self.to_dict(password=password), indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_from_file(
        cls,
        path: str | Path,
        *,
        password: str | None = None,
    ) -> "PQRealWallet":
        file_path = Path(path)
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return cls.from_dict(data, password=password)