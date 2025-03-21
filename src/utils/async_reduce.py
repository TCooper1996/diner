import asyncio
from functools import reduce
from typing import Awaitable, Callable, Any, List, TypeVar

T = TypeVar("T")
B  = TypeVar("B")
V  = TypeVar("V")
async def async_reduce(func: Callable[[T, B], Awaitable[V]], iterable: List[B], initializer: T) -> List[V]:
    value = initializer
    results:List[V] = []
    for item in iterable:
        results.append( await func(value, item))
        value = results[-1][-1][1]
    
    return results
