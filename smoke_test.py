import asyncio
from aetherscrape.engine.fetcher import SmartFetcher
from loguru import logger

async def smoke_test():
    fetcher = SmartFetcher()
    
    # Test 1: Static Fetch (Fast)
    url1 = "https://www.wikipedia.org"
    logger.info(f"Testing Static Fetcher on {url1}...")
    html_static = await fetcher.fetch(url1, strategy="static")
    print(f"Static fetch successful! Title: {html_static[html_static.find('<title>')+7:html_static.find('</title>')]}")
    print(f"Content length: {len(html_static)} bytes")
    
    # Test 2: Dynamic Fetch (Playwright + Stealth)
    url2 = "https://httpbin.org/headers"
    logger.info(f"Testing Dynamic Fetcher on {url2}...")
    # This will use Playwright and show the headers we are sending
    html_dynamic = await fetcher.fetch(url2, strategy="dynamic")
    print("\nDynamic fetch (with stealth) headers seen by server:")
    print(html_dynamic) # This will be JSON-in-HTML on httpbin
    
    print("\n--- Smoke Test Complete ---")

if __name__ == "__main__":
    asyncio.run(smoke_test())
