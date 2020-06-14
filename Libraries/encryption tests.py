from hashlib import sha3_256
from Crypto.Cipher import AES

message = str.encode('test')
hash_object = sha3_256(message)

key = hash_object.digest()
old_cipher = AES.new(key, AES.MODE_EAX)
old_ciphertext = old_cipher.encrypt_and_digest(message)

result = (old_cipher.nonce, old_ciphertext)

print(result)

from Crypto.Cipher import AES

new_nonce = result[0]
new_ciphertext = result[1]


# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, new_nonce)
print(str(type(new_ciphertext)))
data = cipher.decrypt(new_ciphertext)

print(bytes.decode(data))