from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import json
from aetherscrape.client import AetherScrape
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="AetherScape API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = AetherScrape(
    api_key=os.getenv("NVIDIA_API_KEY"),
)

class ScrapeRequest(BaseModel):
    url: str
    description: str
    turbo: bool = False

@app.post("/scrape")
async def perform_scrape(request: ScrapeRequest):
    logger.info(f"Received scrape request for {request.url} (Turbo: {request.turbo})")
    
    class DynamicResult(BaseModel):
        data: Any = Field(description=f"Extracted data for: {request.description}")

    try:
        result = await scraper.scrape(
            url=request.url,
            schema=DynamicResult,
            description=request.description,
            strategy="smart",
            turbo=request.turbo
        )
        
        # New: Generate summary
        summary = await scraper.extractor.summarize(result.data, tier="fast")
        
        return {
            "status": "success", 
            "data": result.data,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Scrape failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
