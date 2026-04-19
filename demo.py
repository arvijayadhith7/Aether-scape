import asyncio
from typing import List
from pydantic import BaseModel, Field
from aetherscrape.client import AetherScrape
from loguru import logger
import os

# 1. Define your data schema
class Product(BaseModel):
    name: str = Field(description="The name of the product")
    price: str = Field(description="The price, including currency")
    availability: str = Field(description="Stock status (e.g., In Stock, Out of Stock)")
    features: List[str] = Field(description="A list of key features of the product")

async def main():
    # 2. Initialize the client
    # You'll need to set your GOOGLE_API_KEY in the environment or .env file
    scraper = AetherScrape(
        api_key=os.getenv("GOOGLE_API_KEY"),
        max_concurrent=2
    )

    # Example URL (Replace with a real site you want to scrape)
    url = "https://example-ecommerce-site.com/products/item-123"
    
    logger.info("Starting intelligent scrape...")
    
    try:
        # 3. Perform a smart scrape
        # The library will try static first, then dynamic if blocked.
        # It uses an LLM to find the data regardless of layout changes.
        product_data = await scraper.scrape(
            url=url,
            schema=Product,
            description="Extract product details from a modern e-commerce page."
        )
        
        print("\n--- Extracted Data ---")
        print(product_data.model_dump_json(indent=2))
        print("----------------------\n")
        
    except Exception as e:
        logger.error(f"Scrape failed: {e}")
        print("\nNote: This demo requires a real URL and a GOOGLE_API_KEY to function.")

if __name__ == "__main__":
    asyncio.run(main())
