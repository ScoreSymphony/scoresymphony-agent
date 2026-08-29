# Configuration

Only non-secret reference configuration belongs here.

Runtime precedence for the bootstrap is intentionally simple:

1. safe application defaults;
2. documented environment variables;
3. deployment-specific secret injection outside Git.

Supported runtime variables currently include `SCORESYMPHONY_ENV`, `SCORESYMPHONY_STATE_DIR`, `SCORESYMPHONY_HOST`, and `SCORESYMPHONY_PORT`.

Do not commit provider tokens, GitHub credentials, database passwords, private keys or production secrets. Provider/model configuration will be added only with the corresponding adapter.
