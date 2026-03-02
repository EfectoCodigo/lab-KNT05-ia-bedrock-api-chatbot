"""
Streaming chatbot using LangGraph with AWS Bedrock
Best practice: Use streaming for better user experience
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_aws import ChatBedrock


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize with streaming enabled
# Using Claude 3.5 Haiku - cheap and reliable for testing
# Cost: $0.80 input / $4.00 output per 1M tokens
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    region_name="us-west-2",
    streaming=True,  # Enable streaming
)


def chatbot_node(state: State):
    """Process messages through the LLM"""
    return {"messages": [llm.invoke(state["messages"])]}


# Build and compile the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


def chat_stream(user_input: str, conversation_history: list = None):
    """
    Stream responses from the chatbot token by token
    
    Args:
        user_input: The user's message
        conversation_history: Previous messages (optional)
    
    Yields:
        str: Token chunks as they arrive
    """
    if conversation_history is None:
        conversation_history = []
    
    conversation_history.append({"role": "user", "content": user_input})
    
    # Stream the response token by token
    full_response = ""
    for chunk in llm.stream(conversation_history):
        if hasattr(chunk, 'content') and chunk.content:
            full_response += chunk.content
            yield chunk.content
    
    # Update conversation history with complete response
    conversation_history.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    print("Streaming Chatbot initialized! Type 'quit' to exit.\n")
    
    conversation = []
    
    while True:
        user_message = input("You: ")
        
        if user_message.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        
        print("\nAssistant: ", end="", flush=True)
        
        for chunk in chat_stream(user_message, conversation):
            print(chunk, end="", flush=True)
        
        print("\n")
