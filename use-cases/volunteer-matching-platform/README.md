# Volunteer Matching Platform

> Scaffold stage — this README is filled in properly during Phase 6. See `SPEC.md` for the full design.

## Problem Statement

Volunteers struggle to find opportunities that actually fit their skills, availability, and causes they care about (SDG 17 — Partnerships for the Goals). This project matches people to relevant volunteer opportunities automatically.

## Solution Overview

A multi-agent Agent Kernel solution: a `profile_agent` captures a user's skills, availability, and causes; a `matching_agent` ranks opportunities from a dataset via a tool and returns justified matches. Preferences are remembered across sessions via a knowledge store. Usable through a web chat UI and Slack. See `SPEC.md` for full details.

## Setup Instructions

1. Install [uv](https://github.com/astral-sh/uv).
2. From this directory, run `./build.sh` (creates `.venv`, installs dependencies).
3. Set the required environment variable: `export OPENAI_API_KEY=sk-...`
4. *(Slack only)* Set `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` — see `SPEC.md`.

## How to Run

- **CLI (local testing):** `uv run python demo.py`
- **REST API (backs the web frontend, and Slack once wired):** `uv run python app.py`

## Status

- [x] Phase 1 — `SPEC.md`
- [x] Phase 2 — scaffold (this stage)
- [ ] Phase 3 — agents, tool, memory (Member 1) / web frontend, Slack, tests (Member 2)
- [ ] Phase 4–6 — integration, testing, docs, demo video, submission
