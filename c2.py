import socket
import logging

# Server IP address and port
ip_addr = '127.0.0.1'
port = 1337

# Create a socket object
serv = socket.socket()

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

    # Get the client's IP address
    client_ip = c_addr[0]

    # Configure logging to write to a file with the client's IP as the filename
    log_filename = f"{client_ip}.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s | %(message)s')

    logging.info(f"[Alert] Got Connection From {c_addr}")
    logging.info("=" * 30)

    # Receive and decode the client data
    while True:
        data = client.recv(2048).decode()
        if not data:
            break
        if "[Client] Transfer Completed!" in data:
            break

        # Print received data and log it
        print(data)
        logging.info(data)

    # Close the client connection
    client.close()
