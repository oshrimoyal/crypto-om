import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import Optional

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish


@dataclass
class FundingSignal:
    strategy: str
    market: str
    direction: str
    strength: float
    timestamp: dt.datetime


class FundingEngine:
    def __init__(self, market: str):
        self.market = market
        self.entry_threshold = get_param("strategies.funding.entry_threshold", 0.0001)
        self.exit_threshold = get_param("strategies.funding.exit_threshold", 0.0)
        self.last_rate: Optional[float] = None

    async def fetch_funding_rate(self) -> float:
        # Placeholder: returns an oscillating funding rate for demonstration
        ts = dt.datetime.utcnow().timestamp()
        return 0.0002 if int(ts) % 2 == 0 else -0.0002

    async def on_data(self) -> None:
        rate = await self.fetch_funding_rate()
        logger.debug(f"[Funding] {self.market} rate={rate:.5f}")
        if rate > self.entry_threshold:
            signal = FundingSignal(
                strategy="funding",
                market=self.market,
                direction="short_perp_long_spot",
                strength=rate,
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.funding", signal.__dict__)
        elif rate < -self.entry_threshold:
            signal = FundingSignal(
                strategy="funding",
                market=self.market,
                direction="long_perp_short_spot",
                strength=abs(rate),
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.funding", signal.__dict__)
        elif self.last_rate is not None and abs(rate) <= self.exit_threshold:
            signal = FundingSignal(
                strategy="funding",
                market=self.market,
                direction="flat",
                strength=0.0,
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.funding", signal.__dict__)
        self.last_rate = rate