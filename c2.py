import socket 

serv = socket.socket()

ip_addr = '127.0.0.1'
port = 1337

try:
    serv.bind((ip_addr, port))
    print(f"[INFO] Successfully Binded To {ip_addr}:{port}")

except Exception as e:
    print("[ERROR] An Error Occured While Trying To Bind! Do You Have The Permissions To Use That Port?")
    exit(1)

serv.listen(5)
while True:
    client, c_addr = serv.accept()
    print(f"[Alert] Got Connection From {c_addr}")
    client.send('Successfully Connected To C2'.encode())
    client.close()