import socket

client = socket.socket()

serv_addr = "127.0.0.1"
port = 1337

try:
    client.connect((serv_addr, port))
except Exception as e:
    print("[Error] Is The Host Really Up? Try Checking The Host And Port.")

data = client.recv(1024).decode()
print(data)

client.close()