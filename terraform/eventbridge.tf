resource "aws_cloudwatch_event_rule" "budget_lambda_rule" {
  name = "budget-lambda-rule"
  description = "Budget lambda rule"
  schedule_expression = "cron(0 19 * * ? *)"
}

resource "aws_cloudwatch_event_target" "budget_lambda_target" {
  rule = aws_cloudwatch_event_rule.budget_lambda_rule.name
  arn = aws_lambda_function.budget_lambda.arn
}