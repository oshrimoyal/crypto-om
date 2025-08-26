import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import List, Tuple

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish
from services.utils.math_utils import zscore


@dataclass
class StatArbSignal:
    strategy: str
    pair: Tuple[str, str]
    direction: str
    strength: float
    timestamp: dt.datetime


class StatArbEngine:
    def __init__(self, pairs: List[Tuple[str, str]]):
        self.pairs = pairs
        self.entry_z = get_param("strategies.statarb.entry_zscore", 2.0)
        self.exit_z = get_param("strategies.statarb.exit_zscore", 0.0)
        self.spread_history = {pair: [] for pair in pairs}

    async def compute_spread(self, pair: Tuple[str, str]) -> float:
        # Placeholder: in real code fetch prices for both symbols and compute log spread
        # Here generate synthetic spread changing sign over time
        ts = dt.datetime.utcnow().timestamp()
        return 0.02 if int(ts) % 2 == 0 else -0.02

    async def on_data(self) -> None:
        for pair in self.pairs:
            spread = await self.compute_spread(pair)
            hist = self.spread_history[pair]
            hist.append(spread)
            if len(hist) > 50:
                hist.pop(0)
            z = zscore(hist)
            logger.debug(f"[StatArb] {pair} z={z:.2f}")
            if z > self.entry_z:
                # spread is positive: short first, long second
                signal = StatArbSignal(
                    strategy="statarb",
                    pair=pair,
                    direction="short_long",
                    strength=z,
                    timestamp=dt.datetime.utcnow(),
                )
                await publish("signals.statarb", signal.__dict__)
            elif z < -self.entry_z:
                # spread negative: long first, short second
                signal = StatArbSignal(
                    strategy="statarb",
                    pair=pair,
                    direction="long_short",
                    strength=abs(z),
                    timestamp=dt.datetime.utcnow(),
                )
                await publish("signals.statarb", signal.__dict__)
            elif abs(z) <= self.exit_z:
                signal = StatArbSignal(
                    strategy="statarb",
                    pair=pair,
                    direction="flat",
                    strength=0.0,
                    timestamp=dt.datetime.utcnow(),
                )
                await publish("signals.statarb", signal.__dict__)