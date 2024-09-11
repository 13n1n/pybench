from timeit import timeit
from random import random
from functools import partial


def benchmark1(heights):
    a = 1
    b = len(heights) - 1
    min_height = heights[0]
    while a < b:
        if heights[a] < min_height:
            min_height = heights[a]
        a += 1

    return min_height


def benchmark2(heights):
    a = 1
    b = len(heights) - 1
    min_height = heights[0]
    while a < b:
        min_height = min(heights[a], min_height)
        a += 1

    return min_height


def all():
    A = [random() for _ in range(int(1e6))]
    yield "inline", timeit(partial(benchmark1, A), number=int(1e2))
    yield "native", timeit(partial(benchmark2, A), number=int(1e2))


print("\n".join(f"{name}: {time}" for name, time in all()))