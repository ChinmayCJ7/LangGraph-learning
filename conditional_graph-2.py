from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number : int
    message : str

def check_number(state: State):

    number = state["number"]

    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

    
def even(state: State):
    number = state["number"]

    return{
        "message" : f"{number} is Even number"
    }

    
def odd(state: State):
    number = state["number"]

    return{
        "message" : f"{number} is Odd number"
    }


graph = StateGraph(State)

graph.add_node("even", even)
graph.add_node("odd", odd)

graph.add_conditional_edges(
    START,
    check_number,
    {
        "Even": "even",
        "Odd": "odd"
    }
)

graph.add_edge("even", END)
graph.add_edge("odd", END)


app = graph.compile()

result = app.invoke({
    "number": 29
})

print(result)