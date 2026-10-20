"""DynamoDB demo ticket persistence."""
import os
import uuid
from datetime import datetime, timezone

def _table():
    name = os.getenv("TICKET_TABLE", "").strip()
    if not name:
        return None
    import boto3
    return boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION")).Table(name)

def create_ticket(category: str, description: str, priority: str = "Medium") -> dict:
    ticket = {
        "ticket_id": "IT-" + uuid.uuid4().hex[:8].upper(),
        "category": (category or "General IT")[:80],
        "description": (description or "No description provided")[:1000],
        "priority": priority if priority in {"Low", "Medium", "High"} else "Medium",
        "status": "Open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    table = _table()
    if table:
        table.put_item(Item=ticket)
    return ticket

def get_ticket(ticket_id: str):
    if not ticket_id:
        return None
    table = _table()
    if not table:
        return None
    return table.get_item(Key={"ticket_id": ticket_id.strip()}).get("Item")

