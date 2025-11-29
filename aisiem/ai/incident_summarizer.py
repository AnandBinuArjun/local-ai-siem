from openai import OpenAI
import os

class IncidentSummarizer:
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama"):
        # Default to Ollama local
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def summarize(self, incident) -> str:
        prompt = self._build_prompt(incident)
        try:
            response = self.client.chat.completions.create(
                model="llama3", # User needs to have this or similar pulled
                messages=[
                    {"role": "system", "content": "You are a Tier 3 SOC Analyst. Summarize the following security incident concisely. Identify the likely attack stage (MITRE ATT&CK) and recommend next steps."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Summarization failed: {e}"

    def _build_prompt(self, incident) -> str:
        detections_str = "\n".join([f"- {d.title} (Severity: {d.severity})" for d in incident.detections])
        return f"""
        Incident ID: {incident.id}
        Duration: {incident.end_ts - incident.start_ts} seconds
        Entities: {incident.entities}
        
        Detections:
        {detections_str}
        
        Please provide a structured summary.
        """

summarizer = IncidentSummarizer()
