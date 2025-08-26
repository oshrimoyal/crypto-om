"""
Signals Service

This module runs the individual strategy engines.  It subscribes to
market data via the message bus and publishes trading signals.
"""

import asyncio
from services.signals.basis import BasisEngine
from services.signals.funding import FundingEngine
from services.signals.statarb import StatArbEngine
from services.signals.trend import TrendEngine
from services.signals.liquidity import LiquidityEngine
from services.utils.logger import logger
from services.utils.messaging import get_nats


async def run_signals() -> None:
    nc = await get_nats()
    # Instantiate engines; in real code, loop over configured markets/timeframes
    basis = BasisEngine(market="BTC/USDT")
    funding = FundingEngine(market="BTC/USDT")
    statarb = StatArbEngine(pairs=[("BTC/USDT", "ETH/USDT")])
    trend = TrendEngine(market="BTC/USDT")
    liquidity = LiquidityEngine(market="BTC/USDT")

    async def on_data(_):
        # Fake signal update; real implementation processes data to produce signals
        await basis.on_data()
        await funding.on_data()
        await statarb.on_data()
        await trend.on_data()
        await liquidity.on_data()

    # Subscribe to data.heartbeat for demonstration
    await nc.subscribe("data.heartbeat", "signals", on_data)
    logger.info("Signals service started")
    while True:
        await asyncio.sleep(1)


def main() -> None:
    try:
        asyncio.run(run_signals())
    except KeyboardInterrupt:
        logger.info("Signals service stopped")


if __name__ == "__main__":
    main()