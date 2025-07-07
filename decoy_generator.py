import uuid
import random
import json
from datetime import datetime
from typing import Dict, Any
from openai_client import OpenAIClient

class DecoyGenerator:
    """Generates decoy assets to mislead attackers using Azure OpenAI."""
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.decoys = []

    def generate_decoy(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a decoy based on threat analysis using Azure OpenAI."""
        prompt = f"""
        You are an AI specializing in deception technology. Based on the following threat data:
        {json.dumps(threat, indent=2)}
        Generate a realistic decoy to mislead the attacker. The decoy should be contextually relevant to the threat (e.g., fake file, honeypot service, or decoy user). 
        Return a JSON object with keys: id, type, target, details, created_at.
        """
        response = self.openai_client.send_prompt(prompt, max_tokens=100, temperature=0.5)
        # Simulated response parsing
        if "error" in response:
            decoy = {
                "id": str(uuid.uuid4()),
                "type": "fallback_decoy",
                "target": threat.get("source_ip", "unknown"),
                "details": "Fallback decoy due to API failure",
                "created_at": datetime.now().isoformat()
            }
        else:
            decoy_type = random.choice(["fake_file", "honeypot_service", "decoy_user"])
            decoy = {
                "id": str(uuid.uuid4()),
                "type": decoy_type,
                "target": threat.get("source_ip", "unknown"),
                "details": f"Decoy {decoy_type} for {threat.get('details', 'unknown')}",
                "created_at": datetime.now().isoformat()
            }
        self.decoys.append(decoy)
        return decoy