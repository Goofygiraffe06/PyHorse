import socket

serv = socket.socket()

ip_addr = '127.0.0.1'
port = 1337

try:
    serv.bind((ip_addr, port))
    print(f"[INFO] Successfully Binded To {ip_addr}:{port}")
except Exception as e:
    print("[ERROR] An Error Occurred While Trying To Bind! Do You Have The Permissions To Use That Port?")
    print(f"LOG:\n{e}")
    exit(1)

serv.listen(5)

while True:
    client, c_addr = serv.accept()
    print(f"[Alert] Got Connection From {c_addr}")  # To Keep Track of All The Connected Clients
    client.send('Successfully Connected To C2'.encode())  # Send an acknowledgement message to the client
    client_data = client.recv(2048).decode()  # Receive and decode the client data
    print(client_data)
    client.close()