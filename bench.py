from timeit import timeit
from random import random
from functools import partial
from threading import Thread


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


def benchmark3(heights):
    t1 = Thread(target=benchmark1, args=(heights,))
    t2 = Thread(target=benchmark2, args=(heights,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def isgil():
    import time

    def fakesleep(t):
        _start, i = time.time(), 997.0
        while _start + t > time.time():
            i *= random()

    start = time.time()
    threads = [Thread(target=fakesleep, args=(1,)) for _ in range(12)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return time.time() - start


def all():
    A = [random() for _ in range(int(1e6))]
    yield "isgil", timeit(isgil, number=1)
    yield "inline", timeit(partial(benchmark1, A), number=int(1e1))
    yield "native", timeit(partial(benchmark2, A), number=int(1e1))
    yield "thread", timeit(partial(benchmark3, A), number=int(1e1))


print("\n".join(f"{name}: {time}" for name, time in all()))