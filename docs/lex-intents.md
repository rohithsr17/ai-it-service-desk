# Lex V2 intents

Use these exact names; the Lambda dispatches by intent name. Enable fulfillment hooks for backend-backed intents and rebuild the locale after changes.

## VPNTroubleshootingIntent
Utterances: “My VPN is not connecting”; “I cannot connect to VPN”; “VPN keeps disconnecting”; “Help me troubleshoot VPN”.

## OutlookTroubleshootingIntent
Utterances: “Outlook keeps crashing”; “Outlook is not opening”; “I cannot send emails”; “Outlook is not syncing”.

## AccountAccessIntent
Utterances: “I am locked out of my account”; “I cannot sign in”; “My corporate account is blocked”.
Never collect passwords, MFA codes, or recovery keys.

## SoftwareInstallIntent
Utterances: “I need to install software”; “How do I request an application”; “I cannot find an app in the software portal”.

## KnowledgeQuestionIntent
Utterances: “How do I connect to VPN”; “What should I do if Outlook is not syncing”; “I have an IT question”.
Create optional text slot `Question` if supported by the selected locale. The handler falls back to `inputTranscript`.

## CreateTicketIntent
Utterances: “Create a support ticket”; “I want to raise an IT ticket”; “Log an IT issue”.
Slots: `Category` (custom values: VPN, Outlook, Account Access, Software Installation, General IT); `Description` (free-form text slot where supported); `Priority` (custom values Low, Medium, High). Prompt for required slots.

## CheckTicketIntent
Utterances: “Check my ticket”; “What is the status of my ticket”; “Look up ticket IT-AB12CD34”.
Slot: `TicketId` (alpha-numeric or suitable custom type). Do not expose real ticket details until caller authentication and authorization are implemented.

## FallbackIntent
Use the built-in fallback intent. Give a short supported-task list and offer human escalation.

AWS references:
- https://docs.aws.amazon.com/lexv2/latest/dg/lambda-input-format.html
- https://docs.aws.amazon.com/lexv2/latest/dg/lambda.html
