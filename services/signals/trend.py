import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import Deque, Optional
from collections import deque

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish


@dataclass
class TrendSignal:
    strategy: str
    market: str
    direction: str
    timestamp: dt.datetime


class TrendEngine:
    def __init__(self, market: str):
        self.market = market
        self.short_ma_period = get_param("strategies.trend.short_ma", 50)
        self.long_ma_period = get_param("strategies.trend.long_ma", 200)
        self.price_history: Deque[float] = deque(maxlen=self.long_ma_period)
        self.last_direction: Optional[str] = None

    async def fetch_price(self) -> float:
        # Placeholder: generate synthetic price oscillation around 1.0
        ts = dt.datetime.utcnow().timestamp()
        return 1.0 + 0.01 * (1 if int(ts) % 2 == 0 else -1)

    def compute_ma(self, length: int) -> float:
        if len(self.price_history) < length:
            return sum(self.price_history) / len(self.price_history) if self.price_history else 0.0
        else:
            return sum(list(self.price_history)[-length:]) / length

    async def on_data(self) -> None:
        price = await self.fetch_price()
        self.price_history.append(price)
        short_ma = self.compute_ma(self.short_ma_period)
        long_ma = self.compute_ma(self.long_ma_period)
        direction = None
        if short_ma > long_ma and (self.last_direction != "long"):
            direction = "long"
        elif short_ma < long_ma and (self.last_direction != "short"):
            direction = "short"
        elif self.last_direction and abs(short_ma - long_ma) < 1e-6:
            direction = "flat"
        if direction:
            signal = TrendSignal(
                strategy="trend",
                market=self.market,
                direction=direction,
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.trend", signal.__dict__)
            logger.debug(f"[Trend] {self.market} short_ma={short_ma:.4f} long_ma={long_ma:.4f} dir={direction}")
            self.last_direction = direction