# Test plan

## Unit tests
```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## Lambda console event: VPN
```json
{
  "messageVersion": "1.0",
  "invocationSource": "FulfillmentCodeHook",
  "inputMode": "Text",
  "inputTranscript": "My VPN is not connecting",
  "sessionId": "demo-session-1",
  "bot": {"name": "ITServiceDeskAssistant", "localeId": "en_US"},
  "sessionState": {
    "sessionAttributes": {},
    "intent": {"name": "VPNTroubleshootingIntent", "state": "ReadyForFulfillment", "slots": {}}
  }
}
```
Expected: numbered VPN guidance and `dialogAction.type=Close`.

## Acceptance matrix
| Scenario | Expected |
|---|---|
| VPN | Safe troubleshooting steps |
| Outlook | Outlook troubleshooting |
| Account locked | Approved reset route; no secrets requested |
| Software install | Approved portal/approval guidance |
| Knowledge with Bedrock disabled | Safe disabled message |
| Knowledge with Bedrock enabled | Concise generated answer |
| Create ticket | Demo ID and Open status |
| Check ticket | Status only from demo table |
| Unknown intent | Fallback/help response |
| Bedrock error | Graceful escalation message |
| Connect transfer | Routes to configured queue |

Check CloudWatch errors/duration, DynamoDB records, Connect contact flow logs, and Bedrock permissions.
