
from dataclasses import dataclass
from queue import Empty, Queue
from typing import Tuple, TypeVar


T = TypeVar("T")
V = TypeVar("V")
@dataclass
class EventManager[T, V]:
    in_q: Queue
    out_q: Queue
    def get_event(self, block: bool=False) -> T | None:
        try:
            return self.in_q.get( block=block)  # Non-blocking get
        except Empty:
            return None

    def put_event(self, event: V):
        self.out_q.put(event)
