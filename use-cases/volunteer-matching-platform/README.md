# Volunteer Matching Platform

> Scaffold stage — this README is filled in properly during Phase 6. See `SPEC.md` for the full design.

## Problem Statement

Volunteers struggle to find opportunities that actually fit their skills, availability, and causes they care about (SDG 17 — Partnerships for the Goals). This project matches people to relevant volunteer opportunities automatically.

## Solution Overview

A multi-agent Agent Kernel solution (built with Pydantic AI on Google Gemini's free tier): a `profile_agent` captures a user's skills, availability, and causes; a `matching_agent` ranks opportunities from a dataset via a tool and returns justified matches. Preferences are remembered across sessions via a knowledge store. Usable through a web chat UI and Slack. See `SPEC.md` for full details.

## Setup Instructions

1. Install [uv](https://github.com/astral-sh/uv).
2. From this directory, run `./build.sh` (creates `.venv`, installs dependencies).
3. Get a free API key (no card required) at https://aistudio.google.com/apikey, then: `export GOOGLE_API_KEY=...`
4. `app.py` now wires Slack alongside the web API, so it **requires** `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` to start at all — even if you only want to test the web frontend. Until you've done real Slack app setup (see below), set placeholders so it boots:
   ```bash
   export SLACK_BOT_TOKEN=xoxb-placeholder
   export SLACK_SIGNING_SECRET=placeholder-secret
   ```
   Swap in real values once you've created a Slack app (next section) — the web frontend and CLI don't care which values are set, only that they're non-empty.

## Slack Setup

1. Create a Slack app at https://api.slack.com/apps (from scratch, pick any workspace — create a free one if needed).
2. Under **OAuth & Permissions**, add these bot token scopes: `chat:write`, `im:write`, `files:read`, `app_mentions:read`. Install the app to your workspace, then copy the **Bot User OAuth Token** (`xoxb-...`) → `SLACK_BOT_TOKEN`.
3. Under **Basic Information**, copy the **Signing Secret** → `SLACK_SIGNING_SECRET`.
4. Start `app.py` (below), then tunnel port 8000 publicly — e.g. with [pinggy.io](https://pinggy.io): `ssh -p 443 -R0:localhost:8000 a.pinggy.io`.
5. Back in the Slack app config, under **Event Subscriptions**, enable events and set the Request URL to `https://<your-tunnel-domain>/slack/events`. Slack sends a verification challenge here — `AgentSlackRequestHandler` answers it automatically, no extra code needed. Subscribe to `message.im`, `message.channels`, and `app_mention`.
6. Invite the bot to a channel (or DM it directly) and send a message.

## How to Run

- **CLI (local testing, no Slack needed):** `uv run python demo.py`
- **REST API + Slack (backs the web frontend, and Slack once tunneled):** `uv run python app.py` — listens on `http://localhost:8000`. Requires all three env vars above (`GOOGLE_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`) to start.
- **Web frontend:** with `app.py` running in one terminal, serve `static/` in another:
  ```bash
  cd static && python -m http.server 5500
  ```
  Then open `http://localhost:5500` in a browser. The page talks to the API at `http://localhost:8000` (edit the `API_BASE` constant at the top of `static/index.html`'s `<script>` if you change the API port).

## Status

- [x] Phase 1 — `SPEC.md`
- [x] Phase 2 — scaffold
- [x] Phase 3d — web frontend
- [x] Phase 3e — Slack (this stage) — code wired and verified (`/slack/events` live, correctly rejects unsigned requests); real workspace/tunnel setup is on you, see above
- [ ] Phase 3a–3c — agents, tool, memory (Member 1)
- [ ] Phase 3f — tests/docs (Member 2)
- [ ] Phase 4–6 — integration, testing, docs, demo video, submission
