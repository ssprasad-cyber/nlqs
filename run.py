# run.py
"""
Entrypoint script to run the FastAPI application using Uvicorn.

Loads environment variables from a .env file and starts the server.
"""

import uvicorn
from dotenv import load_dotenv, find_dotenv
import logging

# Load .env file if available
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logging.warning(".env file not found. Proceeding without loading environment variables.")

if __name__ == "__main__":
    # Run the app with auto-reload enabled for development convenience
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production for performance and stability
        log_level="info",
    )
