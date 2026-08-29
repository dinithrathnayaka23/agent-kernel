"""Tool functions for the Volunteer Matching Platform.

Signatures below follow SPEC.md. Bodies are placeholders (Phase 3, Member 1):
- search_opportunities: Phase 3b (data & tool)
- save_user_profile / load_user_profile: Phase 3c (memory)

Not yet bound to any agent's tools list (see agent.py) — implement the bodies
here first, then bind via OpenAIToolBuilder.bind([...]) in agent.py.
"""

from __future__ import annotations


def search_opportunities(
    skills: list[str],
    causes: list[str] | None = None,
    location: str | None = None,
    remote_ok: bool = True,
) -> list[dict]:
    """Rank volunteer opportunities from data/opportunities.json against the given profile."""
    raise NotImplementedError("search_opportunities: implement in Phase 3b (Member 1)")


def save_user_profile(
    user_id: str,
    skills: list[str],
    availability: str,
    causes: list[str],
    location: str,
) -> str:
    """Persist a user's profile to the knowledge store, keyed by user_id."""
    raise NotImplementedError("save_user_profile: implement in Phase 3c (Member 1)")


def load_user_profile(user_id: str) -> dict | None:
    """Load a previously saved profile for user_id, or None if this is a new user."""
    raise NotImplementedError("load_user_profile: implement in Phase 3c (Member 1)")
