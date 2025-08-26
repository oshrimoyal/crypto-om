"""
Data Fetcher Service

This script connects to configured exchanges and publishes market data to the
message bus.  In this skeleton it simply logs a message periodically.
"""

import asyncio
import os
from services.utils.logger import logger
from services.utils.messaging import publish


async def main() -> None:
    interval = int(os.getenv("DATA_FETCH_INTERVAL", "10"))
    while True:
        # In a real implementation, fetch tickers/funding from ExchangeClient
        logger.info("Data fetcher heartbeat")
        await publish("data.heartbeat", {"msg": "data alive"})
        await asyncio.sleep(interval)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Data fetcher stopped")