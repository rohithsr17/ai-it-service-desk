import os, sys, unittest
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))
import ticket_store

class TicketStoreTests(unittest.TestCase):
    @patch.dict(os.environ, {"TICKET_TABLE": ""})
    def test_create_ticket_without_aws(self):
        t = ticket_store.create_ticket("VPN", "Can't connect", "High")
        self.assertTrue(t["ticket_id"].startswith("IT-"))
        self.assertEqual(t["priority"], "High")
        self.assertEqual(t["status"], "Open")

    @patch.dict(os.environ, {"TICKET_TABLE": ""})
    def test_invalid_priority_defaults(self):
        self.assertEqual(ticket_store.create_ticket("VPN", "test", "Critical")["priority"], "Medium")

    def test_empty_ticket_id(self):
        self.assertIsNone(ticket_store.get_ticket(""))

if __name__ == "__main__":
    unittest.main()
