# Adapter Roadmap

The runtime contracts are prepared before provider integrations.

1. Deterministic/mock end-to-end loop.
2. Git workspace/worktree adapter with path and ownership checks.
3. Controlled test/tool adapters (Git, pytest, Ruff, type checking when present).
4. FCC worker adapter.
5. Codex reviewer adapter with schema validation and reviewer independence.
6. API/UI task control.
7. Hermes orchestration adapter only after core runtime behavior is stable.
8. Local Qwen worker only after benchmarking and resource measurements.

No adapter may silently broaden privileges. Critical tasks remain human-gated.
