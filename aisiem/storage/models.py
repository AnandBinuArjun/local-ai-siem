from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class RawLog(BaseModel):
    source: str
    raw: str
    ingest_ts: float = Field(default_factory=lambda: datetime.now().timestamp())
    host: str

class Event(BaseModel):
    ts: float
    host: str
    source: str
    category: str  # auth, process, network, fs, config, app, generic
    subtype: str   # login_success, login_failure, process_start, etc.
    severity: int = Field(ge=0, le=10)
    principal: Optional[str] = None
    object: Optional[str] = None
    fields: Dict[str, Any] = Field(default_factory=dict)
    raw: str

class Detection(BaseModel):
    id: str
    title: str
    severity: int
    ts: float
    host: str
    rule_id: str
    details: Dict[str, Any]

class Incident(BaseModel):
    id: str
    status: str = "open"
    start_ts: float
    end_ts: float
    detections: list[Detection] = []
    entities: Dict[str, list[str]] = {"users": [], "hosts": [], "ips": [], "processes": []}
    tags: list[str] = []
    severity: int
