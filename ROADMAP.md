# ROADMAP.md

# Aegis Roadmap

## Current stage

Aegis is currently in:

## Alpha technical showcase

What this means:

- the core transaction pipeline works
- PQ profiles work
- end-to-end demo flow works
- persisted chain flow works
- the project is technically demonstrable
- the project is not yet production-ready

Validated current state:

- automated tests: `147 passed, 2 skipped`
- `demo-project-flow` works for:
  - `standard` / `ML-DSA-44`
  - `hardened` / `ML-DSA-65`
  - `max` / `ML-DSA-87`

---

## Phase 1 — Core foundation
### Status: done enough for this stage

Completed:

- project structure and service layer
- CLI and API base
- PQ real wallet support
- PQ real transaction support
- profile-aware wallet creation
- profile comparison and profile cost views
- doctor and backend readiness checks
- end-to-end demo flow
- persisted chain integration
- profile metadata stored in wallet files

Goal of this phase:
- prove the architecture
- prove the PQ flow
- prove profile-aware validation across the pipeline

---

## Phase 2 — Showcase and product framing
### Status: current active phase

Objectives:

- improve repository presentation
- improve public-facing documentation
- make demo flows easier to understand
- define product positioning clearly
- separate showcase from core private implementation

Deliverables:

- polished `README.md`
- showcase documentation
- roadmap
- product positioning notes
- public/private repo strategy
- stable demo command set
- screenshot-ready command outputs

Success criteria:

- a technical person can understand the project quickly
- a non-technical interested person can understand the value proposition
- the project can be shown without exposing the full internal codebase

---

## Phase 3 — Alpha toolkit packaging
### Status: next major target

Objectives:

- package Aegis as an early PQ toolkit
- make the codebase easier to distribute privately
- make demos and integrations repeatable

Candidate deliverables:

- installable package structure
- versioning strategy
- cleaner configuration handling
- exportable demo reports
- cleaner API contract
- alpha release notes
- integration examples

Success criteria:

- the project can be delivered to a selected early user or partner
- demos are repeatable
- setup friction is reduced
- the private codebase is easier to maintain and share selectively

---

## Phase 4 — Private alpha with selected users
### Status: future

Objectives:

- test whether anyone actually wants this
- validate first demand
- validate which use case is strongest

Possible early user groups:

- security-focused developers
- crypto infrastructure developers
- research-oriented builders
- teams interested in PQ wallet experiments
- small integration or advisory clients

What to validate:

- are people more interested in wallet profiles or transaction infrastructure?
- do they want SDK access, demo access, or consulting help?
- what is the clearest and most valuable first offer?

Success criteria:

- first credible user conversations
- first small paid engagement
- first repeated question or repeated need

---

## Phase 5 — First monetizable offer
### Status: future

Most realistic first offer:

## Aegis PQ Toolkit Alpha

Potential form:

- private alpha access
- PQ wallet and transaction demo toolkit
- profile-aware signing flow package
- integration support
- technical walkthrough sessions
- custom prototype support

What this is not yet:

- not a full production wallet platform
- not a production blockchain
- not a token launch
- not a public mass-market product

Success criteria:

- first small symbolic revenue
- clear first use case
- one offer that people understand quickly

---

## Phase 6 — Product decision point
### Status: later

At this stage, decide which path is strongest:

### Path A — SDK / infrastructure toolkit
Best if:
- developers care about integration
- the strongest response is technical
- the project is used as infrastructure

### Path B — private applied product
Best if:
- clients want workflow support more than code
- the strongest response is operational or integration-based

### Path C — coin or chain direction
Best if:
- there is real market pull
- there is a strong ecosystem reason
- trust, legal, product, and distribution questions are answered

Current recommendation:
## do not prioritize coin first

---

## Production readiness checklist
### Not complete yet

Before speaking seriously about production, Aegis should have:

- stable packaging
- release/version policy
- stronger API stability
- clearer data migration strategy
- basic security review
- explicit threat model
- better docs
- test coverage maintained while features expand
- operational deployment guidance

---

## Immediate next steps

### Next step 1
Create a public/private strategy and first-offer plan.

### Next step 2
Prepare public-facing materials without exposing the full core code.

### Next step 3
Define the first monetizable alpha offer.

### Next step 4
Package the project more cleanly for selective sharing.

---

## Summary

Aegis is already beyond a raw proof of concept.

It is currently best described as:

## a profile-aware post-quantum wallet and transaction engineering prototype

The best near-term strategy is to:
- strengthen presentation
- keep the core private
- shape the project into a selective alpha toolkit
- use that to reach first small revenue before thinking about a coin
