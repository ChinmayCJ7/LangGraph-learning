import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


class State(TypedDict):
    messages: Annotated[list, add_messages]


model = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    api_key=api_key
)


def chatbot(state: State):
    response = model.invoke(state["messages"])

    return {
        "messages": [response]
    }


graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()


result = app.invoke({
    "messages": [
        HumanMessage(content="My name is Chinmay")
    ]
})

# print(result["messages"][-1].content)

for message in result["messages"]:
    print(message.content)