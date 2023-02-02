import socket
from secure import Client, encryptData, decryptData

c = socket.socket()
client = Client()

c.connect(('localhost', 9989))
c.send(client.public_key.export_key())
enc_session_key = c.recv(2048)
session_key = client.decryptSessionKey(enc_session_key)

request = bytes(input(' -> '), "utf-8")
while request.lower().strip() != "bye":
    encrypted_request = encryptData(request, session_key)

    c.send(encrypted_request)

    encrypted_response = c.recv(2048)
    response = decryptData(encrypted_response, session_key)
    print("Server:", response.decode())
# response = c.recv(1024).decode()
# print(response)

# name = input("Enter your name")
# c.send(bytes(name, "utf-8"))
# msg = c.recv(1024).decode() #1024 is buffer size

# print(msg)