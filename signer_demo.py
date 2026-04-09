from __future__ import annotations

from pathlib import Path

from signer_app.services.demo_signer_flow_service import run_demo_signer_flow


def main() -> None:
    work_dir = Path("data/signer_demo")
    result = run_demo_signer_flow(
        work_dir=work_dir,
        profile_name="hardened",
    )

    print("=== Aegis Signer Demo ===")
    print(f"Profile:               {result.profile_name}")
    print(f"Backend:               {result.backend_algorithm_name}")
    print(f"Public key path:       {result.key_result.public_key_path}")
    print(f"Private key path:      {result.key_result.private_key_path}")
    print(f"Public fingerprint:    {result.key_result.public_key_fingerprint}")
    print(f"Original file:         {result.original_file_path}")
    print(f"Signature path:        {result.signature_path}")
    print(f"Verify before change:  {result.verify_before_result.is_valid}")
    print(f"Before message:        {result.verify_before_result.message}")
    print(f"Verify after change:   {result.verify_after_result.is_valid}")
    print(f"After message:         {result.verify_after_result.message}")


if __name__ == "__main__":
    main()