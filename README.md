# LangGraph-learning

# LangGraph Learning - Day 1

Today I started learning the basics of LangGraph.

## Topics Covered

### 1. State
I learned that `State` is used to define the data that moves through the graph.

Example:

```python
from typing import TypedDict

class State(TypedDict):
    name: str
    age: int
    message: str
```

The state carries data from one node to another.

---

### 2. Nodes
A node is a Python function that receives the current state and can return updates.

Example:

```python
def greet(state: State):
    name = state["name"]
    return {
        "message": f"Hello {name}!"
    }
```

---

### 3. Edges
Edges define how nodes are connected.

Example:

```python
graph.add_edge(START, "greet")
graph.add_edge("greet", END)
```

Flow:

```text
START
  ↓
greet
  ↓
END
```

---

### 4. Multiple Nodes
I created graphs with multiple nodes.

Example:

```text
START
  ↓
greet
  ↓
introduce
  ↓
END
```

Each node can access the current state and update it.

---

### 5. Conditional Edges
I learned how to route the graph based on a condition.

Example:

```text
START
  ↓
check_number
 ↙       ↘
even     odd
 ↓       ↓
END     END
```

The routing function returns a value:

```python
def check_number(state: State):
    number = state["number"]
    if number % 2 == 0:
        return "even"
    else:
        return "odd"
```

Then LangGraph uses that value to choose the next node.

```python
graph.add_conditional_edges(
    START,
    check_number,
    {
        "even": "even",
        "odd": "odd"
    }
)
```

---

### 6. Conditional Routing After a Node
I also learned that a conditional edge can happen after another node.

Example:

```text
START
  ↓
process_number
  ↓
check_number
 ↙       ↘
even     odd
 ↓       ↓
END     END
```

Example:

```python
graph.add_edge(START, "process_number")
graph.add_conditional_edges(
    "process_number",
    check_number,
    {
        "even": "even",
        "odd": "odd"
    }
)
```

---

## Important Concept: State Updates
Nodes can update the state.

Example:

```python
def process_number(state: State):
    number = state["number"]
    return {
        "message": f"Processing number {number}"
    }
```

If another node later returns a value for the same key:

```python
return {
    "message": "29 is an odd number"
}
```

The previous value of `message` is overwritten.

---

## Practice Completed

- Simple greeting graph
- Multiple node graph
- Age-based conditional routing
- Even/odd conditional routing
- Conditional routing after a node

---

## Concepts Learned

- `StateGraph`
- `TypedDict`
- State
- Nodes
- Edges
- `START`
- `END`
- `add_node()`
- `add_edge()`
- `add_conditional_edges()`
- `compile()`
- `invoke()`
- Conditional routing
- State updates and overwriting

---

## Next Topic

The next topic will be:

```text
State Management
  ↓
How state updates work
  ↓
Overwriting values
  ↓
Keeping multiple values
  ↓
Reducers
```
