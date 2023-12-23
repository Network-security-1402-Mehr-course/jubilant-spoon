from itertools import accumulate
from bitwise import bit


def abs(num: int):
    if num < 0:
        return -num
    return num

p = [
    [0.5, 0.75, 0.8333, 0.875, 0.9, 0.9167, 0.9286],
    [0.25, 0.0625, 0.0278, 0.0156, 0.01, 0.0069, 0.0051],
    [0.125, 0.0469, 0.0231, 0.0137, 0.009, 0.0064, 0.0047],
    [0.0625, 0.0352, 0.0193, 0.012, 0.0081, 0.0058, 0.0044],
    [0.0312, 0.0264, 0.0161, 0.0105, 0.0073, 0.0053, 0.0041],
    [0.0312, 0.0791, 0.0804, 0.0733, 0.0656, 0.0588, 0.0531],
]


def random_excursions(b: bytes):
    input_bits = len(b) * 8

    B: list[int] = [bit(b, i) * 2 - 1 for i in range(input_bits)]
    S = [0] + list(accumulate(B))
    if S[-1] != 0:
        S.append(0)

    cycles: list[list[int]] = []
    for i in S:
        if i == 0:
            cycles.append([])
        else:
            cycles[-1].append(i)

    J = len(cycles)

    v = {i: [0 for _ in range(6)] for i in [-4, -3, -2, -1, 1, 2, 3, 4]}
    for state_value in v.keys():
        for cycle in cycles:
            v[state_value][min(5, cycle.count(state_value))] += 1

    ans = {i: 0.0 for i in v.keys()}

    for i in range(6):
        for j in v.keys():
            ans[j] += (v[j][i] - J * p[i][abs(j)]) ** 2 / J * p[i][abs(j)]
    return ans
