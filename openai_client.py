import json
import os
import requests
from typing import Dict, Any
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
            # Derive a Fernet key from the encryption key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'salt_',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
            fernet = Fernet(key)
            # Decrypt the API key
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
            # Simulated response (replace with actual API call in production)
            # response = requests.post(self.azure_endpoint, headers=self.headers, json=payload)
            # return response.json()
            return {"response": "Simulated response"}  # Placeholder
        except requests.RequestException as e:
            print(f"Azure OpenAI API call failed: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def encrypt_api_key(api_key: str, encryption_key: str) -> str:
        """Encrypts an API key using the provided encryption key."""
        try:
            # Derive a Fernet key from the encryption key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'salt_',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
            fernet = Fernet(key)
            # Encrypt the API key
            encrypted_key = fernet.encrypt(api_key.encode()).decode()
            return encrypted_key
        except Exception as e:
            raise ValueError(f"Failed to encrypt API key: {str(e)}")