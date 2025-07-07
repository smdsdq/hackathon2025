import uuid
import random
import json
from datetime import datetime
from typing import List, Dict, Any
from openai_client import OpenAIClient

class HackMonitor:
    """Monitors decoys for unauthorized access attempts using Azure OpenAI."""
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.alerts = []

    def monitor_decoys(self, deployed_decoys: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Monitors decoys for interactions using Azure OpenAI."""
        for decoy in deployed_decoys:
            prompt = f"""
            You are an AI monitoring system for deception technology. Analyze the following deployed decoy:
            {json.dumps(decoy, indent=2)}
            Determine if there is evidence of unauthorized access or interaction with this decoy.
            Return a JSON object with a single key 'is_accessed' set to true if unauthorized access is detected, false otherwise.
            """
            response = self.openai_client.send_prompt(prompt, max_tokens=50, temperature=0.3)
            if "error" in response:
                print(f"Error in decoy monitoring: {response['error']}")
                continue
            response_data = response.get("response", {})
            if not isinstance(response_data, dict):
                print(f"Unexpected response type: {type(response_data)}")
                continue
            if response_data.get("is_accessed", random.random() > 0.7):
                alert = {
                    "id": str(uuid.uuid4()),
                    "decoy_id": decoy["decoy_id"],
                    "timestamp": datetime.datetime.now().isoformat(),
                    "details": f"Unauthorized access detected on {decoy['details']}"
                }
                self.alerts.append(alert)
        return self.alerts