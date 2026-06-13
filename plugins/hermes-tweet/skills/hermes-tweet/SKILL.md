---
name: hermes-tweet
description: Install and operate Hermes Tweet for X/Twitter workflows in Hermes Agent.
allowed-tools: Read, Grep, Glob
---

# Hermes Tweet

Use this skill when a user wants Hermes Agent to search, inspect, monitor, or
operate X/Twitter through the native Hermes Tweet plugin.

## What It Provides

Hermes Tweet adds these Hermes Agent tools:

- `tweet_explore` searches the bundled Xquik endpoint catalog without network access.
- `tweet_read` calls catalog-listed read-only endpoints when `XQUIK_API_KEY` is configured.
- `tweet_action` calls write-like or private endpoints only when action gating is enabled.

## Install

Use the native Hermes plugin installer:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

If the Hermes registry does not resolve it yet, install into the Hermes
runtime environment from PyPI:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
```

## Configure

Set the API key where the Hermes runtime executes:

```bash
export XQUIK_API_KEY="<your-xquik-api-key>"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Keep `HERMES_TWEET_ENABLE_ACTIONS=false` for read-only, scheduled, unattended,
or gateway-driven sessions. Enable it only for a session that has an explicit
approval step for account-changing operations.

## Workflow

1. Use `tweet_explore` first to find a catalog endpoint.
2. Use `tweet_read` for public read-only `GET` endpoints.
3. Use `tweet_action` only after stating the exact endpoint, method, payload,
   and reason for the operation.

Prefer read-only flows for social listening, launch monitoring, support triage,
creator research, brand research, giveaway audits, and community audits.

## Safety

- Never ask for or reveal API keys, signing keys, passwords, cookies, or TOTP secrets.
- Never pass credentials in tool arguments.
- Do not guess endpoint paths.
- Use only catalog-listed `/api/v1/...` endpoints.
- Do not use account connection, reauthentication, API key, billing, credit
  top-up, or support-ticket endpoints.
- For posting, deleting, following, DMs, profile changes, monitors, webhooks,
  extraction jobs, and draws, summarize the action before using `tweet_action`.

## Troubleshooting

- If Hermes lists the plugin as not enabled, run `hermes plugins enable hermes-tweet`.
- If `tweet_read` is missing, set `XQUIK_API_KEY` in the Hermes runtime environment.
- If `tweet_action` is missing, confirm `HERMES_TWEET_ENABLE_ACTIONS=true`.
- If Hermes Desktop uses a remote gateway profile, install and configure
  Hermes Tweet on the remote Hermes host.

## Links

- Hermes Tweet: https://github.com/Xquik-dev/hermes-tweet
- PyPI: https://pypi.org/project/hermes-tweet/
