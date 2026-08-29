from agentkernel.api import RESTAPI
from agentkernel.pydanticai import PydanticAIModule

from agent import AGENTS

# TODO (Phase 3e, Member 2): add `from agentkernel.slack import AgentSlackRequestHandler`
# and pass RESTAPI.run([AgentSlackRequestHandler()]) to serve Slack alongside the web API.

PydanticAIModule(AGENTS)


if __name__ == "__main__":
    RESTAPI.run()
