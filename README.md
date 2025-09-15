# AWS Budget Lambda

A serverless Lambda function that automatically monitors and reports your monthly AWS spending via Notifox alerts. The function runs daily at noon MST and sends cost information to your configured Notifox audience.

## Features

- 📊 **Daily Cost Monitoring**: Automatically checks your monthly AWS spending
- 🔔 **Notifox Integration**: Sends alerts via Notifox API
- ⏰ **Scheduled Execution**: Runs daily at noon MST using EventBridge
- 🏷️ **Account Identification**: Includes AWS account ID in notifications
- 💰 **Precise Formatting**: Displays costs rounded to 2 decimal places

## Architecture

```
EventBridge (Daily at noon MST) → Lambda Function → AWS Cost Explorer → Notifox API
```

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform installed
- Python 3.10+
- Notifox account and API credentials

## Required AWS Permissions

The Lambda function requires the following IAM permissions:
- `ce:GetCostAndUsage` - Access AWS Cost Explorer
- `sts:GetCallerIdentity` - Get AWS account ID
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` - CloudWatch logging

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/notifoxhq/aws-budget-lambda.git
cd aws-budget-lambda
```

### 2. Deploy with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Verify Deployment

Check that the Lambda function was created successfully:

```bash
aws lambda list-functions --query 'Functions[?FunctionName==`budget-lambda`]'
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NOTIFOX_AUDIENCE` | Your Notifox audience ID | Yes |
| `NOTIFOX_API_KEY` | Your Notifox API key | Yes |

### Schedule

The function runs daily at **noon MST** (7 PM UTC). To modify the schedule, edit the `schedule_expression` in `terraform/eventbridge.tf`:

```hcl
schedule_expression = "cron(0 19 * * ? *)"  # 7 PM UTC = noon MST
```

## Message Format

The Lambda function sends messages in this format:

```
Account 123456789012: monthly AWS cost so far: $45.67
```

## Monitoring

- **CloudWatch Logs**: Check `/aws/lambda/budget-lambda` log group
- **EventBridge**: Monitor rule execution in CloudWatch Events
- **Lambda Metrics**: View function metrics in CloudWatch

## Troubleshooting

### Common Issues

1. **Permission Denied**: Verify IAM role has required permissions
2. **Notifox API Error**: Check your API key and audience ID
3. **Cost Data Missing**: Ensure Cost Explorer is enabled in your AWS account

### Logs

Check CloudWatch logs for detailed error information:

```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/budget-lambda"
```

## Security

- Never commit `terraform.tfvars` or any files containing API keys
- Use IAM roles with minimal required permissions
- Consider using AWS Secrets Manager for sensitive data
