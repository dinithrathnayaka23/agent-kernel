from agents import Agent

# from agentkernel.openai import OpenAIToolBuilder
# from tool import load_user_profile, save_user_profile, search_opportunities

# TODO (Phase 3a, Member 1): replace with the real profile-gathering instructions
# from SPEC.md, and bind save_user_profile/load_user_profile once Phase 3c lands:
#   tools=OpenAIToolBuilder.bind([save_user_profile, load_user_profile])
PROFILE_AGENT_INSTRUCTIONS = """
You are a placeholder profile agent for the Volunteer Matching Platform.
Reply briefly to confirm the platform is wired up correctly. Real behavior
(collecting skills/availability/causes/location, remembering returning users)
lands in Phase 3a/3c.
"""

# TODO (Phase 3b, Member 1): bind search_opportunities once its body is implemented:
#   tools=OpenAIToolBuilder.bind([search_opportunities])
MATCHING_AGENT_INSTRUCTIONS = """
You are a placeholder matching agent for the Volunteer Matching Platform.
Real behavior (ranking opportunities with a tool and justifying matches)
lands in Phase 3b.
"""

matching_agent = Agent(
    name="matching_agent",
    handoff_description="Ranks volunteer opportunities against a captured profile and justifies the matches.",
    instructions=MATCHING_AGENT_INSTRUCTIONS,
)

profile_agent = Agent(
    name="profile_agent",
    handoff_description="Captures a user's skills, availability, causes, and location, then hands off to matching.",
    instructions=PROFILE_AGENT_INSTRUCTIONS,
    handoffs=[matching_agent],
)

AGENTS = [profile_agent, matching_agent]
