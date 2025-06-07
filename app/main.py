# app/main.py
"""
Main FastAPI application entry point for the Natural Language Query System (NLQS).
Loads environment variables and registers API routes.
"""

from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import logging
from app.routes import query
# Adjusted import to match your router location

# Attempt to load environment variables from a .env file
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logging.warning(".env file not found. Environment variables may be missing.")


 

app = FastAPI(
    title="Natural Language Query System (NLQS)",
    version="0.1.0",
    description="API backend for querying structured data using natural language.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register API routes with a prefix for versioning or grouping
app.include_router(query.router, prefix="/api")

# Optional: add a simple health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}
