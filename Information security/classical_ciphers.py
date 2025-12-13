
from typing import List, Tuple, Optional

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = ALPHABET.upper()
M = 26  

def _shift_char_additive(ch: str, k: int) -> str:
    if ch.islower():
        idx = ALPHABET.index(ch)
        return ALPHABET[(idx + k) % M]
    if ch.isupper():
        idx = ALPHABET_UP.index(ch)
        return ALPHABET_UP[(idx + k) % M]
    return ch

def additive_encrypt(plaintext: str, key: int) -> str:
    key = key % M
    return ''.join(_shift_char_additive(c, key) for c in plaintext)

def additive_decrypt(ciphertext: str, key: int) -> str:
    return additive_encrypt(ciphertext, -key)

def additive_bruteforce(ciphertext: str) -> List[Tuple[int, str]]:
    results = []
    for k in range(M):
        pt = additive_decrypt(ciphertext, k)
        results.append((k, pt))
    return results


#! ---------- Multiplicative cipher helpers ----------
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def modinv(a: int, m: int) -> Optional[int]:
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def _mult_char(ch: str, a: int) -> str:
    if ch.islower():
        idx = ALPHABET.index(ch)
        return ALPHABET[(a * idx) % M]
    if ch.isupper():
        idx = ALPHABET_UP.index(ch)
        return ALPHABET_UP[(a * idx) % M]
    return ch

def multiplicative_encrypt(plaintext: str, a: int) -> str:
    a = a % M
    return ''.join(_mult_char(c, a) for c in plaintext)

def multiplicative_decrypt(ciphertext: str, a: int) -> str:
    a = a % M
    inv = modinv(a, M)
    if inv is None:
        raise ValueError(f"المفتاح a={a} غير قابل للعكس modulo {M} (gcd != 1).")
    return ''.join(_mult_char(c, inv) for c in ciphertext)

def multiplicative_bruteforce(ciphertext: str) -> List[Tuple[int, str]]:
    results = []
    for a in range(M):
        if modinv(a, M) is None:
            continue  
        try:
            pt = multiplicative_decrypt(ciphertext, a)
        except ValueError:
            continue
        results.append((a, pt))
    return results

if __name__ == "__main__":
    plain = "Hello, World! abc XYZ"
    print("=== Additive (shift) ===")
    k = 3
    c = additive_encrypt(plain, k)
    print("Plain :", plain)
    print(f"Encrypt (k={k}):", c)
    print("Decrypt:", additive_decrypt(c, k))
    print("Brute force sample (first 6 results):")
    for key, candidate in additive_bruteforce(c)[:6]:
        print(key, candidate)

    print("\n=== Multiplicative ===")
    a = 5  
    c2 = multiplicative_encrypt(plain, a)
    print("Plain :", plain)
    print(f"Encrypt (a={a}):", c2)
    print("Decrypt:", multiplicative_decrypt(c2, a))
    print("Brute force results:")
    for key, candidate in multiplicative_bruteforce(c2):
        print(key, candidate)
