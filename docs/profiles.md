# profiles.md

# Aegis PQ Profiles

## Overview

Aegis currently uses a **profile-aware post-quantum model** built around:

- **FIPS 204**
- **ML-DSA**
- explicit backend selection
- explicit trade-offs between cost and security level

Instead of exposing only one PQ mode, Aegis currently defines three operational profiles:

- `standard`
- `hardened`
- `max`

These profiles shape how PQ wallets and PQ transaction flows are created and demonstrated.

---

## Why profiles exist

Profiles exist because post-quantum signatures are not just a binary question of:

- quantum-safe
- not quantum-safe

In practice, different ML-DSA parameter sets introduce different trade-offs in:

- public key size
- private key size
- signature size
- performance cost
- operational overhead

Aegis makes those trade-offs visible and testable.

That is one of the core ideas of the project.

---

## Standards context

The current PQ profile system is built around:

- signature standard: `FIPS 204`
- signature family: `ML-DSA`

Aegis uses that terminology explicitly in:
- `doctor`
- `pq-real-check`
- profile comparison
- profile cost reporting
- demo flow output
- wallet creation flows

---

## Current profile definitions

Profile definitions live in:

- `app/pq_policy.py`

Each profile contains:
- `name`
- `backend_algorithm`
- `experiment_algorithm`
- `description`

The current experiment algorithm is:

- `MLDSA_REAL_V1`

The current profiles all map to that experiment layer but use different backend parameter sets.

---

## Profile: standard

### Backend
- `ML-DSA-44`

### Description
Balanced default profile for the current engineering phase.

### Role in the project
This is the default PQ profile and the most practical one for:
- default demos
- default checks
- first-line showcase output
- current engineering baseline

### Typical commands
```powershell
python main.py create-pq-real-wallet --name pq_standard_demo --profile standard
python main.py demo-project-flow --profile standard
```

### Observed size characteristics
From current project output:

- public key size: `1312`
- private key size: `2560`
- signature size: `2420`

### Best interpretation
This is the **balanced baseline profile**.

---

## Profile: hardened

### Backend
- `ML-DSA-65`

### Description
Higher-security profile for later production-like testing.

### Role in the project
This profile exists to represent a stronger operational posture than the default baseline while staying below the highest-cost profile.

It is useful for:
- stronger technical demonstrations
- profile-aware testing
- showing that Aegis supports more than one PQ backend
- more serious-looking security posture in demos

### Typical commands
```powershell
python main.py create-pq-real-wallet --name pq_hardened_demo --profile hardened
python main.py demo-project-flow --profile hardened
```

### Observed size characteristics
From current project output:

- public key size: `1952`
- private key size: `4032`
- signature size: `3309`

### Best interpretation
This is the **stronger profile with higher operational cost**.

---

## Profile: max

### Backend
- `ML-DSA-87`

### Description
Maximum-security profile with the highest size and performance cost.

### Role in the project
This profile exists to show the upper end of the current profile model.

It is useful for:
- demonstrating that Aegis handles the highest-cost ML-DSA profile
- making size/security trade-offs very visible
- proving that the transaction pipeline preserves backend metadata across validation

### Typical commands
```powershell
python main.py create-pq-real-wallet --name pq_max_demo --profile max
python main.py demo-project-flow --profile max
```

### Observed size characteristics
From current project output:

- public key size: `2592`
- private key size: `4896`
- signature size: `4627`

### Best interpretation
This is the **maximum-security, maximum-cost showcase profile**.

---

## Side-by-side profile summary

| Profile | Backend | Public key size | Private key size | Signature size | Interpretation |
|---|---|---:|---:|---:|---|
| `standard` | `ML-DSA-44` | 1312 | 2560 | 2420 | Balanced baseline |
| `hardened` | `ML-DSA-65` | 1952 | 4032 | 3309 | Stronger, higher cost |
| `max` | `ML-DSA-87` | 2592 | 4896 | 4627 | Highest cost and strongest profile in current model |

