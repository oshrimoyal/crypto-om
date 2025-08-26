from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Position:
    symbol: str
    qty: float
    avg_entry: float
    unrealised_pnl: float = 0.0
    realised_pnl: float = 0.0


class PortfolioManager:
    def __init__(self) -> None:
        self.positions: Dict[str, Position] = {}

    def update_position(self, symbol: str, qty: float, price: float) -> None:
        pos = self.positions.get(symbol)
        if pos is None:
            self.positions[symbol] = Position(symbol, qty, price)
        else:
            # simple average for demonstration
            total_qty = pos.qty + qty
            if total_qty != 0:
                pos.avg_entry = (pos.avg_entry * pos.qty + price * qty) / total_qty
            pos.qty = total_qty

    def get_positions(self) -> Dict[str, Position]:
        return self.positions