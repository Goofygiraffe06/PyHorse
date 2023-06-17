import socket 

serv = socket.socket()

ip_addr = '127.0.0.1'
port = 1337

serv.bind((ip_addr, port))
print(f"[INFO] Successfully Binded To {ip_addr}:{port}")

serv.listen(5)
while True:
    client, c_addr = serv.accept()
    print(f"[Alert] Got Connection From {c_addr}")