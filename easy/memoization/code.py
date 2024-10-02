from typing import Callable


def memoize(func: Callable) -> Callable:
    """Memoize function"""
    cache = {}

    def wrapped(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))

        if key not in cache:
            cache[key] = result = func(*args, **kwargs)

        return cache[key]

    return wrapped

