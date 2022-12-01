import socket
import threading

IP = "127.0.0.1"
PORT = 5050
HEADER_LEN = 64
FORMAT = "utf-8"

addr = (IP, PORT)

nickname = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print("Error. Client shutting down...")
            client.close()
            break


def send():
    while True:
        msg = input('').encode("utf-8")
        msg_length = len(msg)
        msg_length = str(msg_length) + (' ' * (HEADER_LEN - msg_length))
        client.send(msg_length.encode("utf-8"))
        client.send(msg)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()
