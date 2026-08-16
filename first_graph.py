from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    message: str


def greet(state: State):
    name = state["name"]

    return {
        "message" : f"Hello {name}, Welcome to LangGraph"
    }


graph = StateGraph(State)

graph.add_node("greet", greet)

graph.add_edge(START, "greet")
graph.add_edge("greet", END)


app = graph.compile()


result = app.invoke({
    "name" : "chinmay"
})

print(result)