from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import ClientSession
from src.observers.abc_observers import Observer

if TYPE_CHECKING:
    from src.batch.batch import Batch

API_ENDPOINT = 'http://localhost:8081/tweets/tweets'


class Http:
    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def fetch(self, url):
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            return await resp.read()


class PostBatchObserver(Observer):
    session: ClientSession = None

    async def on_batch_full(self, batch: Batch):
        if self.session is None:
            self.session = ClientSession()
        data = [tweet.dict() for tweet in batch.tweets]

        async with self.session.post(API_ENDPOINT, json=data) as resp:
            print(resp.status)
