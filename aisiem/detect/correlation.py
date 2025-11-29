from typing import List, Dict
from aisiem.storage.models import Event, Incident, Detection
import uuid
import time

class CorrelationEngine:
    def __init__(self):
        self.active_incidents: Dict[str, Incident] = {}
        # Simple in-memory state for MVP. In prod, use Redis or DB.

    def process_detection(self, detection: Detection) -> Incident:
        # 1. Try to find an existing related incident
        # Logic: Same host and principal within 1 hour
        
        related_incident = None
        for inc_id, inc in self.active_incidents.items():
            if inc.status == "open":
                # Check entity overlap
                if detection.host in inc.entities["hosts"] or \
                   (detection.details.get("user") and detection.details.get("user") in inc.entities["users"]):
                    related_incident = inc
                    break
        
        if related_incident:
            # Update existing
            related_incident.detections.append(detection)
            related_incident.end_ts = detection.ts
            if detection.host not in related_incident.entities["hosts"]:
                related_incident.entities["hosts"].append(detection.host)
            # Add other entities...
            return related_incident
        else:
            # Create new
            new_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
            new_inc = Incident(
                id=new_id,
                start_ts=detection.ts,
                end_ts=detection.ts,
                detections=[detection],
                entities={
                    "hosts": [detection.host],
                    "users": [detection.details.get("user")] if detection.details.get("user") else [],
                    "ips": [],
                    "processes": []
                },
                severity=detection.severity,
                tags=[detection.rule_id]
            )
            self.active_incidents[new_id] = new_inc
            return new_inc

correlation_engine = CorrelationEngine()
