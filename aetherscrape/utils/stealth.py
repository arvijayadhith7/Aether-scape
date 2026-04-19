import random
import asyncio
import numpy as np
from loguru import logger

def get_random_user_agent():
    """Returns a realistic modern user agent."""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (AppleScript; AppleScript 1.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    ]
    return random.choice(agents)

async def human_delay(min_sec=1.5, max_sec=4.0):
    """Simulates a human-like thinking/waiting delay."""
    # Use a Gaussian distribution centered slightly towards the lower end for realism
    mu = (min_sec + max_sec) / 2.5
    sigma = (max_sec - min_sec) / 6
    delay = np.random.normal(mu, sigma)
    delay = max(min_sec, min(max_sec, delay))
    logger.debug(f"Simulating human delay: {delay:.2f}s")
    await asyncio.sleep(delay)

async def simulate_mouse_movement(page, start_x, start_y, end_x, end_y, steps=20):
    """Simulates realistic mouse movement using basic linear interpolation with jitter."""
    for i in range(steps + 1):
        t = i / steps
        curr_x = start_x + (end_x - start_x) * t
        curr_y = start_y + (end_y - start_y) * t
        jitter_x = random.uniform(-2, 2)
        jitter_y = random.uniform(-2, 2)
        try:
            await page.mouse.move(curr_x + jitter_x, curr_y + jitter_y)
            await asyncio.sleep(random.uniform(0.01, 0.03))
        except Exception:
            break

async def scroll_naturally(page, fast=False):
    """Simulates a natural scroll behavior or a fast trigger scroll."""
    total_height = await page.evaluate("document.body.scrollHeight")
    current_scroll = 0
    cap = 5000 if not fast else 2000

    while current_scroll < total_height:
        if fast:
            # In fast mode, we jump larger distances and don't wait as long
            scroll_step = random.randint(800, 1200)
            await page.mouse.wheel(0, scroll_step)
            current_scroll += scroll_step
            await asyncio.sleep(0.1) # Minimum wait for lazy images
        else:
            scroll_step = random.randint(200, 500)
            current_scroll += scroll_step
            await page.mouse.wheel(0, scroll_step)
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            if random.random() < 0.1:
                back_scroll = random.randint(50, 150)
                await page.mouse.wheel(0, -back_scroll)
                current_scroll -= back_scroll
                await asyncio.sleep(random.uniform(0.3, 0.8))
            
        total_height = await page.evaluate("document.body.scrollHeight")
        if current_scroll > cap:
             break
