import csv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from data_analyzer import DataAnalyzer
from openai_client import OpenAIClient
import uvicorn

class EventData(BaseModel):
    """Pydantic model for incoming JSON event data."""
    events: List[Dict[str, Any]]

class APIServer:
    """API server to accept JSON data, write to CSV, and call DataAnalyzer."""
    def __init__(self, openai_client: OpenAIClient, host: str = "0.0.0.0", port: int = 8000):
        self.app = FastAPI()
        self.data_analyzer = DataAnalyzer(openai_client)
        self.host = host
        self.port = port
        self.csv_file = "event_data.csv"
        
        # Define API endpoint
        @self.app.post("/events")
        async def receive_events(data: EventData):
            """Endpoint to receive JSON events, write to CSV, and analyze."""
            try:
                # Write to CSV
                self._write_to_csv(data.events)
                # Analyze data
                threats = self.data_analyzer.analyze_data(data.events)
                return {"status": "success", "threats_found": len(threats), "threats": threats}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing events: {str(e)}")

    def _write_to_csv(self, events: List[Dict[str, Any]]) -> None:
        """Writes JSON events to a CSV file."""
        if not events:
            return
        
        # Define CSV headers based on the first event's keys
        headers = list(events[0].keys())
        file_exists = os.path.isfile(self.csv_file)
        
        with open(self.csv_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            for event in events:
                writer.writerow(event)

    def start(self):
        """Starts the FastAPI server."""
        uvicorn.run(self.app, host=self.host, port=self.port)