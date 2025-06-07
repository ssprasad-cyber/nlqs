# app/api/routes.py
"""
API router for handling natural language queries via POST /query endpoint.

Receives a JSON payload with a question string, processes it via the NLQS
handle_query function, and returns structured results or error responses.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, constr
from app.core.orchestrator import handle_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: constr(min_length=1, strip_whitespace=True) = Field(
        ..., description="Natural language question to be processed"
    )

class QueryResponse(BaseModel):
    result: dict | str

@router.post("/query", response_model=QueryResponse, summary="Process natural language query")
async def query_nlqs(req: QueryRequest):
    """
    Endpoint to accept a natural language question and return the query results.

    Args:
        req (QueryRequest): Request body containing the question string.

    Returns:
        QueryResponse: Response containing result data or error details.

    Raises:
        HTTPException 500 if internal processing fails.
    """
    try:
        response = await handle_query(req.question)
        return QueryResponse(result=response)
    except Exception as e:
        # Log error details here if you have logging configured
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
