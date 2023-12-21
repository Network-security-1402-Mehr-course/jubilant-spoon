from itertools import combinations
from random import randbytes
from typing import Generator

from bitwise import toggle

BytesGenerator = Generator[bytes, None, None]


def random_bytes(block_size: int) -> BytesGenerator:
    while True:
        yield randbytes(block_size)


def all_bytes_ascending(block_size: int) -> BytesGenerator:
    if block_size == 0:
        yield bytes()
        return

    assert block_size > 0

    for head in range(256):
        yield from (
            bytes([head]) + tail for tail in all_bytes_ascending(block_size - 1)
        )


def bytes_neighbourhood(center: bytes, radius: int) -> BytesGenerator:
    for toggle_indices in combinations(range(8 * len(center)), radius):
        neighbour = center
        for index in toggle_indices:
            neighbour = toggle(neighbour, index)

        yield neighbour
