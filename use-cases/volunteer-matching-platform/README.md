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
4. *(Slack only)* Set `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` — see `SPEC.md`.

## How to Run

- **CLI (local testing):** `uv run python demo.py`
- **REST API (backs the web frontend, and Slack once wired):** `uv run python app.py` — listens on `http://localhost:8000`.
- **Web frontend:** with `app.py` running in one terminal, serve `static/` in another:
  ```bash
  cd static && python -m http.server 5500
  ```
  Then open `http://localhost:5500` in a browser. The page talks to the API at `http://localhost:8000` (edit the `API_BASE` constant at the top of `static/index.html`'s `<script>` if you change the API port).

## Status

- [x] Phase 1 — `SPEC.md`
- [x] Phase 2 — scaffold
- [x] Phase 3d — web frontend (this stage)
- [ ] Phase 3a–3c — agents, tool, memory (Member 1)
- [ ] Phase 3e–3f — Slack, tests/docs (Member 2)
- [ ] Phase 4–6 — integration, testing, docs, demo video, submission
