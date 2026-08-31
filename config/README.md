# Configuration

Configuration priority is intended to be:

1. safe built-in defaults
2. versioned non-secret configuration
3. environment/host overrides
4. protected secrets
5. explicit runtime overrides where policy allows

Current environment variables:

- `SCORESYMPHONY_ENV`
- `SCORESYMPHONY_STATE_ROOT`
- `SCORESYMPHONY_FRONTEND_DIR`
- `SCORESYMPHONY_AUTH_MODE`

Do not add real credentials to this directory.
