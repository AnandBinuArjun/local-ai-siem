from aisiem.storage.models import RawLog, Event
from aisiem.normalize.windows_parsers import parse_windows_event

def normalize_event(raw_log: RawLog) -> Event:
    if raw_log.source.startswith("win.eventlog"):
        return parse_windows_event(raw_log)
    
    # Fallback for unknown sources
    return Event(
        ts=raw_log.ingest_ts,
        host=raw_log.host,
        source=raw_log.source,
        category="unknown",
        subtype="unknown",
        severity=0,
        raw=raw_log.raw
    )
