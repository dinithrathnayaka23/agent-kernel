from agentkernel.api import RESTAPI, AgentRESTRequestHandler
from agentkernel.pydanticai import PydanticAIModule
from agentkernel.slack import AgentSlackRequestHandler

from agent import AGENTS

PydanticAIModule(AGENTS)


if __name__ == "__main__":
    # Explicit handler list serves both interfaces together: the web frontend's
    # POST /api/v1/chat (AgentRESTRequestHandler) and Slack's POST /slack/events
    # (AgentSlackRequestHandler). RESTAPI.run() with no handlers routes through the
    # queue pipeline instead (api/http.py's activation rule) — passing handlers here
    # takes the direct-serve path both integrations need.
    RESTAPI.run([AgentRESTRequestHandler(), AgentSlackRequestHandler()])
