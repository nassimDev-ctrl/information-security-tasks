
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 1]


def hex_to_bin(hex_key):
    return ''.join(format(int(c, 16), '04b') for c in hex_key)


def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def des_generate_subkeys(hex_key):
   
    key_bin = hex_to_bin(hex_key)

    key_56 = permute(key_bin, PC1)

    C = key_56[:28]
    D = key_56[28:]

    subkeys = []

    for round_no in range(16):
        C = left_shift(C, SHIFT_TABLE[round_no])
        D = left_shift(D, SHIFT_TABLE[round_no])

        subkey = permute(C + D, PC2)
        subkeys.append(subkey)

    return subkeys


if __name__ == "__main__":
    key = "133457799BBCDFF1"

    subkeys = des_generate_subkeys(key)

    print("DES Subkeys:\n")
    for i, k in enumerate(subkeys):
        print(f"Round {i+1:02}: {k}")
