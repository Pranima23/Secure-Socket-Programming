import socket
from secure import Client, encryptData, decryptData

c = socket.socket()
client = Client()

c.connect(('localhost', 9998))
c.send(client.public_key.export_key())
enc_session_key = c.recv(1024)
print("Encrypted session key: ", enc_session_key)
session_key = client.decryptSessionKey(enc_session_key)

print("Decrypted session key: ", session_key)

request = b"Request"
encrypted_request = encryptData(request, session_key)

c.send(encrypted_request)

encrypted_response = c.recv(1024)
response = decryptData(encrypted_response, session_key)
print(response)
# response = c.recv(1024).decode()
# print(response)

# name = input("Enter your name")
# c.send(bytes(name, "utf-8"))
# msg = c.recv(1024).decode() #1024 is buffer size

# print(msg)