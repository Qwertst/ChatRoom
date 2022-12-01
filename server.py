import threading
import socket

IP = "127.0.0.1"
PORT = 5050
HEADER_LEN = 64
FORMAT = "utf-8"

addr = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)

clients = []
users = []


def send_all(msg):
    for client in clients:
        client.send(msg)


def handle(client, nickname):
    while True:
        try:
            msg_len = client.recv(HEADER_LEN).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(FORMAT)
                if msg == "!exit":
                    client.send("You left the chat...")
                msg = f"[{nickname}] " + msg
                send_all(msg.encode(FORMAT))
        except:
            idx = clients.index(client)
            clients.pop(idx)
            users.pop(idx)
            client.close()
            send_all(f"{nickname} has left the chat...".encode(FORMAT))
            print(f"{nickname} has left the chat...")
            break


def start():
    server.listen()
    print("Starting server...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        users.append(nickname)
        clients.append(client)

        print(f"New user: {nickname}")
        send_all(f"{nickname} has joined the chat".encode(FORMAT))
        client.send("Welcome! Type !exit to leave.".encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()


start()
