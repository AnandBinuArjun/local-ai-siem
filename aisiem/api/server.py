from fastapi import FastAPI, Depends
from aisiem.storage.db import db_instance
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    db_instance.init_db()
    yield
    # Shutdown

app = FastAPI(title="Local AI SIEM", version="0.1.0", lifespan=lifespan)

from aisiem.api.routes import chat
app.include_router(chat.router)

@app.get("/status")
def get_status():
    return {"status": "running", "version": "0.1.0"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Local AI SIEM"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("aisiem.api.server:app", host="0.0.0.0", port=8000, reload=True)
