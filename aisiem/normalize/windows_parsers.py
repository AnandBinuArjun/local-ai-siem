import json
from aisiem.storage.models import RawLog, Event

def parse_windows_event(raw_log: RawLog) -> Event:
    data = json.loads(raw_log.raw)
    
    # Basic mapping - this depends heavily on the specific event ID and structure
    # PowerShell ConvertTo-Json structure varies, but usually has 'Id', 'TimeCreated', 'Message', etc.
    
    event_id = data.get('Id', 0)
    message = data.get('Message', '')
    
    # Determine category/subtype based on Event ID (Simplified)
    category = "generic"
    subtype = "info"
    severity = 1
    
    if raw_log.source.endswith("security"):
        category = "auth"
        if event_id == 4624:
            subtype = "login_success"
            severity = 1
        elif event_id == 4625:
            subtype = "login_failure"
            severity = 5
    elif raw_log.source.endswith("application"):
        category = "app"
    
    # Extract timestamp
    # TimeCreated might be a dict or string depending on PS version
    # For now, use ingest_ts if parsing fails
    ts = raw_log.ingest_ts
    
    return Event(
        ts=ts,
        host=raw_log.host,
        source=raw_log.source,
        category=category,
        subtype=subtype,
        severity=severity,
        principal=str(data.get('UserId', 'unknown')),
        object=str(event_id),
        fields={"event_id": event_id, "message": message[:100]}, # Truncate message for demo
        raw=raw_log.raw
    )
