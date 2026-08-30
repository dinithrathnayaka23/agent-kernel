from agentkernel.api import RESTAPI, AgentRESTRequestHandler
from agentkernel.pydanticai import PydanticAIModule
from agentkernel.slack import AgentSlackRequestHandler
from agentkernel.telegram import AgentTelegramRequestHandler

from agent import AGENTS

PydanticAIModule(AGENTS)


if __name__ == "__main__":
    # Explicit handler list serves all three interfaces together: the web frontend's
    # POST /api/v1/chat (AgentRESTRequestHandler), Slack's POST /slack/events
    # (AgentSlackRequestHandler), and Telegram's POST /telegram/webhook
    # (AgentTelegramRequestHandler). RESTAPI.run() with no handlers routes through the
    # queue pipeline instead (api/http.py's activation rule) — passing handlers here
    # takes the direct-serve path these integrations need.
    RESTAPI.run([AgentRESTRequestHandler(), AgentSlackRequestHandler(), AgentTelegramRequestHandler()])
