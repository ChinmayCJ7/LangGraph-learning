from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    number : int
    message : str

def process_number(state: State):

    number = state["number"]

    return{
        "message" : f"the number for processing is {number}"
    }

def check_num(state: State):
    number = state["number"]

    if number % 2 == 0:
        return "even"
    return "odd"


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

graph.add_node("process_number", process_number)
graph.add_node("even", even)
graph.add_node("odd", odd)

graph.add_edge(START, "process_number")
graph.add_conditional_edges(
    "process_number",
    check_num,
    {
        "even" : "even",
        "odd"  : "odd"
    }
)

graph.add_edge("even", END)
graph.add_edge("odd", END)


app = graph.compile()

result = app.invoke({
    "number": 29
})

print(result)