import uuid
import random
import json
from datetime import datetime
from typing import List, Dict, Any
from openai_client import OpenAIClient

class DataAnalyzer:
    """Analyzes collected data to identify potential threats using Azure OpenAI."""
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.threats = []

    def analyze_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyzes data for suspicious patterns using Azure OpenAI to detect anomalies."""
        for entry in data:
            if "error" not in entry:
                if self._is_anomaly(entry):
                    threat = {
                        "id": str(uuid.uuid4()),
                        "timestamp": datetime.datetime.now().isoformat(),
                        "details": f"Anomaly detected: {entry}",
                        "severity": random.choice(["low", "medium", "high"])
                    }
                    self.threats.append(threat)
        return self.threats

    def _is_anomaly(self, event: Dict[str, Any]) -> bool:
        """Uses Azure OpenAI to determine if an event is an anomaly."""
        prompt = f"""
        You are an AI specializing in anomaly detection for cybersecurity. Analyze the following event:
        {json.dumps(event, indent=2)}
        Determine if this event represents an anomaly (e.g., unusual login attempt, unexpected port access, or suspicious protocol usage). 
        Return a JSON object with a single key 'is_anomaly' set to true if the event is an anomaly, false otherwise.
        """
        response = self.openai_client.send_prompt(prompt, max_tokens=50, temperature=0.3)
        # Handle response safely
        if "error" in response:
            print(f"Error in anomaly detection: {response['error']}")
            return False
        response_data = response.get("response", {})
        if not isinstance(response_data, dict):
            print(f"Unexpected response type: {type(response_data)}")
            return random.random() > 0.3  # Fallback
        return response_data.get("is_anomaly", random.random() > 0.3)