import os, sys, unittest
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))
import app

def slot(value):
    return {"value": {"interpretedValue": value, "originalValue": value}}

def event(name, slots=None, transcript=""):
    return {"invocationSource": "FulfillmentCodeHook", "inputTranscript": transcript,
            "sessionState": {"sessionAttributes": {},
            "intent": {"name": name, "state": "ReadyForFulfillment", "slots": slots or {}}}}

class AppTests(unittest.TestCase):
    def test_vpn_intent(self):
        r = app.lambda_handler(event("VPNTroubleshootingIntent"), None)
        self.assertIn("VPN troubleshooting", r["messages"][0]["content"])
        self.assertEqual(r["sessionState"]["dialogAction"]["type"], "Close")

    @patch("app.answer_it_question", return_value="Use the approved VPN client.")
    def test_knowledge_intent(self, mocked):
        r = app.lambda_handler(event("KnowledgeQuestionIntent", {"Question": slot("How do I connect?")}), None)
        self.assertIn("approved VPN client", r["messages"][0]["content"])
        mocked.assert_called_once()

    @patch("app.create_ticket", return_value={"ticket_id":"IT-AB12CD34","category":"VPN","priority":"High"})
    def test_create_ticket(self, mocked):
        slots = {"Category":slot("VPN"),"Description":slot("VPN is down"),"Priority":slot("High")}
        r = app.lambda_handler(event("CreateTicketIntent", slots), None)
        self.assertIn("IT-AB12CD34", r["messages"][0]["content"])
        mocked.assert_called_once()

    @patch("app.get_ticket", return_value={"ticket_id":"IT-AB12CD34","status":"Open","category":"VPN","priority":"High"})
    def test_check_ticket(self, mocked):
        r = app.lambda_handler(event("CheckTicketIntent", {"TicketId":slot("IT-AB12CD34")}), None)
        self.assertIn("Ticket IT-AB12CD34 is Open", r["messages"][0]["content"])

    def test_fallback(self):
        r = app.lambda_handler(event("FallbackIntent"), None)
        self.assertIn("IT Service Desk Assistant", r["messages"][0]["content"])

    def test_dialog_hook_delegates(self):
        e = event("VPNTroubleshootingIntent")
        e["invocationSource"] = "DialogCodeHook"
        self.assertEqual(app.lambda_handler(e, None)["sessionState"]["dialogAction"]["type"], "Delegate")

if __name__ == "__main__":
    unittest.main()
