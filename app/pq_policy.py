from __future__ import annotations

from dataclasses import dataclass


DEFAULT_REAL_EXPERIMENT_ALGORITHM = "MLDSA_REAL_V1"
DEFAULT_PQ_BACKEND_ALGORITHM = "ML-DSA-44"
DEFAULT_PQ_PROFILE_NAME = "standard"

PQ_SIGNATURE_STANDARD_NAME = "FIPS 204"
PQ_SIGNATURE_FAMILY_NAME = "ML-DSA"
PQ_SIGNATURE_STANDARD_DESCRIPTION = (
    "NIST post-quantum digital signature standard based on ML-DSA."
)


@dataclass(frozen=True)
class PQProfile:
    name: str
    backend_algorithm: str
    experiment_algorithm: str
    description: str


PQ_STANDARD_PROFILE = PQProfile(
    name="standard",
    backend_algorithm="ML-DSA-44",
    experiment_algorithm="MLDSA_REAL_V1",
    description="Balanced default profile for the current engineering phase.",
)

PQ_HARDENED_PROFILE = PQProfile(
    name="hardened",
    backend_algorithm="ML-DSA-65",
    experiment_algorithm="MLDSA_REAL_V1",
    description="Higher-security profile for later production-like testing.",
)

PQ_MAX_PROFILE = PQProfile(
    name="max",
    backend_algorithm="ML-DSA-87",
    experiment_algorithm="MLDSA_REAL_V1",
    description="Maximum-security profile with the highest size and performance cost.",
)


PQ_PROFILES: dict[str, PQProfile] = {
    PQ_STANDARD_PROFILE.name: PQ_STANDARD_PROFILE,
    PQ_HARDENED_PROFILE.name: PQ_HARDENED_PROFILE,
    PQ_MAX_PROFILE.name: PQ_MAX_PROFILE,
}


def get_pq_profile(name: str) -> PQProfile:
    normalized = name.strip().lower()
    if normalized not in PQ_PROFILES:
        raise ValueError(
            f"Unknown PQ profile '{name}'. Available profiles: {', '.join(sorted(PQ_PROFILES))}."
        )
    return PQ_PROFILES[normalized]


def get_default_profile() -> PQProfile:
    return PQ_PROFILES[DEFAULT_PQ_PROFILE_NAME]


def get_default_backend_algorithm() -> str:
    return get_default_profile().backend_algorithm


def get_default_experiment_algorithm() -> str:
    return get_default_profile().experiment_algorithm


def get_pq_signature_standard_name() -> str:
    return PQ_SIGNATURE_STANDARD_NAME


def get_pq_signature_family_name() -> str:
    return PQ_SIGNATURE_FAMILY_NAME


def get_pq_signature_standard_description() -> str:
    return PQ_SIGNATURE_STANDARD_DESCRIPTION