import socket
from secure import Server, encryptData, decryptData
from Crypto.PublicKey import RSA

server = Server()
session_key = server.generateSessionKey()
s = socket.socket()
print('Socket created')

s.bind(('localhost', 9989))

s.listen(1) # establish connection with 1 client
print('waiting for connection')


c, addr = s.accept()

print('Connected with ', addr)

c_public_key = RSA.import_key(c.recv(2048)) 
print("Client's public key: ", c_public_key)
     
enc_session_key = server.encryptSessionKey(session_key, c_public_key)
c.send(bytes(enc_session_key))
    


while True:  
    encrypted_request = c.recv(2048)
    if not encrypted_request:
        break
    request = decryptData(encrypted_request, session_key)
    print("Client", str(request.decode()))
    
    response = bytes(input(" -> "), "utf-8")
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