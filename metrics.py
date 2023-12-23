from collections.abc import Callable

from bitwise import bit, count_ones, toggle, xor
from generators import BytesGenerator

Encryption = Callable[[bytes], bytes]


def completeness(
    encryption: Encryption, input_size: int, output_size: int, generator: BytesGenerator
):
    input_bits = 8 * input_size
    output_bits = 8 * output_size

    changed_with_input_bit_change = [bytes(output_size) for _ in range(input_bits)]

    for input in generator:
        output = encryption(input)

        for i in range(input_bits):
            new_input = toggle(input, i)
            new_output = encryption(new_input)
            change = xor(new_output, output)
            changed_with_input_bit_change[i] = bytes(
                j | k for j, k in zip(change, changed_with_input_bit_change[i])
            )

    return [
        [bit(i, j) for j in range(output_bits)] for i in changed_with_input_bit_change
    ]


def avalanche_effect(
    encryption: Encryption, input_size: int, output_size: int, generator: BytesGenerator
):
    input_bits = 8 * input_size
    output_bits = 8 * output_size

    total_changed_bits = 0
    sample_size = 0

    for input in generator:
        output = encryption(input)

        sample_size += 1
        for i in range(input_bits):
            new_input = toggle(input, i)
            new_output = encryption(new_input)
            total_changed_bits += count_ones(xor(new_output, output))

    return total_changed_bits / output_bits / sample_size


def strict_avalanche_effect(
    encryption: Encryption, input_size: int, output_size: int, generator: BytesGenerator
):
    input_bits = 8 * input_size
    output_bits = 8 * output_size

    tcobpcib = [
        0 for _ in range(input_bits)
    ]  # Total changed output bits per changed input bit
    sample_size = 0

    for input in generator:
        output = encryption(input)

        sample_size += 1
        for i in range(input_bits):
            new_input = toggle(input, i)
            new_output = encryption(new_input)
            changed = xor(new_output, output)
            for j in range(output_bits):
                tcobpcib[i] += bit(changed, j)

    return [changed_bits / sample_size for changed_bits in tcobpcib]
