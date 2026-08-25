from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
import random

llm = init_chat_model("google_genai:gemini-3.5-flash-lite", temperature=1)
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": ["vs_6a8bfc14c78c8191ad5cb84e42001e5f"],
}

llm = llm.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    phone: str
    my_age: int

class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: int = Field(description="The age of the person")

llm_with_structured_output = init_chat_model("anthropic:claude-sonnet-4-5-20250929", temperature=1)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 0:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    customer_name = state.get("customer_name", 'Jhon Doe')
    system_message = f"You are a helpful assistant that extracts contact information from a given conversation. The customer name is {customer_name}."
    ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_message]
    print(new_state)
    return new_state

from langgraph.graph import  StateGraph, START, END

builder = StateGraph(State)
builder.add_node("extractor", extractor)
builder.add_node("conversation", conversation)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()