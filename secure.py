from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto import Random

def generateRSAKey():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return private_key, public_key
    
    
def generateSessionKey():
        # session_key = get_random_bytes(16)
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

# class Server:
#     # _session_key = get_random_bytes(8)
#     # session_key = None
#     _private_key = RSA.generate(2048)
#     public_key = _private_key.publickey()
    
#     def generateSessionKey(self):
#         session_key = get_random_bytes(16)
#         # session_key = Random.new().read(AES.block_size)     #generating an aes key or a session key

#         return session_key

#     # def generateRsaKeyS(self):
#     #     s_private_key = RSA.generate(2048)
#     #     s_public_key = s_private_key.publickey()
#     #     return s_private_key, s_public_key
        
#     def encryptSessionKey(self, session_key, c_public_key):
#         rsa_encrypt = PKCS1_OAEP.new(c_public_key)
#         enc_session_key = rsa_encrypt.encrypt(session_key)
#         return enc_session_key
    
    # def encryptData(self, data, session_key):
    #     pad = 8 - (len(data) % 8)
    #     data += bytes([pad]) * pad
    #     cipher_des = DES.new(session_key, DES.MODE_CBC, session_key)
    #     ciphertext = cipher_des.encrypt(data)
    #     return ciphertext
    
        
        
# class Client:
#     _private_key = RSA.generate(2048)
#     public_key = _private_key.publickey()
#     _session_key = None
    
#     # def generateRsaKeyC(self):
#     #     c_private_key = RSA.generate(2048)
#     #     c_public_key = c_private_key.publickey()
#     #     return c_private_key, c_public_key
    
#     def decryptSessionKey(self, enc_session_key):
#         rsa_decrypt = PKCS1_OAEP.new(self._private_key)
#         session_key = rsa_decrypt.decrypt(enc_session_key)
#         return session_key
    
    # def decryptData(self, ciphertext, session_key):
    #     cipher_des = DES.new(session_key, DES.MODE_CBC, session_key)
    #     plaintext = cipher_des.decrypt(ciphertext)
    #     plaintext = plaintext[:-plaintext[-1]]

    #     return plaintext
        
# server = Server()
# client = Client()


# # sending session key from client to server
# c_public_key = client.public_key
# enc_session_key = server.encryptSessionKey(c_public_key)
# client.decryptSessionKey(enc_session_key)

# client = Client()

# server = Server()
# ciphertext = server.encryptData(b"hello", b'Q\x9aSC\xd1\xa9\x0e0')
# print(ciphertext)

# plaintext = client.decryptData(ciphertext, b'Q\x9aSC\xd1\xa9\x0e0')
# print(plaintext)