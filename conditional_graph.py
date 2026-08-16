from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    age: int
    category: str
    message: str


def check_age (state: State):
    age = state["age"]

    if age >= 18:
        return"adult"
    else:
        return"minor"


def adult (state: State):
    name = state["name"]

    return{
        "message" : f"welcome {name} you are an adult."
    }

def minor(state: State):
    name = state["name"]
    return{
            "message" : f"welcome {name} you are an minor."
        }


graph = StateGraph(State)

graph.add_node("adult", adult)
graph.add_node("minor", minor)

graph.add_conditional_edges(
    START,
    check_age,
    {
        "adult": "adult",
        "minor": "minor"
    }
)

graph.add_edge("adult", END)
graph.add_edge("minor", END)


app = graph.compile()

result = app.invoke({
    "name": "chinmay",
    "age": 22
})

print(result)