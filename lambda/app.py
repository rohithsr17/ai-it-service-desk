"""Lex V2 fulfillment handler for the AI IT Service Desk demo."""
import logging
from bedrock_helper import answer_it_question
from ticket_store import create_ticket, get_ticket

logger = logging.getLogger()
logger.setLevel(logging.INFO)

KNOWN_ISSUES = {
    "VPNTroubleshootingIntent": ("VPN", [
        "Confirm your internet connection is working.",
        "Disconnect and reconnect the approved VPN client.",
        "Check for an authentication or certificate error.",
        "If the issue continues, record the exact error and request support."
    ]),
    "OutlookTroubleshootingIntent": ("Outlook", [
        "Check whether Outlook on the web is accessible.",
        "Restart Outlook and verify network connectivity.",
        "Record any error message and when it started.",
        "If the issue continues, create a support ticket."
    ]),
    "AccountAccessIntent": ("Account Access", [
        "Confirm you are using the correct corporate username.",
        "Use your organization's approved password-reset process.",
        "Never share your password, MFA code, or recovery key with this assistant.",
        "Contact identity support if access remains blocked."
    ]),
    "SoftwareInstallIntent": ("Software Installation", [
        "Check the organization's approved software portal.",
        "Confirm the required license and approvals are available.",
        "If the app is not listed, submit the approved software request."
    ]),
}

def _lex_response(event, message, intent_state="Fulfilled"):
    state = event.get("sessionState") or {}
    intent = state.get("intent") or {"name": "FallbackIntent"}
    intent["state"] = intent_state
    return {
        "sessionState": {
            "sessionAttributes": state.get("sessionAttributes") or {},
            "intent": intent,
            "dialogAction": {"type": "Close"},
        },
        "messages": [{"contentType": "PlainText", "content": str(message)[:3500]}],
    }

def _slot(intent, name):
    slots = (intent or {}).get("slots") or {}
    value = (slots.get(name) or {}).get("value") or {}
    return value.get("interpretedValue") or value.get("originalValue") or ""

def lambda_handler(event, context):
    state = event.get("sessionState") or {}
    intent = state.get("intent") or {}
    name = intent.get("name", "FallbackIntent")
    logger.info("Lex request: intent=%s source=%s", name, event.get("invocationSource"))

    if event.get("invocationSource") == "DialogCodeHook":
        state["dialogAction"] = {"type": "Delegate"}
        return {"sessionState": state}

    if name in KNOWN_ISSUES:
        category, steps = KNOWN_ISSUES[name]
        return _lex_response(event, category + " troubleshooting. " +
                             " ".join(f"Step {i}: {s}" for i, s in enumerate(steps, 1)))

    if name == "KnowledgeQuestionIntent":
        question = _slot(intent, "Question") or (event.get("inputTranscript") or "").strip()
        try:
            answer = answer_it_question(question or "What IT support information do you need?")
        except Exception:
            logger.exception("Bedrock knowledge request failed")
            answer = "I couldn't retrieve a reliable answer. Please create a support ticket or ask for a human agent."
        return _lex_response(event, answer)

    if name == "CreateTicketIntent":
        ticket = create_ticket(
            category=_slot(intent, "Category") or "General IT",
            description=_slot(intent, "Description") or event.get("inputTranscript") or "No description provided",
            priority=_slot(intent, "Priority") or "Medium",
        )
        return _lex_response(event, f"Your demo support ticket {ticket['ticket_id']} has been created. "
                                    f"Category: {ticket['category']}. Priority: {ticket['priority']}.")

    if name == "CheckTicketIntent":
        ticket_id = _slot(intent, "TicketId")
        ticket = get_ticket(ticket_id)
        if not ticket:
            return _lex_response(event, "I couldn't find that ticket in the demo system. Please check the ID.")
        return _lex_response(event, f"Ticket {ticket['ticket_id']} is {ticket['status']}. "
                                    f"Category: {ticket['category']}. Priority: {ticket['priority']}.")

    return _lex_response(event, "I'm the IT Service Desk Assistant. I can help with VPN, Outlook, account access, "
                                "software installation, knowledge questions, or demo ticket creation.")

