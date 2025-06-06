# app/main.py

from fastapi import FastAPI
from app.routes import query
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="Natural Language Query System (NLQS)",
    version="0.1.0"
)

# Register routes
app.include_router(query.router, prefix="/api")
