from __future__ import annotations

from typing import TYPE_CHECKING

from src.observers.abc_observers import Observer

if TYPE_CHECKING:
    from src.batch.batch import Batch


class LogObserver(Observer):
    nb_batches: int = 0

    async def on_batch_full(self, batch: Batch):
        print(f"Batch n°{batch.id} {self.nb_batches} is full")
        self.nb_batches += 1
