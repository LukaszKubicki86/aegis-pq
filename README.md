# Aegis

Aegis is a post-quantum transaction and wallet prototype built around **FIPS 204 / ML-DSA** profile-aware signing flows.

It is designed as an engineering-first project that explores how **post-quantum wallet infrastructure**, **profile-based signature choices**, and **end-to-end transaction validation** can work inside a coherent CLI/API system.

## Current status

Aegis is currently in an **alpha technical showcase** stage.

What already works:

- profile-aware PQ wallets:
  - `standard` -> `ML-DSA-44`
  - `hardened` -> `ML-DSA-65`
  - `max` -> `ML-DSA-87`
- persisted classical wallets
- persisted PQ wallets
- PQ-to-classical transaction flow
- pending pool and mining flow
- profile comparison and profile cost views
- project health and backend readiness diagnostics
- end-to-end in-memory demo flow
- automated test suite

Latest validated state:

- `147 passed`
- `2 skipped`

## Why this project exists

Most existing blockchain and wallet ecosystems still rely on classical signature schemes that are not designed for a future large-scale quantum threat model.

Aegis explores a different direction:

- explicit use of **ML-DSA**
- explicit reference to **FIPS 204**
- multiple operational profiles with different size/cost/security trade-offs
- a transaction pipeline that preserves PQ signature metadata all the way through validation

This makes Aegis closer to a **post-quantum wallet / signing infrastructure prototype** than a typical toy blockchain.

## PQ profiles

Aegis currently supports three PQ profiles:

| Profile | Backend | Purpose |
|---|---|---|
| `standard` | `ML-DSA-44` | Balanced default profile for the current engineering phase |
| `hardened` | `ML-DSA-65` | Higher-security profile for later production-like testing |
| `max` | `ML-DSA-87` | Maximum-security profile with the highest size and performance cost |

You can inspect them with:

```powershell
python main.py pq-profile-compare
python main.py pq-profile-costs
```

## Quick start

### 1. Run the test suite

```powershell
python -m pytest
```

### 2. Check project and PQ backend status

```powershell
python main.py doctor
python main.py pq-real-check
```

### 3. Run the full in-memory demo

```powershell
python main.py demo-project-flow
python main.py demo-project-flow --profile hardened
python main.py demo-project-flow --profile max
```

### 4. Create PQ wallets with explicit profiles

```powershell
python main.py create-pq-real-wallet --name pq_standard_demo --profile standard
python main.py create-pq-real-wallet --name pq_hardened_demo --profile hardened
python main.py create-pq-real-wallet --name pq_max_demo --profile max
```

### 5. Inspect a PQ wallet

```powershell
python main.py show-pq-real-wallet --name pq_hardened_demo
```

## Example persisted flow

This flow uses the persisted chain and wallet files.

```powershell
python main.py init
python main.py create-wallet --name classical_receiver
python main.py create-wallet --name classical_miner
python main.py create-pq-real-wallet --name pq_sender --profile hardened
python main.py fund-pq-real-wallet --name pq_sender --amount 100
python main.py pq-real-send-live --sender pq_sender --receiver classical_receiver --amount 10 --fee 1
python main.py show-pending
python main.py pq-real-mine-live --miner classical_miner
python main.py show-chain
python main.py show-balances
```

## Main CLI commands

### Diagnostics

```powershell
python main.py doctor
python main.py pq-real-check
python main.py pq-profile-compare
python main.py pq-profile-costs
```

### Demo

```powershell
python main.py demo-project-flow
python main.py demo-project-flow --profile max
```

### Wallets

```powershell
python main.py create-wallet --name classical_user
python main.py show-wallet --name classical_user

python main.py create-pq-real-wallet --name pq_user --profile standard
python main.py show-pq-real-wallet --name pq_user
```

### Chain and balances

```powershell
python main.py init
python main.py show-chain
python main.py show-balances
python main.py show-pending
```

### Transactions and mining

```powershell
python main.py send --sender classical_miner --receiver classical_user --amount 1 --fee 0.1
python main.py mine --miner classical_miner

python main.py pq-real-send-live --sender pq_user --receiver classical_user --amount 10 --fee 1
python main.py pq-real-mine-live --miner classical_miner
```

## Architecture direction

Aegis currently follows a layered structure:

- `app/` for core application logic
- `app/services/` for service-layer orchestration
- CLI entry in `main.py`
- API layer in `app/api.py`
- persisted runtime paths managed through runtime utilities
- dedicated PQ wallet / transaction / policy modules
- tests in `tests/`

This structure is meant to keep the project extensible as it grows from prototype toward a more product-oriented toolkit.

## What Aegis is not yet

Aegis is **not** yet:

- a production blockchain
- a production wallet SDK
- a launched cryptocurrency
- a finished commercial product

It is currently best understood as:

## a profile-aware post-quantum transaction and wallet prototype

## Most realistic next product direction

The most realistic early product direction is not launching a coin first.

The strongest near-term direction is:

- **PQ wallet / signing toolkit**
- **developer-facing SDK**
- **post-quantum transaction demo platform**
- **security migration showcase for wallet infrastructure**

That direction is closer to the current codebase and much more realistic for early trust and early small revenue.

## Suggested roadmap

Short-term:

1. stabilize showcase and README quality
2. expose a cleaner public demo path
3. tighten API contract and response consistency
4. package the project more cleanly
5. define the first external-facing use case

After that:

- SDK packaging
- better docs
- public demo repo presentation
- early outreach to dev/security/crypto infrastructure audiences

## Notes

Aegis uses **ML-DSA / FIPS 204** terminology deliberately and avoids claiming impossible guarantees. The goal is to build a technically honest and demonstrable post-quantum signing and transaction prototype.

## License

Add the intended license before public release.
