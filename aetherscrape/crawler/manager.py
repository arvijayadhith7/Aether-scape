import asyncio
from typing import List, Callable, Optional, Dict, Any, Type, TypeVar
from loguru import logger
from pydantic import BaseModel
from aetherscrape.engine.fetcher import SmartFetcher
from aetherscrape.intelligence.extractor import SemanticExtractor

T = TypeVar("T", bound=BaseModel)

class ProxyManager:
    """Simple proxy rotation manager."""
    def __init__(self, proxies: List[str]):
        self.proxies = proxies
        self._index = 0

    def get_next(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._index]
        self._index = (self._index + 1) % len(self.proxies)
        return proxy

class Crawler:
    """Orchestrates multi-page scraping tasks."""
    
    def __init__(
        self, 
        max_concurrent: int = 3,
        proxies: Optional[List[str]] = None,
        strategy: str = "smart"
    ):
        self.max_concurrent = max_concurrent
        self.proxy_manager = ProxyManager(proxies or [])
        self.fetcher = SmartFetcher()
        self.extractor = SemanticExtractor()
        self.strategy = strategy
        self.visited = set()

    async def crawl(
        self, 
        urls: List[str], 
        schema: Type[T],
        description: str = "",
        callback: Optional[Callable[[T], Any]] = None
    ) -> List[T]:
        """Crawls a list of URLs and extracts data matching the schema."""
        results = []
        queue = asyncio.Queue()
        for url in urls:
            await queue.put(url)

        async def worker():
            while not queue.empty():
                url = await queue.get()
                if url in self.visited:
                    queue.task_done()
                    continue
                
                self.visited.add(url)
                proxy = self.proxy_manager.get_next()
                
                try:
                    html = await self.fetcher.fetch(url, strategy=self.strategy, proxy=proxy)
                    data = await self.extractor.extract(html, schema, description)
                    results.append(data)
                    
                    if callback:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(data)
                        else:
                            callback(data)
                            
                except Exception as e:
                    logger.error(f"Failed to process {url}: {e}")
                finally:
                    queue.task_done()
                    # Add a small delay between tasks to be polite/stealthy
                    await asyncio.sleep(1.0)

        # Launch workers
        num_workers = min(self.max_concurrent, len(urls))
        tasks = [asyncio.create_task(worker()) for _ in range(num_workers)]
        
        await queue.join()
        
        # Stop workers (in case of long running, though queue.join handles it)
        for t in tasks:
            t.cancel()
            
        return results
