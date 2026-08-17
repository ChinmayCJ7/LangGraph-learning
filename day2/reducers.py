from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages : Annotated[list[str], operator.add]

def step_one(state: State):
    return{
        "messages" : ["hello!"]
    }

def step_two(state: State):
    return{
        "messages": ["Welcome to Day 2"]
    }

graph = StateGraph(State)

graph.add_node("step_one", step_one)
graph.add_node("step_two", step_two)

graph.add_edge(START, "step_one")
graph.add_edge("step_one", "step_two")
graph.add_edge("step_two", END)

app = graph.compile()

result = app.invoke({})

print(result)