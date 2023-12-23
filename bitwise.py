from collections.abc import Callable
from itertools import zip_longest


def bit(b: bytes, index: int):
    return bool(b[index // 8] & 1 << index % 8)


def count_ones(b: bytes) -> int:
    return sum(bit(b, i) for i in range(len(b) * 8))


def toggle(b: bytes, bit_index: int) -> bytes:
    byte_index = bit_index // 8
    return (
        b[:byte_index]
        + bytes([b[byte_index] ^ 1 << bit_index % 8])
        + b[byte_index + 1 :]
    )


def pad(b: bytes, target_length: int, pad_right: bool = False):
    current_length = len(b)
    assert current_length <= target_length

    pad = bytes(target_length - current_length)

    if pad_right:
        return b + pad
    else:
        return pad + b


def truncate(b: bytes, target_length: int, truncate_right: bool = False):
    current_length = len(b)
    assert current_length >= target_length

    if truncate_right:
        return b[:target_length]
    else:
        return b[-target_length:]


def xor(a: bytes, b: bytes):
    return bytes(i ^ j for i, j in zip_longest(a, b, fillvalue=0))
