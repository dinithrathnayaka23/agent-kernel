# Volunteer Matching Platform

A multi-agent Agent Kernel solution for SDG 17 (Partnerships for the Goals) that matches volunteers to opportunities based on their skills, availability, and causes.

## Problem Statement

Volunteers struggle to find opportunities that actually fit their skills, availability, and causes they care about. Existing volunteer listing sites are search-and-browse; nothing has a conversation with you, remembers what you told it, and comes back with a short, justified shortlist instead of a wall of listings to sift through yourself.

## Solution Overview

Two Agent Kernel agents, built with **Pydantic AI** on **Google Gemini** (free tier — no API cost to run):

- **`profile_agent`** — the entry point. Recognizes returning users (via a knowledge store) and asks only for what's missing; for new users, conversationally collects skills, availability, causes of interest, and location/remote preference.
- **`matching_agent`** — once a profile is captured, ranks opportunities from a 36-entry dataset using a deterministic scoring tool (`search_opportunities`) and explains *why* each match fits, or says plainly when nothing fits well rather than forcing a weak match.

**Memory**: profiles are saved to a `ChromaManager` knowledge store, keyed by a stable identity per channel, so a returning user is recognized in a later, separate conversation instead of starting over every time.

**Interfaces**: a web chat UI (`static/index.html`) and a **Telegram bot** are both fully working — a real conversation over Telegram correctly captured a profile, handed off to matching, and returned ranked results. Slack is implemented too, but live delivery was never confirmed despite a thorough investigation; see [Known Limitations](#known-limitations).

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
   set AK_TELEGRAM__BOT_TOKEN=placeholder
   ```
   The Slack and Telegram values only need to be *non-empty* to let `app.py` start — both integrations validate that at construction time regardless of whether they're actually being used. Real setup for either is optional; see below.

## How to Run

- **CLI (local testing, no Slack/Telegram needed):** `uv run python demo.py`
- **REST API (backs the web frontend, Slack, and Telegram):** `uv run python app.py` — listens on `http://localhost:8000`. Requires all four env vars above to start.
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

## Telegram Setup (confirmed working)

`app.py` serves `AgentTelegramRequestHandler` alongside the web API — same agents, tools, and memory store. Unlike Slack, there's no OAuth, no app reinstalls, no scopes to configure — just a bot token and a webhook URL.

1. Open Telegram, message [@BotFather](https://t.me/botfather), send `/newbot`, follow the prompts. Copy the token it gives you.
2. Set `AK_TELEGRAM__BOT_TOKEN` to that real token (replacing the placeholder), restart `app.py`.
3. Tunnel port 8000 publicly — e.g. with ngrok, which offers a free stable domain that doesn't change on restart (recommended over Pinggy, whose URL changes every restart):
   ```
   ngrok http --domain=your-claimed-domain.ngrok-free.app 8000
   ```
4. **Register the webhook manually** — despite what `agentkernel`'s own Telegram integration README says ("automatically set when your server starts"), the installed code does not actually do this; you must call Telegram's API yourself, every time the public URL changes:
   ```
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-domain.ngrok-free.app/telegram/webhook"
   ```
   A `{"ok":true,"result":true,...}` response confirms it registered.
5. Message your bot directly in Telegram.

## Slack Setup (optional, not confirmed working — see Known Limitations)

The code is fully wired the same way as Telegram. If you want to try it:

1. Create a Slack app at https://api.slack.com/apps ("Blank app").
2. Under **OAuth & Permissions**, add bot token scopes: `chat:write`, `im:write`, `files:read`, `app_mentions:read`. Install to your workspace, copy the **Bot User OAuth Token** → `SLACK_BOT_TOKEN`.
3. Under **Basic Information**, copy the **Signing Secret** → `SLACK_SIGNING_SECRET`.
4. Under **App Home**, enable the **Messages Tab** (off by default — Slack blocks DMs to an app otherwise).
5. Start `app.py`, then tunnel port 8000 (ngrok recommended over Pinggy — see Telegram section above for why).
6. Under **Event Subscriptions**, set the Request URL to `https://<tunnel>/slack/events`, confirm it verifies, subscribe to `message.im`/`message.channels`/`app_mention`, and click **Save Changes**.
7. DM the bot directly (not a private channel — that needs the separate `message.groups` event/scope).
8. If it still doesn't deliver real messages despite the URL verifying: that's the known, documented, unresolved issue — see Known Limitations.

## Known Limitations

- **Slack was not confirmed working live**, despite a thorough attempt: the code is correct and independently verified (route live, correctly rejects unsigned requests), OAuth scopes and event subscriptions were confirmed correctly configured and reinstalled in the Slack admin UI, the App Home messages tab was enabled, and the public tunnel was confirmed genuinely reachable from the outside — tested with two different providers (Pinggy, then ngrok with a stable domain) to rule out a tunnel-specific issue. The result was a consistent, telling asymmetry: Slack's one-time URL-verification handshake reached the server correctly every single time, but a real message event never did, across both tunnels and a fully reinstalled app. That pattern points to something on Slack's account/workspace side outside what the app-configuration screens expose, not a missed setup step. This does not block the submission — **Telegram is confirmed working** and the web frontend is independently sufficient on its own regardless.
- **Memory identity is per-channel.** The web frontend, Slack, and Telegram each track identity independently (a persisted browser id, the real Slack user id, or the Telegram chat id) — the same person across channels isn't recognized as one account. See `SPEC.md`'s Memory/Knowledge section for why.
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
- [x] Phase 3g — Telegram — **confirmed fully working with a real bot and a real conversation**: `Selected agent: profile_agent` → profile captured in one message → `Delegating to matching_agent with profile_summary='Skills: coding, teaching. Availability: weekends. Causes: education. Location: Colombo.'` → a full ranked-match reply, all over real Telegram servers
- [x] Phase 3f — test harness
- [x] Phase 5 — fresh-clone acceptance test: cloned the branch into a throwaway directory, followed only this README from scratch — `build.sh`, `pytest` (8 passed, 1 correctly skipped without a key), and `app.py` all worked exactly as documented, including a real conversation reaching Gemini
- [x] Phase 6a — `AGENTS.md` added
- [ ] Phase 6b — demo video, final submission
