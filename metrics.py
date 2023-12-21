from collections.abc import Callable

from bitwise import count_ones, toggle, xor
from generators import BytesGenerator

Encryption = Callable[[bytes], bytes]


def strict_avalanche_deviation(
    encryption: Encryption, input_size: int, output_size: int, generator: BytesGenerator
):
    input_bits = 8 * input_size
    output_bits = 8 * output_size

    total_deviation = 0
    sample_size = 0
    for input in generator:
        output = encryption(input)

        sample_size += input_bits
        for i in range(input_bits):
            new_input = toggle(input, i)
            new_output = encryption(new_input)
            changed_bits = count_ones(xor(new_output, output))
            deviation = changed_bits / output_bits - 0.5
            total_deviation += deviation**2

    return total_deviation / sample_size
