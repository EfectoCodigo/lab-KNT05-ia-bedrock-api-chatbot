"""
Simple chatbot using LangGraph with AWS Bedrock
Demonstrates best practices for Bedrock integration with conversation memory
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_aws import ChatBedrock


# Define the state schema for the chatbot
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize the Bedrock chat model
# Using Claude 3.5 Haiku - cheap and reliable for testing
# Cost: $0.80 input / $4.00 output per 1M tokens
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    region_name="us-west-2",
)


def chatbot_node(state: State):
    """Process messages through the LLM"""
    return {"messages": [llm.invoke(state["messages"])]}


# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()


def chat(user_input: str, conversation_history: list = None):
    """
    Send a message to the chatbot and get a response
    
    Args:
        user_input: The user's message
        conversation_history: Previous messages (optional)
    
    Returns:
        tuple: (response_text, updated_conversation_history)
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Invoke the graph
    result = graph.invoke({"messages": conversation_history})
    
    # Extract the assistant's response
    assistant_message = result["messages"][-1]
    response_text = assistant_message.content
    
    # Update conversation history
    conversation_history.append({"role": "assistant", "content": response_text})
    
    return response_text, conversation_history


if __name__ == "__main__":
    print("Chatbot initialized! Type 'quit' to exit.\n")
    
    conversation = []
    
    while True:
        user_message = input("You: ")
        
        if user_message.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        
        response, conversation = chat(user_message, conversation)
        print(f"\nAssistant: {response}\n")
