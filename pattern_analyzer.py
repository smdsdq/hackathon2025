import uuid
import json
from datetime import datetime
from typing import List, Dict, Any
from openai_client import OpenAIClient

class PatternAnalyzer:
    """Analyzes patterns in threats and decoy interactions using Azure OpenAI."""
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.patterns = []

    def analyze_patterns(self, threats: List[Dict[str, Any]], alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies patterns in threat and alert data using Azure OpenAI."""
        prompt = f"""
        You are an AI specializing in pattern analysis for cybersecurity. Analyze the following threats and alerts:
        Threats: {json.dumps(threats[:3], indent=2)}
        Alerts: {json.dumps(alerts[:3], indent=2)}
        Identify common patterns (e.g., frequent source IPs, repeated event types, or correlated timings).
        Return a JSON object with keys: id, timestamp, details, common_sources.
        """
        response = self.openai_client.send_prompt(prompt, max_tokens=100, temperature=0.5)
        if "error" in response:
            print(f"Error in pattern analysis: {response['error']}")
            pattern = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.datetime.now().isoformat(),
                "details": "Fallback pattern due to API failure",
                "common_sources": []
            }
        else:
            response_data = response.get("response", {})
            if not isinstance(response_data, dict):
                print(f"Unexpected response type: {type(response_data)}")
                pattern = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "details": "Fallback pattern due to unexpected response",
                    "common_sources": []
                }
            else:
                pattern = response_data.get("pattern", {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "details": f"Found {len(threats)} threats and {len(alerts)} alerts",
                    "common_sources": [t.get("source_ip", "unknown") for t in threats[:3]]
                })
        self.patterns.append(pattern)
        return self.patterns