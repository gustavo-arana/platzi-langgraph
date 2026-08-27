from langchain.agents import create_agent
from agents.support.nodes.assistant.tools import tools
from agents.support.nodes.assistant.prompt import SYSTEM_PROMPT

assistant = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)