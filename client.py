import socket
from secure import *


def client():
    private_key, public_key = generateRSAKey()


    c = socket.socket()
    c.connect(('localhost', 9995))
    
    # send client's public key to receive an encrypted session key from server
    c.send(public_key.export_key())
    enc_session_key = c.recv(2048)
    
    #only client's private key can decrypt the encrypted session key
    session_key = decryptSessionKey(enc_session_key, private_key) 

    # message from client to server
    request = bytes(input('Client -> '), "utf-8")
    while request.lower().strip() != b"bye":
        encrypted_request = encryptData(request, session_key)
        c.send(encrypted_request)

        # message from server to client
        encrypted_response = c.recv(2048)
        response = decryptData(encrypted_response, session_key)
        print("Server:", response.decode())

        request = bytes(input('Client -> '), "utf-8")

if __name__ == "__main__":
    client()