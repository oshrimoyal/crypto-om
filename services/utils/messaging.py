import asyncio
import json
import os
from nats.aio.client import Client as NATS


class NatsClient:
    def __init__(self, url: str | None = None):
        self.url = url or os.getenv("NATS_URL", "nats://localhost:4222")
        self.nc = NATS()

    async def connect(self) -> None:
        await self.nc.connect(servers=[self.url])

    async def publish(self, subject: str, message: dict) -> None:
        await self.nc.publish(subject, json.dumps(message).encode())

    async def subscribe(self, subject: str, queue: str, callback):
        async def handler(msg):
            data = json.loads(msg.data.decode())
            await callback(data)
        await self.nc.subscribe(subject, queue, handler)


_client: NatsClient | None = None


async def get_nats() -> NatsClient:
    global _client
    if _client is None:
        _client = NatsClient()
        await _client.connect()
    return _client


async def publish(subject: str, message: dict) -> None:
    nc = await get_nats()
    await nc.publish(subject, message)