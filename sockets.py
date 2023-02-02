import socket
from secure import Server, encryptData, decryptData
from Crypto.PublicKey import RSA


s = socket.socket()
print('Socket created')

s.bind(('localhost', 9998))

s.listen(1) # establish connection with 3 client
print('waiting for connection')

server = Server()
session_key = server.generateSessionKey()


while True:

    c, addr = s.accept()
    print('Connected with ', addr)
    
    c_public_key = RSA.import_key(c.recv(1024)) 
    print("Client's public key: ", c_public_key)
     
    enc_session_key = server.encryptSessionKey(session_key, c_public_key)

    c.send(bytes(enc_session_key))
    
    encrypted_request = c.recv(1024)
    request = decryptData(encrypted_request, session_key)
    print(request)
    
    response = b"Response"
    encrypted_response = encryptData(response, session_key)
    c.send(encrypted_response)
    
    # c.send(b"Response")
    c.close()

# while True:
#     c, addr = s.accept()
#     cname = c.recv(1024).decode()
#     print("Connected with ", addr, cname)
#     # print(client_socket)
    
    
#     c.send(b"hiiiii")
    
#     c.close()