# Architecture notes

Caller → Amazon Connect → Lex V2 → Python Lambda. Lambda routes deterministic intents, writes/reads synthetic tickets in DynamoDB, or calls Bedrock for a knowledge answer. Lex returns the response to Connect. Connect can transfer unresolved calls to a human queue. CloudWatch captures operational logs and metrics.

Trust boundaries:
- Speech, transcripts, and slots are untrusted input.
- Lambda bounds input lengths and uses deterministic code for ticket operations.
- Bedrock is not authoritative for company policy; use approved documentation and retrieval for grounded answers.
- Caller identity is not verified in this demo; do not return sensitive ticket information until authentication/authorization is implemented.

Reliability:
- Keep deterministic support flows working if Bedrock is unavailable.
- Configure timeouts and error branches.
- Add CloudWatch alarms for Lambda errors, duration, and throttles.
- Exclude sensitive values from logs.
