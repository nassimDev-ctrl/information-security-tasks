"""
API لتشفير وفك التشفير باستخدام مختلف المشفرات
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# إضافة مسار مجلد المشفرات إلى المسار
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Information security'))

# استيراد جميع المشفرات
from classical_ciphers import (
    additive_encrypt, additive_decrypt, additive_bruteforce,
    multiplicative_encrypt, multiplicative_decrypt, multiplicative_bruteforce
)
from playfair_cipher import playfair_encrypt, playfair_decrypt
from polyalphabetic_ciphers import vigenere_encrypt, vigenere_decrypt, autokey_encrypt, autokey_decrypt
from adfgvx_cipher import adfgvx_encrypt, adfgvx_key_matrix
from rc4_cipher import rc4_keystream, keystream_to_bits, binary_derivative_test, change_point_test
from des_key_schedule import des_generate_subkeys

app = FastAPI(
    title="Cipher API",
    description="API شامل لاستخدام مختلف المشفرات الكلاسيكية والحديثة",
    version="1.0.0"
)


# ========== نماذج البيانات ==========

class EncryptRequest(BaseModel):
    plaintext: str = Field(..., description="النص المراد تشفيره")
    key: str = Field(..., description="المفتاح")


class DecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="النص المشفر")
    key: str = Field(..., description="المفتاح")


class AdditiveEncryptRequest(BaseModel):
    plaintext: str = Field(..., description="النص المراد تشفيره")
    key: int = Field(..., ge=0, le=25, description="المفتاح (رقم من 0 إلى 25)")


class AdditiveDecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="النص المشفر")
    key: int = Field(..., ge=0, le=25, description="المفتاح (رقم من 0 إلى 25)")


class MultiplicativeEncryptRequest(BaseModel):
    plaintext: str = Field(..., description="النص المراد تشفيره")
    key: int = Field(..., ge=1, le=25, description="المفتاح (رقم من 1 إلى 25)")


class MultiplicativeDecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="النص المشفر")
    key: int = Field(..., ge=1, le=25, description="المفتاح (رقم من 1 إلى 25)")


class BruteforceRequest(BaseModel):
    ciphertext: str = Field(..., description="النص المشفر")


class RC4Request(BaseModel):
    key: str = Field(..., description="المفتاح")
    length: int = Field(..., ge=1, le=10000, description="طول المفتاح المطلوب")


class DESRequest(BaseModel):
    hex_key: str = Field(..., description="المفتاح بصيغة hexadecimal (16 حرف)")


# ========== Classical Ciphers ==========

@app.post("/classical/additive/encrypt", tags=["Classical Ciphers"])
async def encrypt_additive(request: AdditiveEncryptRequest):
    """تشفير باستخدام Additive (Caesar) Cipher"""
    try:
        result = additive_encrypt(request.plaintext, request.key)
        return {"plaintext": request.plaintext, "key": request.key, "ciphertext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/classical/additive/decrypt", tags=["Classical Ciphers"])
async def decrypt_additive(request: AdditiveDecryptRequest):
    """فك التشفير باستخدام Additive (Caesar) Cipher"""
    try:
        result = additive_decrypt(request.ciphertext, request.key)
        return {"ciphertext": request.ciphertext, "key": request.key, "plaintext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/classical/additive/bruteforce", tags=["Classical Ciphers"])
async def bruteforce_additive(request: BruteforceRequest):
    """محاولة فك التشفير باستخدام جميع المفاتيح الممكنة (0-25)"""
    try:
        results = additive_bruteforce(request.ciphertext)
        return {
            "ciphertext": request.ciphertext,
            "results": [{"key": k, "plaintext": pt} for k, pt in results]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/classical/multiplicative/encrypt", tags=["Classical Ciphers"])
async def encrypt_multiplicative(request: MultiplicativeEncryptRequest):
    """تشفير باستخدام Multiplicative Cipher"""
    try:
        result = multiplicative_encrypt(request.plaintext, request.key)
        return {"plaintext": request.plaintext, "key": request.key, "ciphertext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/classical/multiplicative/decrypt", tags=["Classical Ciphers"])
async def decrypt_multiplicative(request: MultiplicativeDecryptRequest):
    """فك التشفير باستخدام Multiplicative Cipher"""
    try:
        result = multiplicative_decrypt(request.ciphertext, request.key)
        return {"ciphertext": request.ciphertext, "key": request.key, "plaintext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/classical/multiplicative/bruteforce", tags=["Classical Ciphers"])
async def bruteforce_multiplicative(request: BruteforceRequest):
    """محاولة فك التشفير باستخدام جميع المفاتيح الممكنة"""
    try:
        results = multiplicative_bruteforce(request.ciphertext)
        return {
            "ciphertext": request.ciphertext,
            "results": [{"key": k, "plaintext": pt} for k, pt in results]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== Playfair Cipher ==========

@app.post("/playfair/encrypt", tags=["Playfair Cipher"])
async def encrypt_playfair(request: EncryptRequest):
    """تشفير باستخدام Playfair Cipher"""
    try:
        result = playfair_encrypt(request.plaintext, request.key)
        return {"plaintext": request.plaintext, "key": request.key, "ciphertext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/playfair/decrypt", tags=["Playfair Cipher"])
async def decrypt_playfair(request: DecryptRequest):
    """فك التشفير باستخدام Playfair Cipher"""
    try:
        result = playfair_decrypt(request.ciphertext, request.key)
        return {"ciphertext": request.ciphertext, "key": request.key, "plaintext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== Polyalphabetic Ciphers ==========

@app.post("/polyalphabetic/vigenere/encrypt", tags=["Polyalphabetic Ciphers"])
async def encrypt_vigenere(request: EncryptRequest):
    """تشفير باستخدام Vigenere Cipher"""
    try:
        result = vigenere_encrypt(request.plaintext, request.key)
        return {"plaintext": request.plaintext, "key": request.key, "ciphertext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/polyalphabetic/vigenere/decrypt", tags=["Polyalphabetic Ciphers"])
async def decrypt_vigenere(request: DecryptRequest):
    """فك التشفير باستخدام Vigenere Cipher"""
    try:
        result = vigenere_decrypt(request.ciphertext, request.key)
        return {"ciphertext": request.ciphertext, "key": request.key, "plaintext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/polyalphabetic/autokey/encrypt", tags=["Polyalphabetic Ciphers"])
async def encrypt_autokey(request: EncryptRequest):
    """تشفير باستخدام AutoKey Cipher"""
    try:
        result = autokey_encrypt(request.plaintext, request.key)
        return {"plaintext": request.plaintext, "key": request.key, "ciphertext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/polyalphabetic/autokey/decrypt", tags=["Polyalphabetic Ciphers"])
async def decrypt_autokey(request: DecryptRequest):
    """فك التشفير باستخدام AutoKey Cipher"""
    try:
        result = autokey_decrypt(request.ciphertext, request.key)
        return {"ciphertext": request.ciphertext, "key": request.key, "plaintext": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== ADFGVX Cipher ==========

@app.post("/adfgvx/encrypt", tags=["ADFGVX Cipher"])
async def encrypt_adfgvx(request: EncryptRequest):
    """تشفير باستخدام ADFGVX Cipher"""
    try:
        result = adfgvx_encrypt(request.plaintext, request.key)
        matrix = adfgvx_key_matrix(request.key)
        return {
            "plaintext": request.plaintext,
            "key": request.key,
            "ciphertext": result,
            "key_matrix": matrix
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== RC4 Cipher ==========

@app.post("/rc4/keystream", tags=["RC4 Cipher"])
async def generate_rc4_keystream(request: RC4Request):
    """إنشاء RC4 keystream"""
    try:
        keystream = rc4_keystream(request.key, request.length)
        bits = keystream_to_bits(keystream)
        derivative = binary_derivative_test(bits)
        changes = change_point_test(bits)
        
        return {
            "key": request.key,
            "length": request.length,
            "keystream_bytes": keystream,
            "keystream_binary": bits,
            "binary_derivative": derivative,
            "change_point_count": changes
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== DES Key Schedule ==========

@app.post("/des/subkeys", tags=["DES"])
async def generate_des_subkeys(request: DESRequest):
    """إنشاء DES subkeys من المفتاح"""
    try:
        if len(request.hex_key) != 16:
            raise ValueError("المفتاح يجب أن يكون 16 حرف hexadecimal")
        
        subkeys = des_generate_subkeys(request.hex_key)
        return {
            "hex_key": request.hex_key,
            "subkeys": [
                {"round": i + 1, "subkey": subkey}
                for i, subkey in enumerate(subkeys)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== Root Endpoint ==========

@app.get("/", tags=["General"])
async def root():
    """الصفحة الرئيسية - قائمة بجميع المشفرات المتاحة"""
    return {
        "message": "مرحباً بك في Cipher API",
        "available_ciphers": {
            "classical": {
                "additive": ["encrypt", "decrypt", "bruteforce"],
                "multiplicative": ["encrypt", "decrypt", "bruteforce"]
            },
            "playfair": ["encrypt", "decrypt"],
            "polyalphabetic": {
                "vigenere": ["encrypt", "decrypt"],
                "autokey": ["encrypt", "decrypt"]
            },
            "adfgvx": ["encrypt"],
            "rc4": ["keystream"],
            "des": ["subkeys"]
        },
        "documentation": "/docs",
        "alternative_docs": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

