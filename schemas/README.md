# Schemas

Machine-readable contracts for persisted and externally exchanged agent data.

Current schemas:

- `task.schema.json` — task identity, lifecycle, risk, scope and acceptance criteria.
- `review-result.schema.json` — structured reviewer result with task/run/attempt/reviewer linkage and findings.

Python semantic validation remains fail-closed where JSON Schema alone cannot express runtime invariants. Additional schemas should be introduced with the data they actually govern, not pre-created speculatively.
