terraform {
  backend "s3" {
    bucket         = "lambda-project-terraform-state-0001"
    key            = "lambda/lambda.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "lambda-project-terraform-locks-0001"
    encrypt        = true
  }
}

