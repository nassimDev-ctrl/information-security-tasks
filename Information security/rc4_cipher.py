def rc4_ksa(key):
    
    key = [ord(c) for c in key]
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def rc4_prga(S, length):
    
    i = 0
    j = 0
    keystream = []

    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)

    return keystream


def rc4_keystream(key, length):
    S = rc4_ksa(key)
    return rc4_prga(S, length)


def keystream_to_bits(keystream):
    bits = ""
    for byte in keystream:
        bits += format(byte, '08b')
    return bits


def binary_derivative_test(bits):
    
    derivative = ""
    for i in range(len(bits) - 1):
        derivative += str(int(bits[i]) ^ int(bits[i + 1]))
    return derivative


def change_point_test(bits):
    
    changes = 0
    for i in range(len(bits) - 1):
        if bits[i] != bits[i + 1]:
            changes += 1
    return changes


if __name__ == "__main__":
    key = "SECURITY"
    length = 16  

    print("Key:", key)

    ks = rc4_keystream(key, length)
    print("\nKeystream (bytes):")
    print(ks)

    bits = keystream_to_bits(ks)
    print("\nKeystream (binary):")
    print(bits)

    derivative = binary_derivative_test(bits)
    print("\nBinary Derivative:")
    print(derivative)

    changes = change_point_test(bits)
    print("\nChange Point Count:", changes)
