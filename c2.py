import socket

# Create a socket object
serv = socket.socket()

# Server IP address and port
ip_addr = '127.0.0.1'
port = 1337

try:
    # Bind the socket to the IP address and port
    serv.bind((ip_addr, port))
    print(f"[INFO] Successfully Binded To {ip_addr}:{port}")
except Exception as e:
    print("[ERROR] An Error Occurred While Trying To Bind! Do You Have The Permissions To Use That Port?")
    print(f"LOG:\n{e}")
    exit(1)

# Listen for incoming connections
serv.listen(5)

while True:
    # Accept a client connection
    client, c_addr = serv.accept()
    print(f"[Alert] Got Connection From {c_addr}")  # To Keep Track of All The Connected Clients

    # Receive and decode the client data
    client_data = client.recv(2048).decode()
    print("="*30)
    print(client_data)
    print("="*30)

    # Receive and decode more data from the client
    data = client.recv(2048).decode()
    print(data)

    # Close the client connection
    client.close()
