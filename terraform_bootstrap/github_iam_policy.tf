data "aws_caller_identity" "current" {}

resource "aws_iam_policy" "github_actions_policy" {
  name        = "GitHubActionsWorkflowPolicy"
  description = "Policy for GitHub Actions to manage EKS infrastructure"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "TerraformStateAccess"
        Effect = "Allow"
        Action = ["s3:ListBucket", "s3:GetObject", "s3:PutObject"]
        Resource = [
          "arn:aws:s3:::lambda-project-terraform-state-0001",
          "arn:aws:s3:::lambda-project-terraform-state-0001/*"
        ]
      },
      {
        Sid    = "TerraformLockAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:DescribeTable",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem"
        ]
        # Dynamically uses your account ID
        Resource = "arn:aws:dynamodb:ap-south-1:${data.aws_caller_identity.current.account_id}:table/lambda-project-terraform-locks-0001"
      },
      {
        Sid    = "FullAccessToServices"
        Effect = "Allow"
        Action = [
          "ec2:*",
          "s3:*",
          "lambda:*",
          "logs:*",
          "iam:*",
          "ssm:*",
          "cloudwatch:*"
        ]
        Resource = "*"
      },
      {
        Sid      = "STSAccess"
        Effect   = "Allow"
        Action   = ["sts:GetCallerIdentity"]
        Resource = "*"
      }
    ]
  })
}
