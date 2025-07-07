import json
import asyncio
from data_gatherer import DataGatherer
from data_analyzer import DataAnalyzer
from decoy_generator import DecoyGenerator
from ai_validator import AIValidator
from decoy_implementer import DecoyImplementer
from hack_monitor import HackMonitor
from logger import Logger
from pattern_analyzer import PatternAnalyzer
from openai_client import OpenAIClient
from api_server import APIServer

class DeceptionToolkit:
    """Orchestrates the deception technology components."""
    def __init__(self, api_endpoint: str = "https://example.com/api", 
                 azure_endpoint: str = "https://your-azure-openai-endpoint", 
                 encrypted_api_key: str = "your-encrypted-api-key", 
                 encryption_key: str = "your-encryption-key"):
        self.openai_client = OpenAIClient(azure_endpoint, encrypted_api_key, encryption_key)
        self.data_gatherer = DataGatherer(api_endpoint)
        self.data_analyzer = DataAnalyzer(self.openai_client)
        self.decoy_generator = DecoyGenerator(self.openai_client)
        self.ai_validator = AIValidator(self.openai_client)
        self.decoy_implementer = DecoyImplementer()
        self.hack_monitor = HackMonitor(self.openai_client)
        self.logger = Logger()
        self.pattern_analyzer = PatternAnalyzer(self.openai_client)
        self.api_server = APIServer(self.openai_client)

    async def run(self):
        """Runs the full deception workflow and starts the API server."""
        # Start API server in the background
        loop = asyncio.get_event_loop()
        server_task = loop.run_in_executor(None, self.api_server.start)

        # Existing workflow
        # Step 1: Gather data
        data = self.data_gatherer.fetch_data()
        self.logger.log_event({"step": "data_gathering", "data_count": len(data)})

        # Step 2: Analyze data
        threats = self.data_analyzer.analyze_data(data)
        self.logger.log_event({"step": "analysis", "threats_found": len(threats)})

        # Step 3: Generate and validate decoys
        for threat in threats:
            decoy = self.decoy_generator.generate_decoy(threat)
            if self.ai_validator.validate_decoy(decoy):
                # Step 4: Deploy decoys
                deployment = self.decoy_implementer.deploy_decoy(decoy)
                self.logger.log_event({"step": "deployment", "decoy_id": decoy["id"]})

        # Step 5: Monitor decoys
        alerts = self.hack_monitor.monitor_decoys(self.decoy_implementer.deployed_decoys)
        for alert in alerts:
            response = self.logger.respond_to_threat(alert)
            self.logger.log_event({"step": "response", "action": response["action"]})

        # Step 6: Analyze patterns
        patterns = self.pattern_analyzer.analyze_patterns(threats, alerts)
        self.logger.log_event({"step": "pattern_analysis", "patterns_found": len(patterns)})

        return {"status": "completed", "logs": self.logger.logs}

if __name__ == "__main__":
    toolkit = DeceptionToolkit()
    asyncio.run(toolkit.run())