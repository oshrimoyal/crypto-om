"""
Execution Service

Consumes approved signals from the risk manager and sends orders to exchanges.
This skeleton logs the order instead of submitting it.
"""

import asyncio
from typing import Dict

from services.utils.logger import logger
from services.utils.messaging import get_nats


class OrderRouter:
    async def handle_order(self, order: Dict[str, any]) -> None:
        # TODO: translate signal into exchange order and submit
        logger.info(f"Executing order: {order}")

    async def run(self) -> None:
        nc = await get_nats()
        async def on_order(msg: Dict[str, any]):
            await self.handle_order(msg)
        await nc.subscribe("orders.inbound", "execution", on_order)
        logger.info("Execution service started")
        while True:
            await asyncio.sleep(1)


def main() -> None:
    router = OrderRouter()
    try:
        asyncio.run(router.run())
    except KeyboardInterrupt:
        logger.info("Execution service stopped")


if __name__ == "__main__":
    main()