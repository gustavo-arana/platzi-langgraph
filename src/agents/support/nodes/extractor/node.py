from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from agents.support.state import State
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

llm = init_chat_model("anthropic:claude-sonnet-4-5-20250929", temperature=1)
llm = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 0:
        #schema = llm.invoke([("system", SYSTEM_PROMPT + history),("user", history)])
        #schema = llm.invoke([SYSTEM_PROMPT + history[-1].text])
        schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state