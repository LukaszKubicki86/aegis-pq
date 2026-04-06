# architecture.md

# Aegis Architecture

## Overview

Aegis is a Python prototype for **profile-aware post-quantum wallet and transaction flows** built around **FIPS 204 / ML-DSA**.

The current implementation combines:

- a small blockchain core
- classical and post-quantum wallet support
- a CLI entrypoint
- a FastAPI layer
- a service layer for orchestration
- runtime helpers for persisted state
- profile-aware PQ policies
- automated tests

At the current stage, Aegis is best understood as:

## an alpha engineering prototype and technical showcase

It is not yet a production blockchain or packaged SDK, but the architecture is already structured enough to support those later directions.

---

## High-level structure

Main project areas:

- `main.py` -> CLI entrypoint
- `app/` -> core application modules
- `app/services/` -> service-layer orchestration
- `app/api.py` -> API layer
- `tests/` -> automated test suite
- `data/` -> persisted runtime state for wallets and chain

---

## Layered architecture

Aegis currently follows a practical layered structure.

### 1. Domain/core layer

Core domain modules live in `app/` and define the behavior of:

- wallets
- transactions
- blocks
- blockchain state
- signers
- PQ adapters and policies

Important modules:

- `app/block.py`
- `app/blockchain.py`
- `app/state.py`
- `app/transaction.py`
- `app/wallet.py`
- `app/signers.py`

This layer is responsible for the actual transaction and chain logic.

### 2. PQ-specific layer

Post-quantum behavior is isolated into dedicated modules.

Important modules:

- `app/pq_policy.py`
- `app/pq_adapter.py`
- `app/pq_backend_stub.py`
- `app/pq_real_wallet.py`
- `app/pq_real_transaction.py`
- `app/pq_real_experiment.py`
- `app/pq_lab.py`

This layer handles:

- PQ profile definitions
- mapping between profiles and backends
- PQ wallet creation
- PQ transaction signing and bridging
- backend readiness checks
- real-vs-stub adapter behavior

### 3. Service layer

The service layer organizes use cases and keeps CLI/API code thinner.

Modules:

- `app/services/wallet_service.py`
- `app/services/transaction_service.py`
- `app/services/chain_service.py`
- `app/services/live_flow_service.py`
- `app/services/pq_demo_service.py`
- `app/services/demo_project_flow_service.py`

This layer handles:

- wallet creation and wallet views
- funding and transaction orchestration
- balances and chain views
- persisted PQ live flow
- demo and showcase flows
- profile comparison and cost reporting

### 4. Runtime layer

Runtime helpers live in:

- `app/runtime.py`

This module centralizes:

- chain path
- wallet paths
- PQ wallet paths
- loading and saving chain state
- live send validation helpers
- presence checks for required files

### 5. Interface layer

Interfaces currently include:

- CLI in `main.py`
- FastAPI in `app/api.py`

This makes it possible to expose the same internal logic through:
- command line usage
- HTTP endpoints

---

## Core transaction model

Aegis currently supports two main transaction paths:

### Classical path
Built around:
- `Wallet`
- `Transaction`
- classical signing (`EC_SECP256K1`)

### PQ path
Built around:
- `PQRealWallet`
- `PQRealTransaction`
- profile-selected ML-DSA backend
- bridge into normal `Transaction`

This is important:

## PQ transactions are not isolated from the rest of the system

A PQ transaction can be signed in the PQ layer, then bridged into the general transaction pipeline and validated by the same blockchain flow.

That is one of the most important architectural properties of the project.

---

## Signature handling

Signature handling is centered around:

- `app/signers.py`
- `app/wallet.py`
- `app/pq_adapter.py`

### Key idea
Aegis separates:
- the generic transaction pipeline
- the signature backend details

This allows the system to:
- preserve `signature_algorithm`
- preserve `signature_backend_algorithm_name`
- validate transactions correctly across profiles

That is what makes these profile-aware flows possible for:

- `ML-DSA-44`
- `ML-DSA-65`
- `ML-DSA-87`

---

## PQ policy model

Profile definitions live in:

- `app/pq_policy.py`

Current defaults:

- signature standard: `FIPS 204`
- signature family: `ML-DSA`
- default experiment algorithm: `MLDSA_REAL_V1`
- default backend: `ML-DSA-44`

Current profiles:

- `standard`
- `hardened`
- `max`

