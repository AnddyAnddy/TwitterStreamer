from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.tweet import Tweet
    from src.observers.abc_observers import Observer


class Batch:
    def __init__(self, limit=10, batch_id: int = 0):
        self.tweets: list[Tweet] = list()
        self.observers: list[Observer] = []
        self.limit = limit
        self.id = batch_id

    @property
    def is_full(self):
        return len(self.tweets) == self.limit

    def attach_observers(self, obs: Observer):
        self.observers.append(obs)

    def dettach_observers(self, obs):
        try:
            self.observers.remove(obs)
        except ValueError:
            pass

    async def add(self, tweet: Tweet) -> 'Batch':
        if tweet is None:
            return self
        self.tweets.append(tweet)
        if not self.is_full:
            return self

        new_batch = Batch(self.limit, batch_id=self.id + 1)
        await asyncio.gather(*[obs.on_batch_full(self) for obs in self.observers])
        for obs in self.observers:
            new_batch.attach_observers(obs)
        return new_batch
