import socket

s = socket.socket()
print('Socket created')

s.bind(('localhost', 9999))

s.listen(3) # establish connection with 3 client
print('waiting for connection')

while True:
    client, addr = s.accept()
    cname = client.recv(1024).decode()
    print("Connected with ", addr, cname)
    # print(client_socket)
    
    client.send(b"hiiiii")
    
    client.close()