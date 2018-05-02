#!/usr/bin/python3

import socket
from time import sleep
from random import choice

# The server will be started on 127.0.0.1:9999
IP = "localhost"
PORT = 9090
MESSAGES = ["Qin is sexy", "Whaaaat you are so pro!", "I fucking love python3"]

class GameClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        try:
            self.client.connect((ip, port))
        except:
            print("Connecting Failed")

    def close(self):
        self.client.close()

    def recv(self):
        msg = self.client.recv(1024)
        print(f"Recieved {msg}")

    def send(self, msg):
        self.client.send(msg.encode())

if __name__ == "__main__":
    client = GameClient()
    client.connect(IP, PORT)
    #sleep(choice(range(5, 10)))
    client.send(choice(MESSAGES))
    client.recv()
    client.close()
