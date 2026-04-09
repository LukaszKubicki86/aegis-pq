# Security Notice

## Public-demo position

This repository is a **public demo**. It is not presented as a certified production product.

Its purpose is to show the design direction and the current signer workflow in a technically honest way.

## Security behaviors shown in the demo

The public demo is designed to show several important ideas clearly:

- post-quantum signatures based on **ML-DSA**
- optional **password-based private-key encryption**
- key metadata and lifecycle state
- rotation-policy evaluation
- enforcement of security rules around key use

## Private-key protection

When password protection is enabled, the private key is not stored in plaintext.

The current implementation uses:

- **Argon2id** as the password-based key derivation function
- **AES-256-GCM** as the authenticated encryption method

The encrypted payload stores the required metadata needed to decrypt the key later, including:

- KDF name: `argon2id`
- salt
- derived key length
- iteration count
- lane count
- memory cost
- cipher name: `aes-256-gcm`
- cipher nonce
- encrypted ciphertext

### Current encryption parameters in the demo implementation

- Argon2id salt: **16 bytes**
- derived key length: **32 bytes**
- iterations: **3**
- lanes: **4**
- memory cost: **65536**
- AES-GCM nonce: **12 bytes**

These details are included because this public demo intentionally shows how private-key protection is handled, rather than hiding it behind vague claims.

## Plaintext mode

The demo also allows plaintext private-key storage when no password is provided.

That is acceptable for controlled demo flows, local testing, and educational inspection of the file format. It should not be treated as the preferred security posture when password protection is desired.

## Rotation policy

The demo shows that keys are not treated as permanently valid by default.

Keys carry lifecycle metadata such as:

- `key_status`
- `key_created_at_utc`
- `rotated_from`
- `rotation_reason`

The current public demo rotation policy uses these profile windows:

- `standard` → **365 days**
- `hardened` → **365 days**
- `max` → **548 days**

A `due_soon` threshold of **30 days** is used.

The policy model distinguishes states such as:

- `ok`
- `due_soon`
- `overdue`
- `rotated`
- `revoked`
- `unknown`

Only `ok` and `due_soon` are considered acceptable for normal signing use.

## Repository hygiene

Before publishing:

- do not include private keys
- do not include local user data
- do not include temporary files or caches
- do not include internal-only materials
- do not include local test artifacts or generated signatures unless they are intentionally safe demo samples

## Public positioning

This demo is intended to communicate:

- that the project follows a **NIST-aligned post-quantum direction**
- that private-key protection is handled deliberately
- that key lifecycle and rotation are part of the design
- that the repository is a **public showcase**, not the full private product
