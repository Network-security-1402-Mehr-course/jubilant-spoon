from functools import partial
from itertools import islice
from random import randbytes

import baby_ridjndael
from bitwise import count_ones
from generators import all_bytes_ascending
from metrics import avalanche_effect, completeness, strict_avalanche_effect

if __name__ == "__main__":
    baby_ridjndael.BLOCK_SIZE
    random_key = randbytes(baby_ridjndael.KEY_SIZE)
    for metric in [completeness, avalanche_effect, strict_avalanche_effect]:
        print(
            metric(
                partial(baby_ridjndael.encrypt, key=random_key),
                baby_ridjndael.BLOCK_SIZE,
                baby_ridjndael.BLOCK_SIZE,
                (
                    i
                    for i in islice(
                        all_bytes_ascending(baby_ridjndael.BLOCK_SIZE), 0, 1000
                    )
                    if count_ones(i) % 2
                ),
            )
        )
