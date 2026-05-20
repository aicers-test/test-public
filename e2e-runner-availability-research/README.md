# E2E runner availability research

This smoke test checks whether a public repository can run a GitHub-hosted workflow and read organization-level self-hosted runner availability from multiple organizations through the GitHub REST API.

## Goal

- Run the monitor job on a GitHub-hosted runner
- Query organization-level self-hosted runner status for `aicers-test` and `petabi-test`
- Keep credentials in GitHub Actions secrets
- Print only sanitized runner fields

## Required secrets

- `AICERS_TEST_RUNNER_READ_TOKEN`
- `PETABI_TEST_RUNNER_READ_TOKEN`

Each token should be a fine-grained personal access token for the matching organization with `Self-hosted runners: Read-only` organization permission.

## Smoke workflow

The workflow is manual-only for the initial validation:

```text
.github/workflows/e2e-runner-availability-smoke.yml
```

If the manual smoke test passes, a 10-minute `schedule` trigger can be added later for cron validation.
