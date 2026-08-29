# Frontend

Reserved for the ScoreSymphony Agent dashboard.

The dashboard is intentionally not implemented in the bootstrap. It will consume the existing `/v1` API rather than duplicate runtime logic. Initial views should cover tasks, runs, attempts, reviews, events and health/status. Security-sensitive actions remain controlled by backend policy and are never implemented as frontend-only gates.
