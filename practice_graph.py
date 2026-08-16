from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name : str
    age : str
    greeting: str
    introduction: str


def greet(state: State):
    name = state["name"]

    return {
        "greeting" : f"Hello {name}!"
    }

def introduce(state: State):
    name = state["name"]
    age = state["age"]

    return {
        "introduction" : f"My name is {name} and I am {age} years old"
    }


graph = StateGraph(State)

graph.add_node("greet", greet)
graph.add_node("introduce", introduce)


graph.add_edge(START, "greet")
graph.add_edge("greet", "introduce")
graph.add_edge("introduce", END)

app = graph.compile()

result = app.invoke({
    "name" : "chinmay",
    "age" : "22"
})

print(result)