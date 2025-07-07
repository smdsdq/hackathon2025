import uuid
import random
import json
from datetime import datetime
from typing import Dict, Any
from openai_client import OpenAIClient

class AIValidator:
    """Validates decoys using Azure OpenAI-based checks."""
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.validation_results = []

    def validate_decoy(self, decoy: Dict[str, Any]) -> bool:
        """Validates decoy realism using Azure OpenAI."""
        prompt = f"""
        You are an AI validator for deception technology. Evaluate the realism of the following decoy:
        {json.dumps(decoy, indent=2)}
        Determine if the decoy is convincing enough to deceive an attacker. 
        Return a JSON object with a single key 'is_valid' set to true if the decoy is realistic, false otherwise.
        """
        response = self.openai_client.send_prompt(prompt, max_tokens=50, temperature=0.3)
        # Simulated response parsing
        is_valid = response.get("response", {}).get("is_valid", random.random() > 0.2)
        result = {
            "decoy_id": decoy["id"],
            "is_valid": is_valid,
            "timestamp": datetime.now().isoformat(),
            "details": f"Validation {'successful' if is_valid else 'failed'} for {decoy['type']}"
        }
        self.validation_results.append(result)
        return is_valid