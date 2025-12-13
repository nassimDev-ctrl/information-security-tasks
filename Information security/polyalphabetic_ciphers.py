
from typing import List

ALPH = "abcdefghijklmnopqrstuvwxyz"
ALPH_UP = ALPH.upper()
M = 26

def _is_alpha(ch: str) -> bool:
    return ch.isalpha()

def _char_to_index(ch: str) -> int:
    return ALPH.index(ch.lower())

def _index_to_char(idx: int, is_upper: bool) -> str:
    idx %= M
    return ALPH_UP[idx] if is_upper else ALPH[idx]

def _sanitize_key(key: str) -> str:
    return ''.join(ch.lower() for ch in key if ch.isalpha())


# ---------- Vigenere ----------
def vigenere_encrypt(plaintext: str, key: str) -> str:
    
    key_clean = _sanitize_key(key)
    if not key_clean:
        raise ValueError("المفتاح لا يجوز أن يكون فارغاً أو لا يحتوي أحرفاً أبجدية.")
    out_chars: List[str] = []
    ki = 0  
    key_len = len(key_clean)

    for ch in plaintext:
        if not _is_alpha(ch):
            out_chars.append(ch)
            continue
        k = _char_to_index(key_clean[ki % key_len])
        c_idx = _char_to_index(ch)
        enc_idx = (c_idx + k) % M
        out_chars.append(_index_to_char(enc_idx, ch.isupper()))
        ki += 1

    return ''.join(out_chars)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    
    key_clean = _sanitize_key(key)
    if not key_clean:
        raise ValueError("المفتاح لا يجوز أن يكون فارغاً أو لا يحتوي أحرفاً أبجدية.")
    out_chars: List[str] = []
    ki = 0
    key_len = len(key_clean)

    for ch in ciphertext:
        if not _is_alpha(ch):
            out_chars.append(ch)
            continue
        k = _char_to_index(key_clean[ki % key_len])
        c_idx = _char_to_index(ch)
        dec_idx = (c_idx - k) % M
        out_chars.append(_index_to_char(dec_idx, ch.isupper()))
        ki += 1

    return ''.join(out_chars)


# ---------- AutoKey ----------
def autokey_encrypt(plaintext: str, key: str) -> str:
    
    key_clean = _sanitize_key(key)
    if not key_clean:
        raise ValueError("المفتاح لا يجوز أن يكون فارغاً أو لا يحتوي أحرفاً أبجدية.")

    plaintext_letters = [ch.lower() for ch in plaintext if _is_alpha(ch)]
    needed = len(plaintext_letters)
    keystream = (key_clean + ''.join(plaintext_letters))[:needed]

    out_chars: List[str] = []
    ki = 0 
    for ch in plaintext:
        if not _is_alpha(ch):
            out_chars.append(ch)
            continue
        k = _char_to_index(keystream[ki])
        p_idx = _char_to_index(ch)
        enc_idx = (p_idx + k) % M
        out_chars.append(_index_to_char(enc_idx, ch.isupper()))
        ki += 1

    return ''.join(out_chars)


def autokey_decrypt(ciphertext: str, key: str) -> str:
   
    key_clean = _sanitize_key(key)
    if not key_clean:
        raise ValueError("المفتاح لا يجوز أن يكون فارغاً أو لا يحتوي أحرفاً أبجدية.")

    keystream_letters: List[str] = list(key_clean)  
    out_chars: List[str] = []
    ki = 0  

    for ch in ciphertext:
        if not _is_alpha(ch):
            out_chars.append(ch)
            continue
        
        k = _char_to_index(keystream_letters[ki])
        c_idx = _char_to_index(ch)
        p_idx = (c_idx - k) % M
        p_char = _index_to_char(p_idx, False)  
        out_chars.append(_index_to_char(p_idx, ch.isupper()))
        keystream_letters.append(p_char)
        ki += 1

    return ''.join(out_chars)



if __name__ == "__main__":
    plain = "Attack at dawn! 123"
    v_key = "LEMON"
    print("=== Vigenere ===")
    c_v = vigenere_encrypt(plain, v_key)
    print("Plain :", plain)
    print("Key   :", v_key)
    print("Cipher:", c_v)
    print("Decrypt:", vigenere_decrypt(c_v, v_key))

    print("\n=== AutoKey ===")
    a_key = "QUEEN"
    c_a = autokey_encrypt(plain, a_key)
    print("Plain :", plain)
    print("Key   :", a_key)
    print("Cipher:", c_a)
    print("Decrypt:", autokey_decrypt(c_a, a_key))
