import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.113", 8080))

while True:

    data = input("[+] Client -> ")
    client.sendall(data.encode())

    if data.lower() == "exit":
        client.close()
        break

    data = client.recv(2048).decode()
    print(f"[+] Serve -> {data}")