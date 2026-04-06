# Aegis Showcase

## Overview

Aegis is a Python-based prototype for post-quantum wallet and transaction flows built around **FIPS 204 / ML-DSA** digital signatures.

At its current stage, Aegis is not positioned as a production blockchain or a public coin. It is a **technical showcase and engineering prototype** focused on one concrete problem:

> how to build, test, compare, and demonstrate profile-aware post-quantum transaction flows using real ML-DSA backends.

The project already supports:

- real post-quantum signature experiments through `liboqs-python`
- profile-aware PQ wallets (`standard`, `hardened`, `max`)
- profile comparison and cost views
- PQ-to-classical transaction bridging
- in-memory end-to-end demo flows
- persisted chain flows with mining and balance updates
- CLI and API coverage
- a growing automated test suite

---

## Why this project exists

Most existing crypto systems and wallets were designed around classical signatures.
Aegis explores a different direction:

- **post-quantum signatures first**
- explicit security profiles
- traceable engineering behavior
- clear demonstrations of trade-offs between cost and security level

The goal is to build something that is technically honest, testable, and explainable.

---

## Current technical status

Aegis is currently in an:

## Alpha technical showcase / engineering prototype stage

This means:

- the core transaction pipeline works
- profile-aware PQ wallets work
- all three ML-DSA profile mappings work end-to-end
- the project can be demonstrated live through CLI flows
- the codebase is structured and test-backed

This does **not** mean:

- production readiness
- public network readiness
- token launch readiness
- audited security guarantees
- SDK packaging completion

---

## Supported PQ profiles

Aegis exposes three profile presets:

| Profile | Backend | Purpose |
|---|---:|---|
| `standard` | `ML-DSA-44` | Balanced default profile for the current engineering phase |
| `hardened` | `ML-DSA-65` | Higher-security profile for later production-like testing |
| `max` | `ML-DSA-87` | Maximum-security profile with the highest size and performance cost |

These profiles are visible in:

- wallet creation
- wallet metadata
- profile comparison view
- profile cost view
- end-to-end demo flow

---

## What already works

### 1. PQ readiness and inspection

Commands:

```powershell
python main.py doctor
python main.py pq-real-check
python main.py pq-profile-compare
python main.py pq-profile-costs
```

What this gives:

- runtime environment check
- FIPS 204 / ML-DSA visibility
- backend readiness check
- profile comparison
- cost trade-off visibility

### 2. Profile-aware PQ wallet creation

Commands:

```powershell
python main.py create-pq-real-wallet --name pq_standard --profile standard
python main.py create-pq-real-wallet --name pq_hardened --profile hardened
python main.py create-pq-real-wallet --name pq_max --profile max
```

Wallet metadata includes:

- algorithm name
- backend algorithm
- profile name
- profile description
- key sizes

### 3. PQ wallet inspection

```powershell
python main.py show-pq-real-wallet --name pq_hardened
```

### 4. In-memory full demo flow

```powershell
python main.py demo-project-flow
python main.py demo-project-flow --profile hardened
python main.py demo-project-flow --profile max
```

This runs an isolated showcase flow that demonstrates:

- PQ wallet creation
- classical receiver and miner creation
- funding
- PQ signing
- transaction bridging
- mining
- final balances
- valid chain result

### 5. Persisted PQ-to-classical chain flow

Example:

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

This proves that a profile-aware PQ wallet can:

- sign a real transaction
- send to a classical address
- enter pending state
- be mined into a persisted chain
- update balances correctly

---

## Test status

Current project test result:

- **147 passed**
- **2 skipped**

This includes tests for:

- runtime
- wallets
- blockchain behavior
- API behavior
- PQ adapter/backend behavior
- PQ transaction flow
- profile comparison and cost reporting
- end-to-end demo service

---

## What Aegis is today

Aegis today is best described as:

## a post-quantum transaction and wallet showcase platform

It is already strong enough to be shown as:

- a technical prototype
- a post-quantum signing showcase
- a developer-facing experiment platform
- an early SDK/tooling foundation

It is **not** yet best described as:

- a finished startup product
- a mainnet-ready chain
- a ready public coin
- a production wallet ecosystem

---

## Most realistic first product direction

The most realistic first commercialization path is **not** a coin.

The strongest first direction is:

## PQ wallet / signing / transaction toolkit

Potential forms:

- Python SDK for PQ transaction flows
- developer tooling for profile-aware ML-DSA signing
- wallet infrastructure demo package
- migration showcase for post-quantum transaction stacks

Why this path makes sense first:

- it matches the current codebase
- it is easier to demonstrate honestly
- it requires less market trust than launching a coin
- it can produce early symbolic revenue faster than a token/network play

---

## What still needs to be done before production thinking

Before any serious production discussion, Aegis still needs:

### Engineering

- packaging and versioning
- release process
- stricter API contracts
- export/import and compatibility rules
- stronger persistence guarantees
- better operational error handling

### Security

- structured security review
- threat model document
- key handling review
- safer secret storage strategy
- production assumptions review

### Product

- a sharp product definition
- a public-facing README
- example use cases
- sample integration stories
- clearer target user definition

---

## Practical roadmap

### Phase 1 — foundation

Status: **done**

- architecture cleanup
- test coverage base
- CLI stability
- real PQ backend connection
- PQ profile system
- demo and comparison tooling

### Phase 2 — showcase

Status: **current phase**

- polished README
- polished demo flow
- clearer output formatting
- public-facing examples
- stronger presentation layer

### Phase 3 — first product shape

Suggested next direction:

- package Aegis as a usable toolkit / SDK
- define supported flows and public interfaces
- publish example integrations
- prepare first public alpha release

### Phase 4 — commercialization experiments

Possible early experiments:

- paid implementation support
- custom PQ demo builds
- developer consulting around PQ wallet flows
- premium examples / integration packages

---

## Suggested next milestone

The best immediate next milestone is:

## README + public showcase quality

This is the point where the project starts becoming easy to present.

A strong public showcase should include:

- what Aegis is
- what problem it targets
- why ML-DSA / FIPS 204 matters here
- supported profiles
- example demo output
- current maturity level
- roadmap

---

## Honest production answer

When can this go to production?

### Honest answer:
Not yet.

But it is now close to something much more valuable than a vague idea:

## a technically credible alpha showcase

That is the right stage to aim for first.

---

## How to show the project when it is ready enough

The best way to present Aegis is:

### 1. Strong repository presentation

A repository that explains:

- the problem
- the architecture
- the demo
- the profiles
- the current maturity level

### 2. One-command demo

Aegis already has this direction:

```powershell
python main.py demo-project-flow --profile hardened
```

### 3. Clean screenshots / terminal captures

Useful showcase outputs:

- `python main.py doctor`
- `python main.py pq-profile-costs`
- `python main.py demo-project-flow --profile hardened`
- `python main.py demo-project-flow --profile max`

### 4. Technical framing, not hype

A better introduction is:

> Built a working FIPS 204 / ML-DSA prototype with profile-aware wallet creation, transaction validation, and end-to-end demo flows.

This is much stronger than overselling a coin too early.

---

## Summary

Aegis is now in a strong prototype state.

It already demonstrates:

- real ML-DSA-backed flows
- profile-aware wallet creation
- transaction validation across profiles
- end-to-end demo behavior
- meaningful technical structure

The next best step is not another deep core refactor.

## The next best step is presentation quality.

That means:

- better showcase docs
- clearer product framing
- SDK/tooling direction
- first public alpha positioning

