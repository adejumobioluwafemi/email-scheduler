import os
import uuid
import json
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Email Scheduler Service",
    description = "Standalone service for scheduling and sending bulk emails",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # in production, this would be restricted to my streamlit url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try: 
        db.init_db()
        logger.info("Scheduler service started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler service: {e}")
        raise

@app.get("/")
async def root():
    return {
        "service": "Email scheduler",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


