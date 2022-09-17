# Ransomware-AES-AND-RSA

# This ransomware is implemented using pycryptodome module

**Hierarchy**
    
    Firstly, generate public and private keys RSA
    Then, change the directory in the encryptor.py and decryptor.py
    To encrypt files, run encryptor.py
    For decryption, run session_key_decryptor.py to decrypt AES symmetric key (that was used for encryption of files) with private key (that was generated in the first step)
    Now, just run decryptor.py to decrypt files in the specified directory
     
