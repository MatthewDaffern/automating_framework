from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

message = str.encode('test')


key = get_random_bytes(16)
old_cipher = AES.new(key, AES.MODE_EAX)
old_ciphertext, tag = old_cipher.encrypt_and_digest(message)

result  = (old_cipher.nonce, tag, old_ciphertext)

print(result)

from Crypto.Cipher import AES

new_nonce = result[0]
tag = result[1]
new_ciphertext = [result[2]]


# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, new_nonce)
data = cipher.decrypt_and_verify(new_ciphertext, tag)

print(bytes.decode())