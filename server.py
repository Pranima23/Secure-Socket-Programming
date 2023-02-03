import socket
from secure import *
from Crypto.PublicKey import RSA
import re

def sanitizeRequest(request):
    sanitized_request = re.sub(r'[^\w\s]', '', str(request.decode()))   # sanitize message
    return sanitized_request

def server():

    session_key = generateSessionKey()

    s = socket.socket()
    print('Socket created')
    s.bind(('localhost', 9999))

    s.listen(1)
    print('Waiting for connection...')

    c, addr = s.accept()
    print('Connected with ', addr)

    # to share session key using RSA
    c_public_key = RSA.import_key(c.recv(2048))      
    enc_session_key = encryptSessionKey(session_key, c_public_key)
    c.send(bytes(enc_session_key))
    
    
    while True:  
        # message from client to server
        encrypted_request = b""
        while True:
            chunk = c.recv(4096)
            encrypted_request += chunk
            if len(chunk)<2048:
                break
        if not encrypted_request:
            break
        request = decryptData(encrypted_request, session_key)
        sanitized_request = sanitizeRequest(request)
        print("Client", sanitized_request)
        
        # message from server to client
        response = bytes(input("Server -> ").encode())
        encrypted_response = encryptData(response, session_key)
        c.send(encrypted_response)
        
    c.close()

if __name__ == "__main__":
    server()