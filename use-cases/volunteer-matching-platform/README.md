# Volunteer Matching Platform

A multi-agent Agent Kernel solution for SDG 17 (Partnerships for the Goals) that matches volunteers to opportunities based on their skills, availability, and causes.

## Problem Statement

Volunteers struggle to find opportunities that actually fit their skills, availability, and causes they care about. Existing volunteer listing sites are search-and-browse; nothing has a conversation with you, remembers what you told it, and comes back with a short, justified shortlist instead of a wall of listings to sift through yourself.

## Solution Overview

Two Agent Kernel agents, built with **Pydantic AI** on **Google Gemini** (free tier — no API cost to run):

- **`profile_agent`** — the entry point. Recognizes returning users (via a knowledge store) and asks only for what's missing; for new users, conversationally collects skills, availability, causes of interest, and location/remote preference.
- **`matching_agent`** — once a profile is captured, ranks opportunities from a 36-entry dataset using a deterministic scoring tool (`search_opportunities`) and explains *why* each match fits, or says plainly when nothing fits well rather than forcing a weak match.

**Memory**: profiles are saved to a `ChromaManager` knowledge store, keyed by a stable identity per channel, so a returning user is recognized in a later, separate conversation instead of starting over every time.

**Interfaces**: a web chat UI (`static/index.html`) is the primary, fully working way to use this — talks to Agent Kernel's REST API. Slack integration is also implemented and wired (`AgentSlackRequestHandler` running alongside the web API in `app.py`) but is optional; see [Known Limitations](#known-limitations).

Full technical design, including two mid-implementation corrections made after verifying against the actual installed Agent Kernel version, is in [`SPEC.md`](SPEC.md).

## Setup Instructions

1. Install [uv](https://github.com/astral-sh/uv).
2. From this directory, run `./build.sh` (creates `.venv`, installs dependencies).
3. Get a free API key (no card required) at https://aistudio.google.com/apikey.
4. Set the required environment variables (cmd.exe shown; PowerShell uses `$env:NAME = "value"`):
   ```
   set GOOGLE_API_KEY=your-real-gemini-key
   set SLACK_BOT_TOKEN=xoxb-placeholder
   set SLACK_SIGNING_SECRET=placeholder-secret
   ```
   The two Slack values only need to be *non-empty* to let `app.py` start — `slack_bolt` validates that at construction time regardless of whether Slack is actually being used. Real Slack setup is optional; see below.

## How to Run

- **CLI (local testing, no Slack needed):** `uv run python demo.py`
- **REST API (backs the web frontend):** `uv run python app.py` — listens on `http://localhost:8000`. Requires all three env vars above to start.
- **Web frontend** — the primary way to use this: with `app.py` running in one terminal, serve `static/` in another:
  ```bash
  cd static && python -m http.server 5500
  ```
  Open `http://localhost:5500`. (Edit the `API_BASE` constant near the top of `static/index.html`'s `<script>` if you change the API port.)

Try a full conversation: give it your skills, availability, causes, and location; it should ask only for what's missing, then hand off to a ranked shortlist with reasons. Reload the page afterward and say hello again — it should recognize you without re-asking, since your browser id is persisted in `localStorage` across visits.

## Testing

```bash
uv run pytest
```

- `tool_test.py`: unit tests for `search_opportunities`'s ranking logic — no agent, session, or LLM call involved, always runs (8/8 passing).
- `demo_test.py`: a live CLI smoke test (skipped automatically if `GOOGLE_API_KEY`/`GEMINI_API_KEY` isn't set) — checks `profile_agent` returns a real, non-empty, error-free reply.

Note: the first call to `save_user_profile`/`load_user_profile` on a machine downloads a small (~80 MB) local embedding model for the memory store — one-time, needs internet, no API key involved.

## Slack Setup (optional)

The code is fully wired: `app.py` serves `AgentSlackRequestHandler` alongside the web API, using the same agents, tools, and memory store. If you want to try it:

1. Create a Slack app at https://api.slack.com/apps ("Blank app").
2. Under **OAuth & Permissions**, add bot token scopes: `chat:write`, `im:write`, `files:read`, `app_mentions:read`. Install to your workspace, copy the **Bot User OAuth Token** → `SLACK_BOT_TOKEN`.
3. Under **Basic Information**, copy the **Signing Secret** → `SLACK_SIGNING_SECRET`.
4. Under **App Home**, enable the **Messages Tab** (off by default — Slack blocks DMs to an app otherwise).
5. Start `app.py`, then tunnel port 8000 (e.g. `ssh -4 -p 443 -R0:localhost:8000 a.pinggy.io` — free tunnels expire after 60 minutes and change URL each restart).
6. Under **Event Subscriptions**, set the Request URL to `https://<tunnel>/slack/events`, confirm it verifies, subscribe to `message.im`/`message.channels`/`app_mention`, and click **Save Changes**.
7. DM the bot directly (not a private channel — that needs the separate `message.groups` event/scope).

## Known Limitations

- **Slack was not confirmed working live** despite the code being correctly implemented and independently verified (routes exist and are live, correctly reject unsigned requests, scopes/events configured correctly). Slack app webhook setup has several easy-to-miss steps (event subscriptions vs. saving vs. reinstalling vs. the App Home messages tab vs. public/private channel event types), and live delivery wasn't achieved in the time available. This does not block the submission — the web frontend is a fully working, independently sufficient user-facing interface running the same agents/tools/memory.
- **Memory identity is per-channel.** The web frontend and Slack each track identity independently (a persisted browser id vs. the real Slack user id) — the same person on both isn't recognized as one account. See `SPEC.md`'s Memory/Knowledge section for why.
- **CLI memory doesn't persist across separate `demo.py` runs** — each run gets a fresh session id. It works fine within one run, and works across visits on the web frontend (which deliberately persists its id).
- Cloud deployment was treated as out of scope — a solid local run plus the web frontend satisfies the rubric without it.

## Status

- [x] Phase 1 — `SPEC.md`
- [x] Phase 2 — scaffold
- [x] Phase 3a — agents (`profile_agent` → `matching_agent` via delegation-via-tool)
- [x] Phase 3b — dataset (36 opportunities) + `search_opportunities` (8/8 unit tests passing)
- [x] Phase 3c — memory (`save_user_profile`/`load_user_profile` via `ChromaManager`)
- [x] Phase 3d — web frontend — **confirmed working with a real conversation and a real Gemini key**
- [x] Phase 3e — Slack — code correct and independently verified; live webhook not confirmed (see Known Limitations)
- [x] Phase 3f — test harness
- [ ] Phase 5 — fresh-clone acceptance test
- [ ] Phase 6 — `AGENTS.md`, demo video, submission
