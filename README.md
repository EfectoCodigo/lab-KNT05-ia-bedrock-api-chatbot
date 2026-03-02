# AWS Bedrock Chatbot with LangGraph

A minimal chatbot implementation using LangGraph and AWS Bedrock, following best practices.

## Features

- Simple conversational chatbot with memory
- Streaming support for better UX
- Uses Claude 3.5 Sonnet (latest model)
- Proper state management with LangGraph
- AWS credentials handling

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Choose one of these methods:

**Option A: AWS CLI (Recommended)**
```bash
aws configure
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option C: Bearer Token**
```bash
export AWS_BEARER_TOKEN_BEDROCK=your_token
```

### 3. Enable Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Navigate to "Model access"
3. Request access to "Claude 3.5 Sonnet v2"
4. Wait for approval (usually instant)

## Usage

### Basic Chatbot

```bash
python chatbot.py
```

### Streaming Chatbot (Recommended)

```bash
python chatbot_streaming.py
```

## Code Examples

### Simple Usage

```python
from chatbot import chat

response, history = chat("Hello! What can you help me with?")
print(response)

# Continue conversation with memory
response, history = chat("Tell me a joke", history)
print(response)
```

### Streaming Usage

```python
from chatbot_streaming import chat_stream

conversation = []
for chunk in chat_stream("Write a short poem", conversation):
    print(chunk, end="", flush=True)
```

## Best Practices Implemented

1. **Model Selection**: Uses Claude 3.5 Sonnet for optimal balance of performance and cost
2. **Streaming**: Provides real-time response feedback
3. **State Management**: LangGraph handles conversation history properly
4. **Security**: Credentials loaded from environment/AWS config (never hardcoded)
5. **Temperature**: Set to 0.7 for balanced creativity and consistency
6. **Token Limits**: Configured max_tokens to prevent runaway costs

## Available Models

You can change the `model_id` to use different models:

- `anthropic.claude-3-5-sonnet-20241022-v2:0` (Recommended)
- `anthropic.claude-3-5-haiku-20241022-v1:0` (Faster, cheaper)
- `anthropic.claude-3-opus-20240229-v1:0` (Most capable)
- `amazon.titan-text-premier-v1:0` (AWS native)

## Troubleshooting

**Error: "Could not load credentials"**
- Ensure AWS credentials are configured properly
- Check IAM permissions include `bedrock:InvokeModel`

**Error: "Model access denied"**
- Enable model access in AWS Bedrock console
- Wait a few minutes for access to propagate

**Error: "Region not supported"**
- Bedrock is available in: us-east-1, us-west-2, ap-southeast-1, etc.
- Check [AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) for current regions

## References

- [LangChain AWS Documentation](https://python.langchain.com/docs/integrations/chat/bedrock/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
