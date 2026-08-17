from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    message: str
    message2: str

def step_one(state: State):
    name = state["name"]

    return{
        "message" : f"Hello {name}"
    }

def step_two(state: State):
    return{
        "message2" : f"Welcome to Day 2 of LangGraph"
    }


graph = StateGraph(State)

graph.add_node("step_one", step_one)
graph.add_node("step_two", step_two)

graph.add_edge(START, "step_one")
graph.add_edge("step_one", "step_two")
graph.add_edge("step_two", END)

app = graph.compile()

result = app.invoke({
    "name":"chinmay"
})

print(result)