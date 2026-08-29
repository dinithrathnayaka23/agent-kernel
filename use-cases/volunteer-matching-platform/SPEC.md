# Volunteer Matching Platform Specification

## Agent Description

A multi-agent solution that connects individuals with suitable volunteer opportunities (SDG 17 — Partnerships for the Goals). A `profile_agent` captures the user's skills, availability, causes of interest, and location preference, then hands off to a `matching_agent`, which retrieves and ranks relevant opportunities from a provided dataset using a tool, returning the result with a brief justification per match. A knowledge store retains user preferences so returning users are recognized in later, separate conversations.

## Functional Requirements

### Agents

- Build two Agent Kernel agents using **Pydantic AI**, pointed at **Google Gemini** (`google:gemini-2.5-flash`, free tier via Google AI Studio — `GOOGLE_API_KEY` or `GEMINI_API_KEY` env var, no card required): `profile_agent` (entry point) and `matching_agent`.
- `profile_agent`:
  - On the first message of a conversation, calls `load_user_profile` to check whether this user has a stored profile.
  - If a profile exists, greets the user by referencing what's already known and asks only for anything missing or that they want to change, instead of re-asking everything.
  - If no profile exists, conversationally collects: skills (list), availability (days/hours or a free-text description), causes of interest (e.g. environment, education, health — ideally SDG-aligned), and a location or remote preference.
  - Once the required fields are gathered, calls `save_user_profile`, then calls `hand_off_to_matching_agent` with a summary of the captured profile.
- `matching_agent`:
  - Calls `search_opportunities` with the current profile's skills, causes, location, and remote preference.
  - Returns the top 3–5 ranked matches, each with a one-line justification tying the match to a specific skill or cause overlap.
  - If no opportunities score above a minimum relevance threshold, says so plainly rather than forcing weak matches.
- **Pydantic AI has no `handoffs=` primitive** (unlike the OpenAI Agents SDK) — multi-agent routing is delegation-via-tool: `profile_agent` is given a plain async tool function, `hand_off_to_matching_agent(profile_summary)`, that runs `matching_agent.run(...)` internally and returns its output. Register both agents via `PydanticAIModule([profile_agent, matching_agent])`.

### Tool

- Implement `search_opportunities(skills: list[str], causes: list[str] | None, location: str | None, remote_ok: bool) -> list[dict]` in `tool.py`.
- Reads opportunities from `data/opportunities.json` (see Dataset below).
- Deterministic scoring (not LLM-based): weight skill overlap count highest, then cause/SDG tag match, then location/remote match.
- Returns the top N (default 5) results sorted by score descending; each result includes a `justification` string generated from which fields matched (e.g. "Matches your skills in graphic design and your interest in education").
- Must be unit-testable in isolation from any agent or LLM call.

### Dataset

- `data/opportunities.json`: a list of 30–40 objects, each with:
  - `id` (string), `organization` (string, fictional/generic — not a real org's name or branding), `title` (string), `description` (string), `required_skills` (list of strings), `cause_tags` (list of strings, SDG-aligned where possible), `location` (string), `remote` (boolean), `time_commitment` (string, e.g. "2 hrs/week").
- Cover a spread of causes/skills/locations broad enough that the matching tool's ranking is visibly meaningful across different user profiles, not just returning the same top results regardless of input.

### Memory / Knowledge

- Implement `save_user_profile(user_id: str, skills: list[str], availability: str, causes: list[str], location: str) -> str` and `load_user_profile(user_id: str) -> dict | None` in `tool.py`, backed by an Agent Kernel `KnowledgeBase` (`agentkernel.knowledgebase`) rather than plain session cache.
- Keyed explicitly by a stable `user_id` passed into the tool call — not by the Agent Kernel session ID — so a profile persists across separate conversations/sessions for the same user.
  - Web frontend: `user_id` is a UUID generated client-side on first visit and persisted in `localStorage`.
  - Slack: `user_id` is the Slack user ID from the incoming event; verify during implementation exactly how `AgentSlackRequestHandler` exposes this to a tool call before wiring it.
- Known, accepted limitation: identity is per-channel. The same person using both the web UI and Slack has two independent profiles — there is no cross-channel account linking in this version.

### User Interfaces

- **Web frontend (primary):** a static HTML/JS chat page that calls Agent Kernel's REST chat endpoint (`POST /api/v1/chat`), sending the browser-generated `user_id` with every request, and rendering the conversation as a chat thread. Enable CORS on the REST API if the frontend is served from a different origin than the API.
- **Slack (secondary):** wire `AgentSlackRequestHandler` alongside the web API so both interfaces are served from the same `RESTAPI.run([...])` call, front the same two agents, and share the same knowledge store.

## Local Development

- Provide a local CLI entry point (`demo.py`) for testing the agents without needing the web frontend or Slack running.
- Use `uv` for dependency management.
- Keep generated dependency exports, deployment packages, local virtual environments, and installed coding-agent skills out of Git.
- Required environment variable: `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) — get a free key with no card required at https://aistudio.google.com/apikey.
- `app.py` constructs `AgentSlackRequestHandler` unconditionally alongside the web API handler, so `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` must also be set (even to placeholder values) for `app.py` to start at all — `slack_bolt` validates the signing secret is non-empty at construction time. `demo.py` (CLI) needs none of the Slack variables. Real end-to-end Slack testing additionally needs a tunnel (e.g. pinggy.io) for the local webhook URL — see README.md.

## Deployment

- Optional / stretch goal — not required for a working submission.
- If pursued, follow the deployment folder structure used by the Agent Kernel AWS serverless examples (a single `lambda.py` entry point, packaging commands in `deploy/deploy.sh`), and keep the underlying agent and tool logic shared between local and deployed execution.
