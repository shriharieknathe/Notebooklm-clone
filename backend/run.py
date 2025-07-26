#!/usr/bin/env python3
"""
Run script for the PDF Chat Backend
"""

import uvicorn
from main import app
from config import Config

if __name__ == "__main__":
    print("Starting PDF Chat Backend...")
    print(f"Server will run on http://{Config.HOST}:{Config.PORT}")
    print(f"API documentation available at http://{Config.HOST}:{Config.PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info"
    ) 