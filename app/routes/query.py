from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.orchestrator import handle_query
from typing import Optional

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    source: Optional[str] = None

class QueryResponse(BaseModel):
    result: dict

@router.post("/query", response_model=QueryResponse)
async def query_nlqs(req: QueryRequest):
    try:
        response = await handle_query(req.question)
        return QueryResponse(result=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))