import time
import json
from aisiem.ingest.windows import collect_windows_events
from aisiem.normalize.router import normalize_event
from aisiem.storage.db import db_instance, EventModel
from aisiem.storage.models import Event

from aisiem.ai.embedder import embedder_instance
from aisiem.ai.vector_index import vector_index
import uuid

def save_event(event: Event, db):
    # Simple de-duplication based on raw content (not efficient for prod but good for MVP)
    # In reality, use a unique ID from the source (e.g. EventRecordID)
    # For now, we just insert.
    db_event = EventModel(
        ts=event.ts,
        host=event.host,
        source=event.source,
        category=event.category,
        subtype=event.subtype,
        severity=event.severity,
        principal=event.principal,
        object=event.object,
        fields=event.fields,
        raw=event.raw
    )
    db.add(db_event)
    db.commit()
    
    # --- AI Enrichment ---
    # Generate embedding
    try:
        text_rep = embedder_instance.event_to_text(event)
        embedding = embedder_instance.embed_text([text_rep])[0]
        
        # Store in Vector DB
        vector_index.add_events(
            ids=[str(db_event.id)], # Use DB ID
            embeddings=[embedding],
            metadatas=[{"source": event.source, "category": event.category}],
            documents=[text_rep]
        )
    except Exception as e:
        print(f"Embedding failed: {e}")

def run_ingestion():
    db_instance.init_db()
    db = next(db_instance.get_db())
    
    print("Starting ingestion loop (Ctrl+C to stop)...")
    try:
        while True:
            print("Collecting batch...")
            count = 0
            for raw_log in collect_windows_events(max_events=5):
                event = normalize_event(raw_log)
                save_event(event, db)
                count += 1
            print(f"Ingested {count} events.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping ingestion.")
    finally:
        db.close()

if __name__ == "__main__":
    run_ingestion()
