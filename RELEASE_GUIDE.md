# Release Guide

## Recommended public publishing model

### GitHub repository

Use the repository for:

- source code
- README
- screenshots
- public documentation

### GitHub Releases

Use GitHub Releases for:

- `Aegis-Signer-Demo-Windows.zip`
- later optionally `Aegis-Signer-Demo-Setup.exe`

## Recommended first release tag

- `v0.1.0-demo`

## Recommended publishing notes

Public messaging should make these points clear:

- this is a **public demo repository**
- the current visible cryptographic direction is **FIPS 204 / ML-DSA**
- the demo includes **password-based private-key encryption**
- the demo includes **rotation and lifecycle policy**
- the repository does **not** represent the full private product

## Pre-release checklist

- run the public test subset in a clean virtual environment
- verify the desktop UI starts correctly
- verify signer demo flow works
- verify no private keys or local artifacts are included
- verify screenshots match the current UI
- verify README language matches the actual public scope
