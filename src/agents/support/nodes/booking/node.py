from langchain.agents import create_agent
from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import system_prompt

booking_node = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=tools,
    system_prompt=system_prompt,
)