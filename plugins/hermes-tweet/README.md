# Hermes Tweet

Guidance for installing and operating the native Hermes Agent plugin for
X/Twitter automation through Xquik.

## Install This Marketplace Plugin

```bash
/plugin install hermes-tweet@abc-claude-plugin-marketplace
```

## Install Hermes Tweet

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

If the Hermes registry does not resolve it yet, install from PyPI into the
Hermes runtime environment:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
```

## Configuration

Set the API key where Hermes Agent executes:

```bash
export XQUIK_API_KEY="<your-xquik-api-key>"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Keep actions disabled for read-only, scheduled, unattended, or gateway-driven
workflows. Enable `HERMES_TWEET_ENABLE_ACTIONS=true` only for sessions with an
explicit approval step for account-changing operations.

## Usage

Invoke the skill:

```bash
/hermes-tweet explore X search endpoints
```

Recommended tool order in Hermes Agent:

1. `tweet_explore` to find a catalog endpoint.
2. `tweet_read` for public read-only `GET` endpoints.
3. `tweet_action` only after the endpoint, method, payload, and reason are clear.

Use Hermes Tweet for social listening, launch monitoring, support triage,
creator research, brand research, giveaway audits, community audits, and
controlled publishing workflows.

## Links

- Hermes Tweet: https://github.com/Xquik-dev/hermes-tweet
- PyPI: https://pypi.org/project/hermes-tweet/
