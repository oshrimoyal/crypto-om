import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import Optional

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish


@dataclass
class LiquiditySignal:
    strategy: str
    market: str
    direction: str
    timestamp: dt.datetime


class LiquidityEngine:
    def __init__(self, market: str):
        self.market = market
        self.grid_levels = get_param("strategies.liquidity.grid_levels", 5)
        self.price_step_pct = get_param("strategies.liquidity.price_step_pct", 0.005)
        self.last_rebalanced: Optional[dt.datetime] = None

    async def on_data(self) -> None:
        # In a real implementation, we would monitor current price and adjust grid orders;
        # here we simply emit a heartbeat signal periodically to demonstrate functionality.
        now = dt.datetime.utcnow()
        if not self.last_rebalanced or (now - self.last_rebalanced).seconds > 60:
            signal = LiquiditySignal(
                strategy="liquidity",
                market=self.market,
                direction="rebalance",
                timestamp=now,
            )
            await publish("signals.liquidity", signal.__dict__)
            logger.debug(f"[Liquidity] {self.market} rebalance")
            self.last_rebalanced = now