from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def decode_base64(b64):
    return base64.b64decode(b64)
def encode_base64(p):
    return base64.b64encode(p).decode('ascii')
def read_from_base64():
    return [ decode_base64(input()), decode_base64(input()) ]

def decrypt_secret(secret, priKey):
    # PKCS#1 OAEP를 이용한 RSA 복호화 구현
    RSAkey = RSA.importKey(priKey)
    Rsa = PKCS1_OAEP.new(RSAkey)
    return Rsa.decrypt(secret)

[secret, prikey] = read_from_base64()
result = encode_base64(decrypt_secret(secret, prikey))

print(result)