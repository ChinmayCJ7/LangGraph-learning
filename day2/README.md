# LangGraph Learning - Day 2

Today I learned how LangGraph handles state updates and how reducers can combine values instead of overwriting them.

## Topics Covered

### 1. State Overwriting

When two nodes update the same state key, the later update replaces the previous value.

Example:

```text
START
  ↓
step_one
  ↓
step_two
  ↓
END
```

State (defined as [State](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/main.py#L4) in [main.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/main.py)):
```python
from typing import TypedDict

class State(TypedDict):
    name: str
    message: str
```

Example nodes:
```python
def step_one(state: State):
    name = state["name"]

    return {
        "message": f"Hello {name}"
    }


def step_two(state: State):
    return {
        "message": "Welcome to Day 2 of LangGraph"
    }
```

Initial state:
```json
{
    "name": "chinmay"
}
```

After [step_one](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/main.py#L8):
```json
{
    "name": "chinmay",
    "message": "Hello chinmay"
}
```

After [step_two](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/main.py#L15):
```json
{
    "name": "chinmay",
    "message": "Welcome to Day 2 of LangGraph"
}
```

The second node overwrites the previous value because both nodes update the same key: `message`.

### 2. Different State Keys

Different state keys allow multiple values to be preserved.

Example state (defined as [State](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/state_multiple.py#L4) in [state_multiple.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/state_multiple.py)):
```python
class State(TypedDict):
    name: str
    message: str
    message2: str
```

[step_one](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/state_multiple.py#L9):
```python
def step_one(state: State):
    name = state["name"]

    return {
        "message": f"Hello {name}"
    }
```

[step_two](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/state_multiple.py#L16):
```python
def step_two(state: State):
    return {
        "message2": "Welcome to Day 2 of LangGraph"
    }
```

Final state:
```json
{
    "name": "chinmay",
    "message": "Hello chinmay",
    "message2": "Welcome to Day 2 of LangGraph"
}
```

Important Concept:
```text
Same state key
    ↓
Value is overwritten

Different state keys
    ↓
Both values are preserved
```

### 3. Reducers

Reducers allow LangGraph to combine updates instead of overwriting them.

For this example, I used `operator.add`.

State (defined as [State](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/reducers.py#L5) in [reducers.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/reducers.py)):
```python
from typing import TypedDict, Annotated
import operator


class State(TypedDict):
    messages: Annotated[list[str], operator.add]
```

The reducer `operator.add` combines values using `+`.

Example:
```python
["Hello!"] + ["Welcome to Day 2"]
```

Result:
```python
["Hello!", "Welcome to Day 2"]
```

#### Reducer Example

Graph flow:
```text
START
  ↓
step_one
  ↓
step_two
  ↓
END
```

Node one ([step_one](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/reducers.py#L8)):
```python
def step_one(state: State):
    return {
        "messages": ["Hello!"]
    }
```

Node two ([step_two](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/reducers.py#L13)):
```python
def step_two(state: State):
    return {
        "messages": ["Welcome to Day 2"]
    }
```

Final state:
```json
{
    "messages": [
        "Hello!",
        "Welcome to Day 2"
    ]
}
```

Without a reducer, updating the same key normally replaces the old value.

With `operator.add`:
```text
Node 1
["Hello!"]

        +

Node 2
["Welcome to Day 2"]

        ↓

Final State

["Hello!", "Welcome to Day 2"]
```

## Concepts Learned

- State updates
- State overwriting
- Different state keys
- Preserving multiple values
- Reducers
- `Annotated`
- `operator.add`

## Practice Files

- [main.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/main.py): Practice for state overwriting.
- [state_multiple.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/state_multiple.py): Practice for preserving values using different state keys.
- [reducers.py](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/reducers.py): Practice for combining values using a reducer.
- [pyproject.toml](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/pyproject.toml)
- [uv.lock](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/uv.lock)
- [README.md](file:///Users/chinmay/Developer/Python/LangGraph/langgraph-learning/day2/README.md)

## Day 2 Summary

```text
Same Key
    ↓
Overwrite

Different Keys
    ↓
Preserve Both Values

Reducer
    ↓
Combine Values
```

## Next Topic

Day 3 will focus on using LangGraph with an actual LLM.

```text
Messages
   ↓
HumanMessage
AIMessage
   ↓
Chatbot Node
   ↓
Gemini + LangGraph
```
