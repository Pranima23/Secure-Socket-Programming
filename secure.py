from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto import Random

def generateRSAKey():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return private_key, public_key
    
    
def generateSessionKey():
        session_key = Random.new().read(AES.block_size)     #generating an aes key or a session key
        return session_key
    

def encryptSessionKey(session_key, c_public_key):
        rsa_encrypt = PKCS1_OAEP.new(c_public_key)
        enc_session_key = rsa_encrypt.encrypt(session_key)
        return enc_session_key
    

def decryptSessionKey(enc_session_key, c_private_key):
        rsa_decrypt = PKCS1_OAEP.new(c_private_key)
        session_key = rsa_decrypt.decrypt(enc_session_key)
        return session_key
    

def encryptData(data, session_key):
        pad = 16 - (len(data) % 16)
        data += bytes([pad]) * pad
        cipher_aes = AES.new(session_key, AES.MODE_CBC, session_key)
        ciphertext = cipher_aes.encrypt(data)
        return ciphertext
    
    
def decryptData(ciphertext, session_key):
        cipher_aes = AES.new(session_key, AES.MODE_CBC, session_key)
        plaintext = cipher_aes.decrypt(ciphertext)
        plaintext = plaintext[:-plaintext[-1]]
        return plaintext