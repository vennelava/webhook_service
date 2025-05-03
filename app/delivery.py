import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Main webhook sending function with retry logic
async def deliver_webhook_with_retries(url: str, payload: dict, secret: str = None, max_retries: int = 3):
    headers = {}
    if secret:
        headers["X-Hub-Signature"] = secret

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=5)
                response.raise_for_status()
                logger.info(f"[✓] Delivered webhook to {url} on attempt {attempt}")
                return {"status": "success", "attempt": attempt}
        except Exception as e:
            logger.warning(f"[!] Attempt {attempt} failed for {url}: {e}")
            if attempt < max_retries:
                await asyncio.sleep(2 ** (attempt - 1))  # Exponential backoff
            else:
                logger.error(f"[X] Final failure to deliver webhook to {url}")
                return {"status": "failure", "reason": str(e)}
