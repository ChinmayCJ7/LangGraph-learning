import os

from dotenv import load_dotenv

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")



class State(TypedDict):
    messages : Annotated[list, add_messages]



model = ChatGroq(
    model = "groq/compound",
    api_key=api_key
)


def chatbot(state: State):
    response = model.invoke(state["messages"][-10:])

    return{
        "messages": [response]
    }

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


memory = MemorySaver()

app = graph.compile(
    checkpointer=memory
)


messages = []

while True:
    user_input = input("you: ")

    if user_input.lower() == "exit":
        break

    result = app.invoke({
        "messages": [
            HumanMessage(content=user_input)
        ]
    },
    config={
        "configurable": {
            "thread_id": "chinmay2"
        }
    }
    )

    print("AI:", result["messages"][-1].content)