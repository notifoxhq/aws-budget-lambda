# Package the Lambda function code
data "archive_file" "example" {
  type        = "zip"
  source_file = "${path.module}/../src/main.py"
  output_path = "${path.module}/../src/function.zip"
}

resource "aws_lambda_function" "budget_lambda" {
  function_name = "budget-lambda"
  handler       = "main.lambda_handler"
  runtime       = "python3.10"
  role          = aws_iam_role.budget_lambda_role.arn
  filename      = data.archive_file.example.output_path
  layers        = ["arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-requests:23"]


  environment {
    variables = {
      NOTIFOX_AUDIENCE = var.NOTIFOX_AUDIENCE
      NOTIFOX_API_KEY  = var.NOTIFOX_API_KEY
    }
  }
}

resource "aws_cloudwatch_log_group" "budget_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.budget_lambda.function_name}"
  retention_in_days = 30
}

resource "aws_iam_role" "budget_lambda_role" {
  name = "budget-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "budget_lambda_policy" {
  name = "budget-lambda-policy"
  role = aws_iam_role.budget_lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      },
      {
        Action   = "ce:GetCostAndUsage",
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action   = "sts:GetCallerIdentity"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}