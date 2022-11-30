from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.batch.batch import Batch


class Observer(abc.ABC):
    @abc.abstractmethod
    def on_batch_full(self, batch: 'Batch'):
        ...
