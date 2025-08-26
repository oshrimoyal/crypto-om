import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import Optional

from services.utils.config import get_param
from services.utils.logger import logger
from services.utils.messaging import publish


@dataclass
class BasisSignal:
    strategy: str
    market: str
    direction: str
    strength: float
    timestamp: dt.datetime


class BasisEngine:
    def __init__(self, market: str):
        self.market = market
        self.entry_threshold = get_param("strategies.basis.entry_threshold", 0.02)
        self.exit_threshold = get_param("strategies.basis.exit_threshold", 0.005)
        self.last_basis: Optional[float] = None

    async def compute_basis(self) -> float:
        # Placeholder: in real code fetch spot and future prices
        # and compute annualised basis.  Here we oscillate for demo.
        ts = dt.datetime.utcnow().timestamp()
        return 0.025 * (1 if int(ts) % 2 == 0 else -1)

    async def on_data(self) -> None:
        basis = await self.compute_basis()
        logger.debug(f"[Basis] {self.market} basis={basis:.4f}")
        if basis > self.entry_threshold:
            signal = BasisSignal(
                strategy="basis",
                market=self.market,
                direction="short_futures_long_spot",
                strength=basis,
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.basis", signal.__dict__)
        elif basis < -self.entry_threshold:
            signal = BasisSignal(
                strategy="basis",
                market=self.market,
                direction="long_futures_short_spot",
                strength=abs(basis),
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.basis", signal.__dict__)
        elif self.last_basis is not None and abs(basis) < self.exit_threshold:
            signal = BasisSignal(
                strategy="basis",
                market=self.market,
                direction="flat",
                strength=0.0,
                timestamp=dt.datetime.utcnow(),
            )
            await publish("signals.basis", signal.__dict__)
        self.last_basis = basis