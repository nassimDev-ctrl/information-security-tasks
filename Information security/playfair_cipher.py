

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 


def playfair_prepare_text(text):
    text = text.upper()
    text = ''.join(ch for ch in text if ch.isalpha())
    text = text.replace('J', 'I')

    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + 'X')
            i += 1

    return pairs


def playfair_key_matrix(key):
    key = key.upper()
    key = ''.join(ch for ch in key if ch.isalpha())
    key = key.replace('J', 'I')

    seen = set()
    matrix = []

    for ch in key:
        if ch not in seen:
            seen.add(ch)
            matrix.append(ch)

    for ch in ALPHABET:
        if ch not in seen:
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def find_position(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    return None


def playfair_encrypt(plaintext, key):
    matrix = playfair_key_matrix(key)
    pairs = playfair_prepare_text(plaintext)

    cipher = ""

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            cipher += matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r2][(c2 + 1) % 5]

        elif c1 == c2:
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]

        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher


def playfair_decrypt(ciphertext, key):
    matrix = playfair_key_matrix(key)
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]

    plaintext = ""

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plaintext += matrix[r1][(c1 - 1) % 5]
            plaintext += matrix[r2][(c2 - 1) % 5]

        elif c1 == c2:
            plaintext += matrix[(r1 - 1) % 5][c1]
            plaintext += matrix[(r2 - 1) % 5][c2]

        else:
            plaintext += matrix[r1][c2]
            plaintext += matrix[r2][c1]

    return plaintext


if __name__ == "__main__":
    key = "MONARCHY"
    plaintext = "BALLOON"

    print("Key:", key)
    print("Plaintext:", plaintext)

    cipher = playfair_encrypt(plaintext, key)
    print("Encrypted:", cipher)

    decrypted = playfair_decrypt(cipher, key)
    print("Decrypted:", decrypted)
