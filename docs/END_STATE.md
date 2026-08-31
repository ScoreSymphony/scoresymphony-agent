# End-State Decision

This repository is prepared for the complete Agent Platform instead of a disposable backend-only bootstrap.

## Fixed product surfaces

The primary Develop Control UI contains:

1. Overview
2. Proposals
3. Specifications
4. Tasks
5. Runs
6. Reviews
7. Approvals
8. System (read-mostly)

Later views may deepen these surfaces but must not create a parallel truth.

## Fixed application boundaries

- `api/`: HTTP command/query boundary
- `domain/`: canonical runtime objects and state contracts
- `state/`: persistence adapters, never duplicated semantics
- `services/`: application/use-case layer
- `adapters/`: workers, review, system telemetry and external capabilities
- `frontend/`: Human Control Plane UI
- `tests/`: deterministic contracts

## Fixed deployment shape for KVM-4

The first production shape is intentionally one application container plus persistent volumes. This is not a monolith-by-accident: internal boundaries are explicit so a later worker or persistence service can move out-of-process without rewriting the UI/API/domain model.

## Planned integrations

- Hermes orchestration
- FCC implementation path
- independent Codex review path
- local/GPU Qwen worker
- deterministic test runner
- worktree lifecycle
- research runner
- code-intelligence layer
- read-only resource/health telemetry

No integration is promoted merely because its directory exists.
