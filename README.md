# AWS Budget Lambda

A serverless Lambda function that notifies you of your month-to-date AWS spend using Notifox.

![Screenshot of text received via Notifox](https://github.com/notifoxhq/aws-budget-lambda/blob/main/img/text.jpg?raw=true)

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform installed
- Notifox account and API credentials

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/notifoxhq/aws-budget-lambda.git
cd aws-budget-lambda
```

### 2. Configure `terraform.tfvars`
This file will be used by terraform to set environment variables inside the Lambda function.

Get your Notifox API key and audience from the console at https://console.notifox.com.

#### Audience
![Screenshot of audience in Notifox](https://github.com/notifoxhq/aws-budget-lambda/blob/main/img/audience.png?raw=true)

#### Token
![Screenshot of token in Notifox](https://github.com/notifoxhq/aws-budget-lambda/blob/main/img/token.png?raw=true)

```bash
# terraform.tfvars
NOTIFOX_API_KEY="YOUR_API_KEY"
NOTIFOX_AUDIENCE="YOUR AUDIENCE"
SCHEDULE_EXPRESSION="0 20 * * ? *" # 8 PM UTC, every day
```


### 3. Deploy with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 4. Validate functionality

```bash
aws lambda invoke --function-name budget-lambda /dev/null
```


## Troubleshooting

### Common Issues

1. **Permission Denied**: Verify IAM role has required permissions
2. **Notifox API Error**: Check your API key and audience ID
3. **Cost Data Missing**: Ensure Cost Explorer is enabled in your AWS account
