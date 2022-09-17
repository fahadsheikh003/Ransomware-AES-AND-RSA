from os import walk, rename
from os.path import join, exists
from Crypto.Cipher import AES

class Decryptor:
    def __init__(self) -> None:
        # checking if decrypted_session_key (decrypted AES symmetric key) exists or not
        if not exists("decrypted_session_key"):
            print("'decrypted_session_key' not found..")
            exit(1)

        # loading decrypted AES symmetric key
        with open("decrypted_session_key", "rb") as f:
            self.session_key = f.read(32)

    # to decrypt a file
    def decrypt_file(self, file):

        with open(file, "rb") as f:
            nonce = f.read(16) # 16 bytes
            tag = f.read(16) # 16 bytes
            data = f.read()

        cipher_aes = AES.new(self.session_key, AES.MODE_EAX, nonce)
        plaintext = cipher_aes.decrypt_and_verify(data, tag)

        # storing decrypted binary to file
        try:
            with open(file, "wb") as f:
                f.write(plaintext)
            rename(file, file[:-4]) # renaming file (to avaid re-decryption)
            print(file[:-4], "decrypted")
        except:
            print(file[:-4], "not decrypted")

    def decrypt_files(self, directory: str):
        # finding all the files in the directory recursively
        system = walk(directory, topdown=True)
        for root, dir, files in system:
            for file in files:
                if ".enc" in file: # if file is encrypted
                    file_path = join(root, file)
                    self.decrypt_file(file_path)
                    
dec = Decryptor()
dec.decrypt_files("mydirectory")
