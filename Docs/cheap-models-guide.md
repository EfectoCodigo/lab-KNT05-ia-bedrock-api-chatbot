# Cheapest AWS Bedrock Models for Testing (2026)

## Top 3 Cheapest Models

### 1. 🏆 Mistral Ministral 3B (RECOMMENDED FOR TESTING)
- **Model ID:** `mistral.ministral-3b-3-0`
- **Cost:** $0.10 per 1M tokens (input and output)
- **Best for:** Testing, development, simple chatbots
- **Cost per message:** ~$0.00003 (0.003 cents)
- **$10 budget:** ~333,000 messages

```python
llm = ChatBedrock(
    model_id="mistral.ministral-3b-3-0",
    model_kwargs={"temperature": 0.7, "max_tokens": 2048}
)
```

### 2. Google Gemma 3 4B
- **Model ID:** `google.gemma-3-4b`
- **Cost:** $0.04 input / $0.08 output per 1M tokens
- **Best for:** Lightweight tasks, high volume
- **Cost per message:** ~$0.000024 (0.0024 cents)
- **$10 budget:** ~416,000 messages

```python
llm = ChatBedrock(
    model_id="google.gemma-3-4b",
    model_kwargs={"temperature": 0.7, "max_tokens": 2048}
)
```

### 3. Mistral Voxtral Mini
- **Model ID:** `mistral.voxtral-mini-1-0`
- **Cost:** $0.04 per 1M tokens (input and output)
- **Best for:** Voice/audio applications
- **Cost per message:** ~$0.000012 (0.0012 cents)
- **$10 budget:** ~833,000 messages

---

## Cost Comparison Table

| Model | Input (per 1M) | Output (per 1M) | Cost/Message | Messages/$10 |
|-------|----------------|-----------------|--------------|--------------|
| **Mistral Ministral 3B** | $0.10 | $0.10 | $0.00003 | 333,000 |
| **Google Gemma 3 4B** | $0.04 | $0.08 | $0.00002 | 416,000 |
| **Mistral Voxtral Mini** | $0.04 | $0.04 | $0.00001 | 833,000 |
| Mistral Ministral 8B | $0.15 | $0.15 | $0.00005 | 200,000 |
| NVIDIA Nemotron Nano 2 | $0.06 | $0.23 | $0.00006 | 166,000 |
| Claude 3.5 Haiku | $0.80 | $4.00 | $0.00090 | 11,000 |
| Claude 3.5 Sonnet | $6.00 | $30.00 | $0.00300 | 3,300 |

*Assumes ~100 input tokens + ~200 output tokens per message*

---

## Recommended Setup for Testing

### Ultra-Cheap Testing (Ministral 3B)
```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="mistral.ministral-3b-3-0",
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 1024,  # Lower for even cheaper
    }
)
```

**Pros:**
- 30x cheaper than Claude Sonnet
- Perfect for development/testing
- Good enough for simple conversations

**Cons:**
- Less capable than larger models
- May struggle with complex reasoning
- Smaller context window

---

## When to Upgrade

**Stick with cheap models for:**
- Initial development and testing
- Simple Q&A chatbots
- High-volume, low-complexity tasks
- Learning LangGraph/Bedrock

**Upgrade to better models when:**
- Need complex reasoning (use Claude Sonnet)
- Production deployment with quality requirements
- Advanced features like function calling
- Multi-step reasoning tasks

---

## IAM Policy for Cheap Models Only

Restrict access to only the cheapest models:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "OnlyCheapModels",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/mistral.ministral-3b-3-0",
        "arn:aws:bedrock:*::foundation-model/google.gemma-3-4b",
        "arn:aws:bedrock:*::foundation-model/mistral.voxtral-mini-1-0"
      ]
    }
  ]
}
```

---

## Batch Mode (50% Discount)

For non-real-time processing, use batch mode for 50% savings:

**Ministral 3B Batch:**
- Input: $0.05 per 1M tokens
- Output: $0.05 per 1M tokens
- **Cost per message:** $0.000015 (half price!)

**Note:** Batch mode has delays (minutes to hours), not suitable for chatbots.

---

## Cost Monitoring Commands

```bash
# Check your current spending
aws ce get-cost-and-usage \
  --time-period Start=2026-03-01,End=2026-03-02 \
  --granularity DAILY \
  --metrics BlendedCost \
  --filter file://bedrock-filter.json

# bedrock-filter.json
{
  "Dimensions": {
    "Key": "SERVICE",
    "Values": ["Amazon Bedrock"]
  }
}
```

---

## Real Cost Examples

**Testing scenario (1000 test messages):**
- Ministral 3B: $0.03
- Gemma 3 4B: $0.02
- Claude Sonnet: $3.00

**Development (10,000 messages/month):**
- Ministral 3B: $0.30/month
- Gemma 3 4B: $0.24/month
- Claude Sonnet: $30/month

**Production (100,000 messages/month):**
- Ministral 3B: $3/month
- Claude Sonnet: $300/month

---

## Quick Switch Between Models

```python
# Easy model switching
MODELS = {
    "cheap": "mistral.ministral-3b-3-0",
    "balanced": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "premium": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}

# Use environment variable to switch
import os
model_tier = os.getenv("MODEL_TIER", "cheap")

llm = ChatBedrock(
    model_id=MODELS[model_tier],
    model_kwargs={"temperature": 0.7, "max_tokens": 2048}
)
```

---

## Summary

For testing your LangGraph chatbot:
1. **Start with Mistral Ministral 3B** ($0.10 per 1M tokens)
2. Set a $5-10 budget alert
3. Test thoroughly without worrying about costs
4. Upgrade to Claude Haiku or Sonnet when ready for production

With Ministral 3B, you can send 333,000 messages for just $10!
