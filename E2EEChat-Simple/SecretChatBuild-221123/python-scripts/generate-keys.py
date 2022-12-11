from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')


# 32바이트 (256비트) 랜덤 비밀키 생성
# 아스키 변환 에러 핸들링
bytes = bytearray(Random.get_random_bytes(32))
secret = bytearray([byte % 256 for byte in bytes])

# RSA 2048 키 생성 시작
Rsa = RSA.generate(2048)

# 공개키 export
pubkey = Rsa.public_key().exportKey()

# 개인키 export
prikey = Rsa.exportKey()

print(encode_base64(secret) + '\n')

print(encode_base64(pubkey) + '\n')
print(encode_base64(prikey) + '\n')
