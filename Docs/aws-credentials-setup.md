# AWS Credentials Setup - Best Practices for Bedrock

## Step 1: Create IAM User with Least Privilege

### 1.1 Go to AWS Console → IAM → Users → Create User

- Username: `bedrock-chatbot-dev` (or your preferred name)
- Enable "Provide user access to the AWS Management Console" (optional)
- Click "Next"

### 1.2 Create Custom Policy (Recommended - Least Privilege)

Instead of attaching full Bedrock access, create a minimal policy:

**Go to IAM → Policies → Create Policy → JSON**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvokeOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-haiku-20241022-v1:0",
        "arn:aws:bedrock:*::foundation-model/mistral.ministral-3b-3-0",
        "arn:aws:bedrock:*::foundation-model/google.gemma-3-4b",
        "arn:aws:bedrock:*::foundation-model/mistral.voxtral-mini-1-0"
      ]
    },
    {
      "Sid": "ListModelsOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock:ListFoundationModels"
      ],
      "Resource": "*"
    }
  ]
}
```

**Policy Name:** `BedrockChatbotInvokeOnly`

This policy:
- ✅ Only allows invoking specific Claude models
- ✅ Cannot create/delete resources
- ✅ Cannot access other AWS services
- ✅ Cannot customize models or access training data

### 1.3 Attach Policy to User

- Select your new policy `BedrockChatbotInvokeOnly`
- Click "Next" → "Create User"

### 1.4 Create Access Keys

- Click on the user you just created
- Go to "Security credentials" tab
- Click "Create access key"
- Select "Application running outside AWS"
- Click "Next" → "Create access key"
- **SAVE THESE IMMEDIATELY** (you won't see them again):
  - Access Key ID
  - Secret Access Key

---

## Step 2: Set Up Cost Limits and Alerts

### Option A: AWS Budgets (Recommended)

**Go to AWS Console → Billing → Budgets → Create Budget**

1. **Budget Type:** Cost budget
2. **Budget Name:** `bedrock-monthly-limit`
3. **Period:** Monthly
4. **Budget Amount:** $10 (or your preferred limit)
5. **Filters:**
   - Service: Amazon Bedrock
6. **Alert Thresholds:**
   - 50% of budgeted amount
   - 80% of budgeted amount
   - 100% of budgeted amount
7. **Email Recipients:** Your email

**Note:** AWS Budgets alerts are reactive (notify after spending), not preventive. They don't automatically stop usage.

### Option B: CloudWatch Alarms for Real-Time Monitoring

**Go to CloudWatch → Alarms → Create Alarm**

1. Select metric: `AWS/Bedrock` → `InvocationCount`
2. Set threshold (e.g., 1000 invocations per day)
3. Configure SNS notification to your email

### Option C: Service Control Policies (Advanced)

For organizations, you can use SCPs to enforce guardrails:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyExpensiveModels",
      "Effect": "Deny",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-opus*"
      ]
    }
  ]
}
```

---

## Step 3: Enable Model Access

**Go to AWS Console → Amazon Bedrock → Model Access**

1. Click "Manage model access"
2. Enable:
   - ✅ Claude 3.5 Sonnet v2
   - ✅ Claude 3.5 Haiku (optional, cheaper)
3. Click "Save changes"
4. Wait for "Access granted" status

---

## Step 4: Configure Credentials Locally

### Option A: AWS CLI (Recommended)

```cmd
aws configure
```

Enter:
- AWS Access Key ID: [your key]
- AWS Secret Access Key: [your secret]
- Default region: us-east-1
- Default output format: json

### Option B: Environment Variables (Session-only)

```cmd
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1
```

---

## Cost Estimates (as of 2026)

**Claude 3.5 Sonnet v2:**
- Input: ~$3 per 1M tokens
- Output: ~$15 per 1M tokens

**Typical chatbot usage:**
- Average message: ~100 input tokens + ~200 output tokens
- Cost per message: ~$0.003 (less than 1 cent)
- 1000 messages ≈ $3
- $10 budget ≈ 3,000+ messages

**Claude 3.5 Haiku (cheaper alternative):**
- Input: ~$0.80 per 1M tokens
- Output: ~$4 per 1M tokens
- Cost per message: ~$0.0009
- $10 budget ≈ 11,000+ messages

---

## Additional Security Best Practices

### 1. Use MFA on IAM User
- Go to IAM → Users → Security credentials
- Enable MFA for console access

### 2. Rotate Access Keys Regularly
- Create new keys every 90 days
- Delete old keys after rotation

### 3. Use IAM Roles Instead (Production)
- For EC2/Lambda: Use instance profiles/execution roles
- For local dev: Use AWS SSO or temporary credentials

### 4. Monitor Usage
- Check CloudWatch metrics regularly
- Review AWS Cost Explorer monthly
- Set up anomaly detection in Cost Management

### 5. Use VPC Endpoints (Production)
- Keep traffic within AWS network
- Add VPC endpoint policies for additional restrictions

---

## Testing Your Setup

After configuration, test your credentials:

```cmd
# Test AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Test specific model access
aws bedrock invoke-model ^
  --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 ^
  --body "{\"anthropic_version\":\"bedrock-2023-05-31\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}],\"max_tokens\":100}" ^
  --region us-east-1 ^
  output.json
```

---

## Troubleshooting

**"Access Denied" errors:**
- Verify IAM policy is attached to user
- Check model access is enabled in Bedrock console
- Ensure correct region (Bedrock not available in all regions)

**Budget alerts not working:**
- Budgets can take 24 hours to activate
- Check email spam folder
- Verify SNS topic subscription

**High costs:**
- Check CloudWatch metrics for unexpected usage
- Review application logs for retry loops
- Consider switching to Haiku model for testing

---

## References

- [AWS Bedrock Least Privilege Guide](https://aws.amazon.com/blogs/security/implementing-least-privilege-access-for-amazon-bedrock/)
- [AWS Budgets Documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
