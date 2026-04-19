import asyncio
from typing import List
from pydantic import BaseModel, Field
from aetherscrape.client import AetherScrape
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define the schema for GitReverse project library
class GitReverseProject(BaseModel):
    name: str = Field(description="The name of the repository or project")
    github_url: str = Field(description="The original GitHub URL for the project")
    prompt_snippet: str = Field(description="A short snippet of the reverse-engineered prompt")

class ProjectLibrary(BaseModel):
    items: List[GitReverseProject] = Field(description="List of projects in the library")

async def main():
    # 2. Initialize the client (will use NVIDIA from .env)
    scraper = AetherScrape(
        max_concurrent=1
    )

    url = "https://www.gitreverse.com/library"
    
    logger.info(f"Starting intelligent scrape of {url} using NVIDIA NIM...")
    
    try:
        # 3. Perform a smart scrape
        # We use 'dynamic' strategy because the library likely loads via JS
        library_data = await scraper.scrape(
            url=url,
            schema=ProjectLibrary,
            description="Extract the list of reverse-engineered repositories from the GitReverse library page.",
            strategy="dynamic"
        )
        
        print("\n--- GitReverse Project Library ---")
        for project in library_data.items:
            print(f"Project: {project.name}")
            print(f"URL:     {project.github_url}")
            print(f"Snippet: {project.prompt_snippet}")
            print("-" * 30)
        
    except Exception as e:
        logger.error(f"Scrape failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
