# Adapter Roadmap

The runtime contracts are prepared before provider integrations.

## Ready foundation

- Task, run and attempt persistence.
- Append-only event history.
- Persisted worker summaries, changed-file lists and claims.
- Persisted structured reviews with task/run/attempt/reviewer linkage.
- Deny-by-default tool policy.
- Worker and reviewer protocols.
- Mock worker/reviewer end-to-end loop.
- API, CLI, Docker and CI.

## Next implementation order

1. Git workspace/worktree adapter with path, repository and ownership checks.
2. Controlled deterministic tool adapters (Git inspection, pytest, Ruff and existing project checks).
3. Artifact/evidence manifest for full raw test and tool outputs when those outputs are introduced.
4. FCC worker adapter.
5. Codex reviewer adapter with schema validation and reviewer independence.
6. Review-loop policy with a configured maximum of three regular correction rounds.
7. Dashboard on top of the existing API.
8. Hermes orchestration adapter only after core runtime behavior is stable.
9. Local Qwen worker only after benchmarking and resource measurements.

No adapter may silently broaden privileges. Critical tasks remain human-gated. A separate container is added only when an actual isolation boundary requires one.
