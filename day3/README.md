# LangGraph Learning - Day 3

## Overview

Today I connected LangGraph with Google Gemini and built a basic chatbot.

The chatbot receives a user message, sends it to Gemini, receives the AI response, and stores both messages in the conversation history.

## Topics Covered

- Google Gemini API
- `ChatGoogleGenerativeAI`
- Environment variables
- `HumanMessage`
- `AIMessage`
- `add_messages`
- Chatbot node
- Conversation history
- Multi-turn conversations

---

# 1. Project Setup

I created the Day 3 project using `uv`.

```bash
uv init day3
cd day3
```

Installed the required packages:

```bash
uv add langgraph langchain-google-genai python-dotenv
```

## Environment Variables

Created a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Loaded the environment variables using:

```python
from dotenv import load_dotenv

load_dotenv()
```

Then retrieved the API key:

```python
import os

api_key = os.getenv("GOOGLE_API_KEY")
```

---

# 2. Connecting to Gemini

I created a Gemini chat model using `ChatGoogleGenerativeAI`.

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    api_key=api_key
)
```

The model can now receive messages and generate responses.

Basic flow:

```text
Python
   ↓
ChatGoogleGenerativeAI
   ↓
Gemini
   ↓
Response
```

---

# 3. Messages

Instead of sending normal strings, LangChain uses message objects.

## HumanMessage

A message sent by the user:

```python
from langchain_core.messages import HumanMessage

HumanMessage(
    content="Hello! Who are you?"
)
```

Conceptually:

```text
User
 ↓
HumanMessage
```

## AIMessage

Gemini's response is returned as an AI message.

Conceptually:

```text
Gemini
 ↓
AIMessage
```

A conversation can contain multiple messages:

```text
HumanMessage
"My name is Chinmay"

AIMessage
"Hello Chinmay!"

HumanMessage
"What is my name?"

AIMessage
"Your name is Chinmay."
```

---

# 4. Messages as State

The LangGraph state stores the conversation history.

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
```

The `messages` key stores all messages in the conversation.

Example:

```text
messages = [

    HumanMessage("Hello"),

    AIMessage("Hi! How can I help?")
]
```

---

# 5. add_messages Reducer

`add_messages` is a reducer designed for chat messages.

Without preserving previous messages, a new response could replace the old conversation.

With:

```python
messages: Annotated[list, add_messages]
```

LangGraph adds the new message to the existing conversation.

Example:

```text
Existing messages

[
    HumanMessage("Hello")
]

+

New AI response

[
    AIMessage("Hi!")
]

↓

Final messages

[
    HumanMessage("Hello"),
    AIMessage("Hi!")
]
```

Important concept:

```text
add_messages
     ↓
Preserves conversation history
```

---

# 6. Creating the Chatbot Node

A LangGraph node is a Python function.

The chatbot node receives the current state:

```python
def chatbot(state: State):
```

The current conversation is available through:

```python
state["messages"]
```

The messages are sent to Gemini:

```python
response = model.invoke(state["messages"])
```

Gemini returns a response.

The chatbot then returns the response to the graph:

```python
return {
    "messages": [response]
}
```

Because `add_messages` is used, the AI response is added to the existing messages.

Complete chatbot node:

```python
def chatbot(state: State):
    response = model.invoke(state["messages"])

    return {
        "messages": [response]
    }
```

---

# 7. Building the LangGraph

Created a graph using the `State`:

```python
graph = StateGraph(State)
```

Added the chatbot node:

```python
graph.add_node("chatbot", chatbot)
```

Connected the graph:

```python
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
```

Graph flow:

```text
START
  ↓
chatbot
  ↓
Gemini
  ↓
AI Response
  ↓
END
```

Compiled the graph:

```python
app = graph.compile()
```

---

# 8. Running the Chatbot

The graph starts with a `HumanMessage`.

```python
result = app.invoke({
    "messages": [
        HumanMessage(
            content="My name is Chinmay"
        )
    ]
})
```

The flow is:

```text
HumanMessage
"My name is Chinmay"

        ↓

LangGraph State

        ↓

chatbot node

        ↓

model.invoke(state["messages"])

        ↓

Gemini

        ↓

AIMessage

        ↓

add_messages

        ↓

Final conversation history
```

The final state contains both the user message and the AI response.

---

# 9. Printing the Conversation

The messages can be printed using:

```python
for message in result["messages"]:
    print(message.content)
```

Example:

```text
My name is Chinmay

Hello Chinmay! Nice to meet you.
```

---

# 10. Conversation History

The important concept learned today is:

```text
messages = conversation history
```

After the first interaction:

```text
Human: My name is Chinmay

AI: Hello Chinmay!
```

The conversation is stored inside:

```python
result["messages"]
```

A second message can be added to the existing conversation:

```python
result = app.invoke({
    "messages": result["messages"] + [
        HumanMessage(
            content="What is my name?"
        )
    ]
})
```

Now Gemini receives the previous conversation along with the new message.

Example:

```text
User: My name is Chinmay

AI: Hello Chinmay! Nice to meet you.

User: What is my name?

AI: Your name is Chinmay.
```

Because the previous messages are sent again, Gemini can use the conversation history to answer the second question.

---

# Key Concepts

```text
HumanMessage
    ↓
Represents a user message

AIMessage
    ↓
Represents an AI response

state["messages"]
    ↓
Stores conversation history

model.invoke(messages)
    ↓
Sends messages to Gemini

add_messages
    ↓
Adds new messages to existing conversation history

result["messages"]
    ↓
Contains the updated conversation
```

---

# Files

```text
day3/
├── main.py
├── conversation.py
├── conversation_history.py
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Important

The `.env` file contains the API key and should not be pushed to GitHub.

Example `.gitignore`:

```text
.env
.venv/
__pycache__/
```

---

# Day 3 Summary

Today I learned how to connect an LLM with LangGraph.

The complete flow is:

```text
User Input
    ↓
HumanMessage
    ↓
LangGraph State
    ↓
Chatbot Node
    ↓
Gemini
    ↓
AIMessage
    ↓
add_messages
    ↓
Conversation History
```

I also built a multi-turn conversation where Gemini could answer a second question using previous messages.

## Day 3 Complete ✅

## Next

Day 4: Build an interactive terminal chatbot.

```text
User types a message
        ↓
HumanMessage
        ↓
LangGraph
        ↓
Gemini
        ↓
AI Response
        ↓
User types the next message
```