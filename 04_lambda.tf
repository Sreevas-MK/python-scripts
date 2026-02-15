# 1. Archive the script
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_scripts/eip_auditor_lambda.py"
  output_path = "${path.module}/lambda_function_payload.zip"
}

# 2. IAM role for Lambda execution
data "aws_iam_policy_document" "assume_lambda_exec_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_exec_role.json
}

# 3. Logging Permissions (Essential for seeing output)
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 4. EC2 Read Permissions
resource "aws_iam_role_policy_attachment" "lambda_ec2" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

# 5. Lambda function
resource "aws_lambda_function" "eip_auditor" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "EIP_Auditor_Automation"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "eip_auditor_lambda.lambda_handler"
  runtime          = "python3.12"
  timeout          = 60
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      ENVIRONMENT = "Development"
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Project     = var.project_name
    Environment = "Development"
  }
}

# 6. EventBridge (The Cron)
resource "aws_cloudwatch_event_rule" "daily_cron" {
  name                = "daily-eip-audit-schedule"
  schedule_expression = "cron(30 3 * * ? *)"
}

resource "aws_cloudwatch_event_target" "trigger_lambda" {
  target_id = "EIP_Auditor"
  rule      = aws_cloudwatch_event_rule.daily_cron.name
  arn       = aws_lambda_function.eip_auditor.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.eip_auditor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_cron.arn
}
