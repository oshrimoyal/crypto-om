import asyncio
from datetime import datetime, timedelta

from services.utils.logger import logger


async def send_eod_report() -> None:
    logger.info("Sending end‑of‑day report (placeholder)")


async def scheduler_loop() -> None:
    next_run = datetime.utcnow() + timedelta(days=1)
    while True:
        now = datetime.utcnow()
        if now >= next_run:
            await send_eod_report()
            next_run = now + timedelta(days=1)
        await asyncio.sleep(60)


def main() -> None:
    try:
        asyncio.run(scheduler_loop())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()