

LABELS = "ADFGVX"
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def adfgvx_key_matrix(key):
    
    key = key.upper()

    seen = set()
    matrix = []

    for ch in key:
        if ch in SYMBOLS and ch not in seen:
            seen.add(ch)
            matrix.append(ch)

    for ch in SYMBOLS:
        if ch not in seen:
            matrix.append(ch)

    return [matrix[i:i+6] for i in range(0, 36, 6)]


def find_position(matrix, ch):
    
    for r in range(6):
        for c in range(6):
            if matrix[r][c] == ch:
                return r, c
    return None


def adfgvx_encrypt(plaintext, key):
    matrix = adfgvx_key_matrix(key)

    plaintext = plaintext.upper()
    plaintext = ''.join(ch for ch in plaintext if ch.isalnum())

    cipher = ""

    for ch in plaintext:
        r, c = find_position(matrix, ch)
        cipher += LABELS[r] + LABELS[c]

    return cipher


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(row))


if __name__ == "__main__":
    key = "SECURITY"
    plaintext = "ATTACK2025"

    print("Key:", key)
    print("Plaintext:", plaintext)

    matrix = adfgvx_key_matrix(key)
    print("\nADFGVX Key Matrix:")
    print_matrix(matrix)

    cipher = adfgvx_encrypt(plaintext, key)
    print("\nEncrypted Text:", cipher)
