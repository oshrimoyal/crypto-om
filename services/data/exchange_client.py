import os
import ccxt
from typing import Dict, Any


class ExchangeClient:
    def __init__(self, exchange_id: str, api_key: str | None = None, api_secret: str | None = None):
        self.exchange_id = exchange_id
        self.api_key = api_key or os.getenv(f"{exchange_id.upper()}_API_KEY", "")
        self.api_secret = api_secret or os.getenv(f"{exchange_id.upper()}_API_SECRET", "")
        exchange_class = getattr(ccxt, exchange_id)
        self.client = exchange_class({
            "apiKey": self.api_key,
            "secret": self.api_secret,
            "enableRateLimit": True,
        })

    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        return self.client.fetch_ticker(symbol)

    def fetch_funding_rate(self, symbol: str) -> float:
        # ccxt unified funding rate for perpetuals, returns funding rate per period
        try:
            funding_info = self.client.funding_rate(symbol)
            return funding_info.get("fundingRate", 0.0)
        except Exception:
            return 0.0