---

## Where profiles are used in the project

Profiles are not just labels in Aegis.
They are propagated through real project behavior.

### 1. Wallet creation
Profiles are used when creating PQ wallets:

```powershell
python main.py create-pq-real-wallet --name pq_user --profile hardened
```

The wallet stores:
- `profile_name`
- `profile_description`
- backend algorithm name

### 2. Wallet inspection
Profiles are visible when reading wallet metadata:

```powershell
python main.py show-pq-real-wallet --name pq_user
```

### 3. Profile comparison view
Profiles can be listed side-by-side:

```powershell
python main.py pq-profile-compare
```

### 4. Profile cost view
Profiles can be compared by observed sizes:

```powershell
python main.py pq-profile-costs
```

### 5. Demo flow
Profiles drive the in-memory end-to-end showcase:

```powershell
python main.py demo-project-flow --profile standard
python main.py demo-project-flow --profile hardened
python main.py demo-project-flow --profile max
```

### 6. Persisted live flow
Profiles also work in persisted PQ-to-classical transaction flows:
- wallet creation with profile
- PQ funding
- live send
- mining
- balance update

This is a key strength of the current implementation.

---

## Why profile metadata matters

Aegis does not stop at choosing a backend during wallet creation.

The project now preserves profile-related information through:
- wallet metadata
- transaction metadata
- backend-aware validation
- demo and diagnostics output

This matters because it makes the system:

- more transparent
- easier to inspect
- more product-like
- less dependent on hidden assumptions

---

## What the profile system proves today

The current profile system proves that Aegis can:

- expose multiple ML-DSA parameter sets
- create wallets with explicit profile selection
- preserve profile choice in wallet metadata
- preserve backend metadata through transaction validation
- demonstrate all three profiles end-to-end

That is a real engineering result, not just a naming layer.

---

## What the profile system does not prove yet

The current profile system does **not** yet mean:

- full production readiness
- audited security guarantees
- large-scale performance characterization
- deployment-grade SDK packaging
- external ecosystem adoption

At the current stage, profiles should be understood as:

## technically working, demonstrable configuration tiers inside an alpha PQ prototype

---

## Best way to use profiles right now

### Use `standard` for:
- default demos
- first screenshots
- general showcase

### Use `hardened` for:
- stronger technical demonstrations
- more serious PQ narrative
- profile-aware persisted flow testing

### Use `max` for:
- showing the upper bound of the current model
- making security/cost trade-offs visible
- demonstrating full pipeline compatibility with the heaviest profile

---

## Most realistic product interpretation

In the current stage, the profile model makes Aegis especially credible as:

- a PQ wallet/signing toolkit prototype
- a profile-aware transaction showcase
- a developer-facing demo platform
- an early infrastructure exploration project

This is much more realistic than treating the profile system as proof that Aegis should immediately become a public coin.

---

## Practical commands

### Compare profile definitions
```powershell
python main.py pq-profile-compare
```

### Compare profile costs
```powershell
python main.py pq-profile-costs
```

### Create wallets for all profiles
```powershell
python main.py create-pq-real-wallet --name pq_standard_demo --profile standard
python main.py create-pq-real-wallet --name pq_hardened_demo --profile hardened
python main.py create-pq-real-wallet --name pq_max_demo --profile max
```

### Inspect saved wallets
```powershell
python main.py show-pq-real-wallet --name pq_standard_demo
python main.py show-pq-real-wallet --name pq_hardened_demo
python main.py show-pq-real-wallet --name pq_max_demo
```

### Run end-to-end demo flow for each profile
```powershell
python main.py demo-project-flow --profile standard
python main.py demo-project-flow --profile hardened
python main.py demo-project-flow --profile max
```

---

## Summary

The Aegis profile model is one of the most important parts of the project.

It makes the project:
- more explicit
- more testable
- more demonstrable
- more product-oriented

At the current stage, profiles are already a real technical feature and a real showcase feature.
