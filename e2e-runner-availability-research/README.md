# E2E runner availability research

This smoke test checks whether a public repository can run a GitHub-hosted workflow and read repository-level self-hosted runner availability from multiple repositories through the GitHub REST API.

## Goal

- Run the monitor job on a GitHub-hosted runner
- Query repository-level self-hosted runner status for `aicers-test/test-public` and `petabi-test/test-public`
- Keep credentials in GitHub Actions secrets
- Print only sanitized runner fields

## Required secrets

- `AICERS_TEST_RUNNER_READ_TOKEN`
- `PETABI_TEST_RUNNER_READ_TOKEN`

Each token should be a fine-grained personal access token for the matching organization with access to the matching test repository and `Administration: Read-only` repository permission.

## Smoke workflow

The workflow is manual-only for the initial validation:

```text
.github/workflows/e2e-runner-availability-smoke.yml
```

If the manual smoke test passes, a 10-minute `schedule` trigger can be added later for cron validation.
