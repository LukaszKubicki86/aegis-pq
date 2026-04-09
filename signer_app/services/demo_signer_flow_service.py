from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from signer_app.models import FileSignResult, FileVerifyResult, GenerateKeyResult
from signer_app.services.file_sign_service import sign_file_with_private_key
from signer_app.services.file_verify_service import verify_file_signature
from signer_app.services.key_service import generate_pq_keypair


@dataclass
class DemoSignerFlowResult:
    key_result: GenerateKeyResult
    sign_result: FileSignResult
    verify_before_result: FileVerifyResult
    verify_after_result: FileVerifyResult
    original_file_path: str
    signature_path: str
    modified_file_path: str
    profile_name: str
    backend_algorithm_name: str


def run_demo_signer_flow(
    work_dir: str | Path,
    profile_name: str = "hardened",
    key_name: str = "demo_user",
    file_name: str = "demo.txt",
    original_content: str = "hello aegis signer",
    modified_content: str = "hello aegis signer modified",
    password: str | None = None,
) -> DemoSignerFlowResult:
    base_dir = Path(work_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    key_result = generate_pq_keypair(
        output_dir=base_dir,
        name=key_name,
        profile_name=profile_name,
        password=password,
    )

    input_file = base_dir / file_name
    input_file.write_text(original_content, encoding="utf-8")

    sign_result = sign_file_with_private_key(
        file_path=input_file,
        private_key_path=key_result.private_key_path,
        password=password,
    )

    verify_before_result = verify_file_signature(
        file_path=input_file,
        signature_path=sign_result.signature_path,
    )

    input_file.write_text(modified_content, encoding="utf-8")

    verify_after_result = verify_file_signature(
        file_path=input_file,
        signature_path=sign_result.signature_path,
    )

    return DemoSignerFlowResult(
        key_result=key_result,
        sign_result=sign_result,
        verify_before_result=verify_before_result,
        verify_after_result=verify_after_result,
        original_file_path=str(input_file),
        signature_path=sign_result.signature_path,
        modified_file_path=str(input_file),
        profile_name=key_result.profile_name,
        backend_algorithm_name=key_result.backend_algorithm_name,
    )