Each profile contains:
- a name
- a backend algorithm
- an experiment algorithm
- a description

This is the policy layer that drives:
- wallet creation
- profile comparison
- cost view
- demo flows

---

## Persisted vs in-memory flows

Aegis supports two important operating modes.

### 1. In-memory showcase flow
Implemented through:

- `app/services/demo_project_flow_service.py`
- CLI command: `demo-project-flow`

Purpose:
- safe end-to-end demo
- no mutation of real runtime files
- repeatable showcase output

This is the best path for:
- demonstrations
- screenshots
- public showcase

### 2. Persisted runtime flow
Implemented through:

- `app/runtime.py`
- `app/services/live_flow_service.py`

Purpose:
- use real `data/chain.json`
- use persisted wallets
- inspect pending pool, balances, and chain state over time

This is the best path for:
- manual integration-style testing
- CLI usage with saved state
- more realistic project flows

---

## Wallet model

Aegis currently supports:

### Classical wallets
Stored in:
- `data/wallets/`

### PQ wallets
Stored in:
- `data/pq_real_wallets/`

PQ wallets persist:
- algorithm name
- backend algorithm name
- public/private key material
- address
- `profile_name`
- `profile_description`

This is important because profile metadata is now part of the wallet identity and user-facing model.

---

## CLI command groups

The CLI in `main.py` currently exposes several functional groups.

### Diagnostics
- `doctor`
- `pq-lab`
- `pq-real-check`
- `pq-profile-compare`
- `pq-profile-costs`

### Demo
- `pq-real-wallet-demo`
- `pq-real-tx-demo`
- `pq-real-mine-demo`
- `demo-project-flow`

### Wallet management
- `create-wallet`
- `show-wallet`
- `fund`
- `create-pq-real-wallet`
- `show-pq-real-wallet`
- `fund-pq-real-wallet`

### Chain and state
- `init`
- `show-chain`
- `show-balances`
- `show-pending`

### Transaction and mining flows
- `send`
- `mine`
- `pq-real-send`
- `pq-real-send-live`
- `pq-real-mine-live`

This is one of the reasons the project is already useful as a technical showcase: it has a real command surface.

---

## API layer

The API layer is implemented in:

- `app/api.py`

Its purpose is not yet to be a polished public SaaS API. At the current stage it acts as:

- a second interface to the same internal logic
- proof that the architecture is not CLI-only
- a step toward future toolkit / SDK / service packaging

This is a good sign for future product direction, even though the current project is still alpha.

---

## Test structure

The test suite lives in:

- `tests/`

Current validated project state:
- `147 passed`
- `2 skipped`

Test coverage includes:
- blockchain behavior
- runtime helpers
- API support
- wallet services
- chain services
- transaction services
- PQ adapter/backend behavior
- PQ wallet and transaction behavior
- demo flow service
- profile comparison and cost reporting

This gives Aegis a strong engineering signal for its current stage.

---

## Current architectural strengths

### 1. Separation of responsibilities
The project has a clear separation between:
- domain objects
- services
- runtime helpers
- interfaces

### 2. PQ policy is explicit
Profiles are modeled directly instead of being hidden in ad hoc flags.

### 3. PQ metadata survives the transaction pipeline
This is a real architectural milestone, especially across multiple ML-DSA backend profiles.

### 4. Demo and persisted flows both exist
That gives the project both:
- showcase value
- realistic stateful testing value

### 5. Test-backed changes
The project has already gone through repeated refactoring while preserving a green test suite.

---

## Current architectural limits

The project is not yet:

- production packaged
- release-versioned
- deployment-oriented
- security-reviewed for production use
- designed as a finished external SDK

There is also still a gap between:
- internal engineering structure
- external product packaging

That is normal for the current stage.

---

## Best current interpretation of the architecture

Aegis is currently strongest as:

## a profile-aware post-quantum wallet and transaction prototype architecture

It is already suitable for:
- technical demonstration
- architecture showcase
- controlled alpha packaging
- future toolkit direction

It is not yet best used as:
- production chain infrastructure
- public mass-market wallet software
- launch-ready cryptocurrency platform

---

## Most realistic next architectural step

The most useful next step is not adding random new features.

The next strong step is:

## packaging and documentation around the current architecture

That means:
- stronger repo presentation
- documentation that explains the current layers
- clearer public/private separation
- later, cleaner packaging for a selective alpha toolkit
