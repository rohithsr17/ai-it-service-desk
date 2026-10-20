# Console-first AWS build

## 1. Region
Choose one Region where Connect, Lex V2, Lambda, DynamoDB, and your selected Bedrock model are available. Model availability and access vary by Region/account.

## 2. DynamoDB
Create table `itsm-demo-tickets`, partition key `ticket_id` (String), on-demand capacity. Use only synthetic ticket data.

## 3. Lambda
Create `itsm-lex-handler` from scratch with Python 3.12 (or a currently supported runtime), handler `app.lambda_handler`. ZIP the contents of `lambda/`, upload the ZIP, and set timeout to 15 seconds initially.
Environment:
- `TICKET_TABLE=itsm-demo-tickets`
- `BEDROCK_ENABLED=false`
- Set `BEDROCK_MODEL_ID` only after choosing a model.
Give the execution role `dynamodb:PutItem` and `dynamodb:GetItem` on only this table. Add Bedrock permissions only after enabling Bedrock. Avoid logging entire Lex events.

## 4. Lex V2
Create bot `ITServiceDeskAssistant`, select a suitable IAM role and locale (for example, `en_US` if supported). Create intents/slots from `lex-intents.md`. Associate the Lambda with the bot alias, enable fulfillment code hooks, build the locale, and test each utterance. See https://docs.aws.amazon.com/lexv2/latest/dg/lambda.html

## 5. Bedrock
Select a model available in the chosen Region and complete required access steps. Test in the playground. Set `BEDROCK_ENABLED=true` and `BEDROCK_MODEL_ID` to the exact supported model or inference profile ID. Grant least-privilege `bedrock:InvokeModel` for the selected model. The starter is not RAG-grounded; for company-specific answers, add a Bedrock Knowledge Base and approved docs.

## 6. Connect
Create/select an instance, configure a test number, queue, routing profile, and agent. Add the Lex V2 bot alias to the Connect instance. Create the inbound contact flow from `connect-flow.md`, publish it, and associate it with the test number. Test both agent transfer and error branches.

## 7. Clean up
Remove unused test numbers/Connect resources and the Lambda, Lex, DynamoDB, log groups, and IAM resources created only for this demo. Check Billing for remaining resources.
