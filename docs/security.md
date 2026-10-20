# Security checklist

- Use synthetic demo data.
- Never collect/log passwords, MFA codes, recovery keys, or tokens.
- Add caller authentication and authorization before ticket lookup.
- Do not allow the model to execute commands or modify AWS/identity systems.
- Scope Lambda IAM to the one DynamoDB table and chosen Bedrock model.
- Configure encryption, log retention, alarms, throttling, input limits, and timeouts.
- For RAG, use approved documents, source metadata, retrieval filters, and prompt-injection evaluation.
- Route low-confidence, sensitive, or unresolved issues to a human.
- Protect Terraform state with an encrypted remote backend and locking.
- Review Connect telephony and Bedrock model costs before live testing.
