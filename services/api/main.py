from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import datetime as dt

from services.utils.logger import logger
from services.utils.messaging import publish


app = FastAPI(title="Crypto‑OM API", version="1.0.0")


class SignalRequest(BaseModel):
    strategy: str
    market: str
    timeframe: Optional[str] = None
    direction: str
    strength: float = Field(ge=0)
    parameters: Optional[Dict[str, float]] = None


class NewOrderRequest(BaseModel):
    signal_id: Optional[str] = None
    exchange: str
    symbol: str
    type: str
    side: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    take_profit: Optional[float] = None
    client_order_id: Optional[str] = None


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "timestamp": dt.datetime.utcnow().isoformat()}


@app.post("/signals", status_code=201)
async def post_signal(signal: SignalRequest) -> Dict[str, str]:
    logger.info(f"API received signal: {signal}")
    await publish("signals.api", signal.dict())
    return {"status": "accepted"}


@app.post("/orders", status_code=201)
async def post_order(order: NewOrderRequest) -> Dict[str, str]:
    logger.info(f"API received order: {order}")
    await publish("orders.api", order.dict())
    return {"status": "received"}


@app.get("/positions", response_model=List[Dict[str, any]])
async def get_positions() -> List[Dict[str, any]]:
    # TODO: load positions from portfolio manager or DB
    return []


@app.get("/risk", response_model=Dict[str, float])
async def get_risk() -> Dict[str, float]:
    # TODO: calculate risk metrics from risk manager or DB
    return {"system_drawdown": 0.0, "daily_drawdown": 0.0, "exposure": 0.0}