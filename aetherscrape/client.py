from typing import Type, TypeVar, Optional, List
from pydantic import BaseModel
from aetherscrape.engine.fetcher import SmartFetcher
from aetherscrape.intelligence.extractor import SemanticExtractor
from aetherscrape.crawler.manager import Crawler, ProxyManager

T = TypeVar("T", bound=BaseModel)

class AetherScrape:
    """The main client for the AetherScrape framework."""
    
    def __init__(self, api_key: Optional[str] = None, max_concurrent: int = 5, proxies: Optional[List[str]] = None):
        self.fetcher = SmartFetcher()
        self.extractor = SemanticExtractor(api_key=api_key)
        self.proxy_manager = ProxyManager(proxies) if proxies else None
        self.max_concurrent = max_concurrent

    async def scrape(self, url: str, schema: Type[T], description: str = "", strategy: str = "smart", **kwargs) -> T:
        """
        Performs an intelligent scrape of a single URL.
        
        Args:
            url: The target URL
            schema: Pydantic model for structured data
            description: Context for the LLM
            strategy: 'static', 'dynamic', or 'smart'
            **kwargs: Additional args for fetcher (e.g., turbo=True)
        """
        # Fetch raw content
        proxy = self.proxy_manager.get_proxy() if self.proxy_manager else None
        html = await self.fetcher.fetch(url, strategy=strategy, proxy=proxy, **kwargs)
        
        # Extract structured data
        tier = "fast" if kwargs.get("turbo") else "quality"
        return await self.extractor.extract(html, schema, description, tier=tier)

    async def crawl(self, urls: List[str], schema: Type[T], description: str = "", **kwargs):
        """Performs a concurrent crawl of multiple URLs."""
        crawler = Crawler(self, max_concurrent=self.max_concurrent)
        for url in urls:
            crawler.add_task(url, schema, description, **kwargs)
        return await crawler.run()
