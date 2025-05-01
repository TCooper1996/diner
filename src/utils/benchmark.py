import datetime
import time
import functools
import asyncio


stack = 0
def benchmark(func):
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        global stack
        start = time.perf_counter()
        print(f"{"\n"*stack}Benchmarking {func.__name__} - Stack level: {stack}")
        stack += 1
        result = func(*args, **kwargs)
        stack -= 1
        end = time.perf_counter()
        print(f"{"\t"*stack}{func.__name__} executed in {end - start} seconds")
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        global stack
        start = time.perf_counter()
        print(f"{"\t"*stack}Benchmarking {func.__name__} - Stack level: {stack}")
        stack += 1
        result = await func(*args, **kwargs)
        stack -= 1
        end = time.perf_counter()
        print(f"{"\t"*stack}{func.__name__} executed in {end - start} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

start = 0
first_func = None
def print_time_since(func_name):
    global start
    global first_func
    if start == 0:
        start = time.perf_counter()
        first_func = func_name
    if first_func == func_name:
        start = time.perf_counter()
    elapsed = time.perf_counter() - start
    print(f"Executing {func_name} at {elapsed}")