import numpy as np
from functools import reduce

# (15, 11) Hamming code, allows to fix single bit error on the receiver side
# this example for 11 data bits, 4 parity bits

# Message representation:
# X is parity bit
# D is data bit
# zero element is ignored
#
# _ X X D
# X D D D
# X D D D
# D D D D


def to_message(data):
    if len(data) != 11:
        raise Exception("invalid data")

    res = [0]*16

    i = 0
    for idx in range(16):
        if idx not in [0, 1, 2, 4, 8]:
            res[idx] = data[i]
            i += 1

    # number of 1ns in elements 1, 3, 5, 7, 9, 11, 13, 15 should be even
    res[1] = 0 if sum([res[3], res[5], res[7], res[9], res[11], res[13], res[15]]) % 2 == 0 else 1
    # number of 1ns in elements 2, 3, 6, 7, 10, 11, 14, 15 should be even
    res[2] = 0 if sum([res[3], res[6], res[7], res[10], res[11], res[14], res[15]]) % 2 == 0 else 1
    # number of 1ns in elements 4, 5, 6, 7, 12, 13, 14, 15 should be even
    res[4] = 0 if sum([res[5], res[6], res[7], res[12], res[13], res[14], res[15]]) % 2 == 0 else 1
    # number of 1ns in elements 8, 9, 10, 11, 12, 13, 14, 15 should be even
    res[8] = 0 if sum([res[9], res[10], res[11], res[12], res[13], res[14], res[15]]) % 2 == 0 else 1

    print("sending message:")
    print_data(res)
    return res


def print_data(data):
    for i in range(16):
        if i > 0 and i % 4 == 0:
            print()
        print(f"{str(data[i])} ", end="")
    print()


def from_message(message):
    reduced = reduce(lambda x, y: x ^ y, [i for i, bit in enumerate(message) if bit])
    if reduced is not 0:
        # error detected
        print(f"error detected at pos {reduced}:{bin(reduced)}")
        message[reduced] = 0 if message[reduced] else 1

    print("received message:")
    print_data(message)

    res = [0]*11
    i = 0
    for idx in range(16):
        if idx not in [0, 1, 2, 4, 8]:
            res[i] = message[idx]
            i += 1

    return res


if __name__ == '__main__':

    src_data = np.random.randint(0, 2, 11)
    msg = to_message(src_data)

    k = np.random.randint(16)
    msg[k] = 0 if msg[k] else 1
    print(f"message with corrupted bit {k}:")
    print_data(msg)

    dst_data = from_message(msg)
    print(f"Src: {list(src_data)}")
    print(f"Dst: {list(dst_data)}")
    assert (src_data == dst_data).all()








