import uuid
import random
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

class DataGatherer:
    """Collects network and system data from an external API."""
    def __init__(self, api_endpoint: str = "https://example.com/api"):
        self.api_endpoint = api_endpoint
        self.data = []

    def fetch_data(self) -> List[Dict[str, Any]]:
        """Fetches JSON data from an external API."""
        try:
            # Simulate API call with mock JSON response
            mock_response = [
                {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source_ip": f"192.168.1.{random.randint(1, 255)}",
                    "destination_ip": f"192.168.1.{random.randint(1, 255)}",
                    "port": random.randint(1, 65535),
                    "protocol": random.choice(["TCP", "UDP", "HTTP"]),
                    "event": random.choice(["login_attempt", "file_access", "process_start"]),
                    "user": f"user_{random.randint(1, 100)}",
                    "status": random.choice(["success", "failed"])
                } for _ in range(random.randint(1, 5))
            ]
            self.data.extend(mock_response)
            return self.data
        except requests.RequestException as e:
            return [{"error": f"API fetch failed: {str(e)}"}]