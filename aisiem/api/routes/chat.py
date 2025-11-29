from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from aisiem.ai.embedder import embedder_instance
from aisiem.ai.vector_index import vector_index
from aisiem.ai.incident_summarizer import summarizer
from aisiem.storage.models import Incident
# Mock DB access for chat
from aisiem.storage.db import db_instance

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    context: list

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # 1. Intent Classification (Simple keyword based for MVP)
    query = request.query.lower()
    
    context = []
    response_text = ""

    if "search" in query or "show" in query:
        # Vector Search
        embedding = embedder_instance.embed_text([request.query])[0]
        results = vector_index.search(embedding, n_results=3)
        
        # Format results
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        
        context_str = "\n".join([f"Event: {d}" for d in docs])
        
        # Ask LLM to explain
        # We reuse the summarizer client for generic chat
        prompt = f"User asked: '{request.query}'.\n\nFound these events:\n{context_str}\n\nAnswer the user's question based on these events."
        
        try:
            llm_resp = summarizer.client.chat.completions.create(
                model="llama3",
                messages=[
                    {"role": "system", "content": "You are a helpful SOC Assistant. Answer based on the provided logs."},
                    {"role": "user", "content": prompt}
                ]
            )
            response_text = llm_resp.choices[0].message.content
            context = docs
        except Exception as e:
            response_text = f"Error querying LLM: {e}"
            
    else:
        response_text = "I can help you search logs. Try asking 'Show me suspicious login attempts'."

    return ChatResponse(response=response_text, context=context)
