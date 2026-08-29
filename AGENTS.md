# AGENTS.md

## Scope

This repository owns the standalone ScoreSymphony agent application. It must not duplicate the ScoreSymphony music-analysis/product implementation or VPS host administration.

## Rules

- Inspect existing code and tests before changing behavior.
- Preserve working structures unless a change is justified.
- Keep changes small, explicit, and testable.
- Prefer deterministic tools over LLM calls when a task can be solved deterministically.
- Never commit secrets, tokens, credentials, private keys, or production data.
- Do not add new infrastructure, databases, queues, or agent frameworks without a concrete requirement.
- Do not give workers unrestricted host, Docker socket, sudo, main-merge, or production-database access.
- Keep worker and reviewer roles logically independent.
- Treat generated files and templates as non-deployed until verified.
- Add or update tests for behavior changes.
- Fail closed when required configuration or evidence is missing.

## Initial architecture

The first version is intentionally a single Python application and a single Docker image. Internal modules may later be split into separate processes or containers only when isolation, scaling, or operational evidence requires it.
