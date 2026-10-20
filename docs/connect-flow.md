# Amazon Connect contact flow

Create an inbound contact flow named `IT Service Desk - Inbound`.

## Suggested block sequence
1. Entry point.
2. Set logging behavior for the test environment.
3. Optional Set contact attributes: `projectName=AI-IT-Service-Desk`.
4. Get customer input: select the Lex V2 bot and alias; prompt: “Welcome to the IT Service Desk Assistant. Briefly describe your IT issue.”
5. Branch according to the Lex intent and its response. Use self-service completion for resolved cases.
6. Optional Check hours of operation.
7. Set working queue for unresolved cases.
8. Transfer to queue.
9. Disconnect only after the self-service task is complete or the caller confirms.
10. Add Error branches for Lex/Lambda failures; play a short apology and route to a human or alternate support path.

The main Lambda is called by Lex as a code hook; a separate Connect Lambda block is not needed for the basic design. If one is added later, create a Connect-specific adapter because its event payload differs from Lex's.

## Setup checklist
- Add the Lex V2 bot alias to the Connect instance.
- Configure a test number, queue, routing profile, agent, and hours of operation.
- Associate the published flow with the inbound number.
- Test self-service, fallback, transfer, and failure paths.
- Do not share a public-facing number until privacy, authentication, retention, and escalation are reviewed.

AWS references:
- https://docs.aws.amazon.com/connect/latest/adminguide/amazon-lex.html
- https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html
