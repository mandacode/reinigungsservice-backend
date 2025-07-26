import functools
import time
from typing import Callable, Awaitable


def timer(func: Callable[..., Awaitable]) -> Callable:
    @functools.wraps(func)
    async def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.10f} secs")
        return result
    return wrapper_timer

