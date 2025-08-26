import asyncio
from typing import Dict

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish


class RiskManager:
    """
    RiskManager enforces per‑trade and portfolio level limits.  In this skeleton it
    simply approves all signals and forwards them to the order router.
    """

    def __init__(self):
        self.max_trade_risk = get_param("risk.max_trade_risk", 0.05)

    async def handle_signal(self, signal: Dict[str, any]) -> None:
        # TODO: check exposures, drawdowns, etc.
        logger.info(f"Risk approved signal {signal}")
        await publish("orders.inbound", signal)

    async def run(self) -> None:
        from services.utils.messaging import get_nats
        nc = await get_nats()
        async def on_signal(msg: Dict[str, any]):
            await self.handle_signal(msg)
        await nc.subscribe("signals.*", "risk", on_signal)
        logger.info("Risk manager started")
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    import asyncio
    rm = RiskManager()
    try:
        asyncio.run(rm.run())
    except KeyboardInterrupt:
        logger.info("Risk manager stopped")