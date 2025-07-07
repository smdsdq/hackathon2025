import uuid
import random
from datetime import datetime
from typing import Dict, Any

class Logger:
    """Handles logging and response actions."""
    def __init__(self):
        self.logs = []

    def log_event(self, event: Dict[str, Any]) -> None:
        """Logs events to a file or system."""
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        self.logs.append(log_entry)

    def respond_to_threat(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Responds to a detected threat."""
        response = {
            "alert_id": alert["id"],
            "timestamp": datetime.now().isoformat(),
            "action": random.choice(["block_ip", "alert_admin", "isolate_system"]),
            "details": f"Responded to {alert['details']}"
        }
        self.log_event(response)
        return response