import socket

client = socket.socket()

serv_addr = "127.0.0.1"
port = 1337

client.connect((serv_addr, port))

data = client.recv(1024).decode()
print(data)

client.close()