from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import asyncio
from curl_cffi import requests as curl_requests
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from loguru import logger
from aetherscrape.utils.stealth import get_random_user_agent, scroll_naturally, human_delay

class BaseFetcher(ABC):
    @abstractmethod
    async def fetch(self, url: str, **kwargs) -> str:
        pass

class StaticFetcher(BaseFetcher):
    """Fetcher using curl_cffi for high-performance TLS impersonation."""
    async def fetch(self, url: str, proxy: Optional[str] = None, **kwargs) -> str:
        logger.info(f"Fetching (Static) {url}")
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        # Impersonate Chrome to bypass basic TLS fingerprinting
        response = curl_requests.get(
            url, 
            impersonate="chrome", 
            proxies=proxies,
            headers={"User-Agent": get_random_user_agent()},
            **kwargs
        )
        return response.text

class DynamicFetcher(BaseFetcher):
    """Fetcher using Playwright for JavaScript-heavy sites with stealth patches."""
    async def fetch(self, url: str, proxy: Optional[str] = None, wait_until: str = "networkidle", **kwargs) -> str:
        turbo = kwargs.get("turbo", False)
        logger.info(f"Fetching (Dynamic{' - TURBO' if turbo else ''}) {url}")
        
        async with async_playwright() as p:
            browser_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
            
            proxy_config = None
            if proxy:
                proxy_config = {"server": proxy}

            browser = await p.chromium.launch(
                headless=True,
                args=browser_args,
                proxy=proxy_config
            )
            
            context = await browser.new_context(
                user_agent=get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            # Stealth is always applied for fingerprinting, but behaviors are toggled
            await Stealth().apply_stealth_async(page)
            
            # Navigate
            await page.goto(url, wait_until=wait_until)
            
            # Turbo Mode skips the slow human simulation
            if not turbo:
                if kwargs.get("simulate_human", True):
                    await human_delay(1.0, 2.0)
                    await scroll_naturally(page)
                    await human_delay(0.5, 1.5)
            else:
                # In Turbo, we might still want to trigger initial lazy loading quickly
                await scroll_naturally(page, fast=True)
            
            content = await page.content()
            await browser.close()
            return content

class SmartFetcher:
    """Orchestrator that chooses the best fetcher for the job."""
    def __init__(self):
        self.static = StaticFetcher()
        self.dynamic = DynamicFetcher()

    async def fetch(self, url: str, strategy: str = "smart", **kwargs) -> str:
        if strategy == "static":
            return await self.static.fetch(url, **kwargs)
        elif strategy == "dynamic":
            return await self.dynamic.fetch(url, **kwargs)
        else:
            # Smart strategy: Try static first
            try:
                content = await self.static.fetch(url, **kwargs)
                # Optimized threshold check
                is_blocked = any(x in content.lower() for x in ["cloudflare", "blocked", "access denied", "captcha"])
                if is_blocked or len(content) < 300:
                    logger.warning("Static fetch might be blocked. Falling back to Dynamic.")
                    return await self.dynamic.fetch(url, **kwargs)
                return content
            except Exception as e:
                logger.error(f"Static fetch failed: {e}. Falling back to Dynamic.")
                return await self.dynamic.fetch(url, **kwargs)
