# Demo Scope

## Public demo purpose

The purpose of this repository is to present the current public-facing signer workflow of Aegis.

## Included public scope

- desktop signer UI
- ML-DSA key generation
- optional private-key encryption with a password
- key inspection and public-key export
- file signing
- signature verification
- key rotation
- rotation-policy evaluation and enforcement
- selected public tests for the signer domain

## What the public demo intentionally shows

This demo is meant to make three things visible:

1. **NIST direction**
   - the signer domain is currently centered on **FIPS 204 / ML-DSA**

2. **Private-key protection**
   - private keys can be password-protected
   - encrypted private keys use **Argon2id + AES-256-GCM**

3. **Key lifecycle and security policy**
   - keys carry metadata such as status, creation time, and rotation information
   - the demo evaluates whether a key is still acceptable for normal signing use

## Excluded scope

- broader private application architecture
- full private API and CLI surface
- private business logic beyond the signer demo
- experimental blockchain / coin work
- internal operational material
- private release engineering

## Public positioning

This repository is a **demo repository**, not the full private product.
