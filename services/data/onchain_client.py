from typing import Dict

from services.utils.onchain_features import fetch_onchain_metrics


class OnchainClient:
    async def get_metrics(self, symbol: str) -> Dict[str, float]:
        return await fetch_onchain_metrics(symbol)