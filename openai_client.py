import json
import os
import random
import requests
import uuid
from typing import Dict, Any
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class OpenAIClient:
    """Handles Azure OpenAI API authentication and requests with encrypted API key."""
    def __init__(self, azure_endpoint: str = "https://your-azure-openai-endpoint", 
                 encrypted_api_key: str = None, encryption_key: str = None):
        self.azure_endpoint = azure_endpoint
        self.api_key = self._decrypt_api_key(encrypted_api_key, encryption_key)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _decrypt_api_key(self, encrypted_api_key: str, encryption_key: str) -> str:
        """Decrypts the API key using the provided encryption key."""
        if not encrypted_api_key or not encryption_key:
            raise ValueError("Encrypted API key and encryption key must be provided.")
        
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'salt_',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
            fernet = Fernet(key)
            decrypted_key = fernet.decrypt(encrypted_api_key.encode()).decode()
            return decrypted_key
        except Exception as e:
            raise ValueError(f"Failed to decrypt API key: {str(e)}")

    def send_prompt(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> Dict[str, Any]:
        """Sends a prompt to Azure OpenAI and returns the response."""
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            # Simulated response for testing (ensures consistent dictionary format)
            # In production, replace with: response = requests.post(self.azure_endpoint, headers=self.headers, json=payload)
            simulated_response = {
                "response": {
                    "is_anomaly": random.random() > 0.3,  # For DataAnalyzer
                    "is_valid": random.random() > 0.2,    # For AIValidator
                    "is_accessed": random.random() > 0.7, # For HackMonitor
                    "decoy": {                            # For DecoyGenerator
                        "id": str(uuid.uuid4()),
                        "type": random.choice(["fake_file", "honeypot_service", "decoy_user"]),
                        "target": "unknown",
                        "details": "Simulated decoy",
                        "created_at": datetime.datetime.now().isoformat()
                    },
                    "pattern": {                          # For PatternAnalyzer
                        "id": str(uuid.uuid4()),
                        "timestamp": datetime.datetime.now().isoformat(),
                        "details": "Simulated pattern",
                        "common_sources": []
                    }
                }
            }
            return simulated_response
        except requests.RequestException as e:
            print(f"Azure OpenAI API call failed: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def encrypt_api_key(api_key: str, encryption_key: str) -> str:
        """Encrypts an API key using the provided encryption key."""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'salt_',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
            fernet = Fernet(key)
            encrypted_key = fernet.encrypt(api_key.encode()).decode()
            return encrypted_key
        except Exception as e:
            raise ValueError(f"Failed to encrypt API key: {str(e)}")