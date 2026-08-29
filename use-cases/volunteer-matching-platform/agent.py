from agentkernel.pydanticai import PydanticAIToolBuilder
from pydantic_ai import Agent

# Google Gemini via the free Google AI Studio tier (GEMINI_API_KEY / GOOGLE_API_KEY env var) —
# no OpenAI key or card required. Swap the prefix for "openai:...", "anthropic:...", etc. if the
# team later wants a different provider (also swap the pydantic-ai-slim[google] extra to match).
MODEL = "google:gemini-2.5-flash"

# TODO (Phase 3b, Member 1): bind search_opportunities once its body is implemented:
#   tools=PydanticAIToolBuilder.bind([search_opportunities])
MATCHING_AGENT_INSTRUCTIONS = """
You are a placeholder matching agent for the Volunteer Matching Platform.
Real behavior (ranking opportunities with a tool and justifying matches)
lands in Phase 3b.
"""

matching_agent = Agent(
    model=MODEL,
    name="matching_agent",
    description="Ranks volunteer opportunities against a captured profile and justifies the matches.",
    instructions=MATCHING_AGENT_INSTRUCTIONS,
)


# Pydantic AI has no handoffs= primitive (unlike the OpenAI Agents SDK) — multi-agent routing is
# delegation-via-tool: profile_agent calls this tool once it has enough information, which runs
# matching_agent and returns its output as the reply.
async def hand_off_to_matching_agent(profile_summary: str) -> str:
    """Delegate to the matching agent once the user's profile (skills, availability, causes,
    location) has been captured. Pass a short summary of the captured profile."""
    return str((await matching_agent.run(profile_summary)).output)


# TODO (Phase 3a/3c, Member 1): replace with the real profile-gathering instructions from
# SPEC.md, and bind save_user_profile/load_user_profile once Phase 3c lands:
#   tools=PydanticAIToolBuilder.bind([hand_off_to_matching_agent, save_user_profile, load_user_profile])
PROFILE_AGENT_INSTRUCTIONS = """
You are a placeholder profile agent for the Volunteer Matching Platform.
Reply briefly to confirm the platform is wired up correctly. Real behavior
(collecting skills/availability/causes/location, remembering returning users,
then calling hand_off_to_matching_agent) lands in Phase 3a/3c.
"""

profile_agent = Agent(
    model=MODEL,
    name="profile_agent",
    description="Captures a user's skills, availability, causes, and location, then hands off to matching.",
    instructions=PROFILE_AGENT_INSTRUCTIONS,
    tools=PydanticAIToolBuilder.bind([hand_off_to_matching_agent]),
)

AGENTS = [profile_agent, matching_agent]
