# Local Setup with Virtual Environment

## Step 1: Create Virtual Environment

```cmd
python -m venv venv
```

## Step 2: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

## Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

## Step 4: Configure AWS Credentials
Look for aws-credentials-setup.md file

**Option A: Use AWS CLI (Recommended)**
```cmd
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Output format (json)

**Option B: Set Environment Variables**
These environment variables only last for that terminal session.
```cmd
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-west-2
```

## Step 5: Enable Bedrock Model Access

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Enable "Claude 3.5 Sonnet v2"
5. Click "Save changes"

## Step 6: Run the Chatbot

**Streaming version (recommended):**
```cmd
python chatbot_streaming.py
```

**Basic version:**
```cmd
python chatbot.py
```

## Deactivate Virtual Environment

When you're done:
```cmd
deactivate
```

## Troubleshooting

**If `python` command not found:**
```cmd
py -m venv venv
py -m pip install -r requirements.txt
```

**If AWS credentials not working:**
```cmd
aws sts get-caller-identity
```
This verifies your credentials are configured correctly.

**Check installed packages:**
```cmd
pip list
```
