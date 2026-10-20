output "ticket_table_name" {
  value = aws_dynamodb_table.tickets.name
}

output "lambda_function_name" {
  value = aws_lambda_function.handler.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.handler.arn
}
