from os.path import exists
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# checking if encrypted_session_key file exists or not
if not exists("encrypted_session_key"):
    print("file 'encrypted_session_key' not found..")
    exit(1)

# loading private key
with open("private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# instantiating RSA cipher with private key
cipher_rsa = PKCS1_OAEP.new(private_key)

# loading encrypted AES symmetric key
with open("encrypted_session_key", "rb") as f:
    enc_session_key = f.read(private_key.size_in_bytes())

# decrypting AES symmetric key
session_key = cipher_rsa.decrypt(enc_session_key)

# storing decrypted AES symmetric key
with open("decrypted_session_key", "wb") as f:
    f.write(session_key)