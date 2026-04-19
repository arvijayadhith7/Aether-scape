import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from aetherscrape.client import AetherScrape
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define the specific schema requested by the user
class ConfigItem(BaseModel):
    name: str = Field(description="The name of the feature or configuration item")
    description: str = Field(description="The description of what this feature does")
    options: Optional[List[str]] = Field(default=None, description="Any specific options or examples associated with this item")

class PageConfig(BaseModel):
    configuration: List[ConfigItem] = Field(description="A list of high-level configuration items or features found on the page")

async def main():
    # 2. Initialize the client (using NVIDIA NIM)
    scraper = AetherScrape(
        max_concurrent=1
    )

    url = "https://www.gitreverse.com/"
    
    logger.info(f"Extracting page configuration from {url}...")
    
    try:
        # 3. Perform a smart scrape
        # We ask for a high-level configuration audit of the landing page
        config_data = await scraper.scrape(
            url=url,
            schema=PageConfig,
            description="Audit the landing page and extract the main features and configuration options into a structured list.",
            strategy="dynamic"
        )
        
        print("\n--- Extracted Page Configuration ---")
        import json
        print(config_data.model_dump_json(indent=2))
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
