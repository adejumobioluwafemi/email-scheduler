import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Email Scheduler Service",
    description="Standalone microserviice for scheduling and managing bulk email campaigns",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # in production, restrict to your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "Email Scheduler API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

async def startup_event():
    print("Email Scheduler Service started successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)