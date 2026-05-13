#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request


TARGETS = [
    ("aicers-test", "AICERS_TEST_RUNNER_READ_TOKEN"),
    ("petabi-test", "PETABI_TEST_RUNNER_READ_TOKEN"),
]


def request_json(url, token):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "e2e-runner-availability-smoke",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def parse_http_error(err):
    try:
        payload = json.loads(err.read().decode("utf-8"))
    except Exception:
        return f"HTTP {err.code}"

    message = payload.get("message", "no message")
    documentation_url = payload.get("documentation_url", "no documentation_url")
    return f"HTTP {err.code}: {message} ({documentation_url})"


def sanitize_runner(runner):
    return {
        "id": runner.get("id"),
        "name": runner.get("name"),
        "status": runner.get("status"),
        "busy": runner.get("busy"),
        "os": runner.get("os"),
        "labels": sorted(
            label.get("name")
            for label in runner.get("labels", [])
            if isinstance(label, dict) and label.get("name")
        ),
    }


def main():
    failures = []

    for org, token_env in TARGETS:
        token = os.environ.get(token_env)
        if not token:
            failures.append(f"{org}: missing {token_env}")
            continue

        url = f"https://api.github.com/orgs/{org}/actions/runners"
        try:
            status, payload = request_json(url, token)
        except urllib.error.HTTPError as err:
            failures.append(f"{org}: GitHub API returned {parse_http_error(err)}")
            continue
        except Exception as err:
            failures.append(f"{org}: request failed: {err.__class__.__name__}")
            continue

        runners = payload.get("runners", [])
        print(f"org={org} http_status={status} total_count={payload.get('total_count')}")
        print(json.dumps([sanitize_runner(runner) for runner in runners], indent=2, sort_keys=True))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
