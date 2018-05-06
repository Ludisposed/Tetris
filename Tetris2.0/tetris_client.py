#!/usr/bin/env python3

import socket
from time import sleep
from random import choice

# The server will be started on 127.0.0.1:9999
IP = "localhost"
PORT = 9090
MESSAGES = [b"Line Finished", b"Game Over"]

class GameClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        try:
            self.client.connect((ip, port))
        except Exception as error:
            print(f"[!] Connecting Failed\n[!] {error}")

    def game_loop(self):
        game_over = False
        try:
            while not game_over:
                sleep(choice(range(3, 10)))
                sending_msg = choice(MESSAGES)
                self.client.send(sending_msg)
                msg = self.client.recv(1024)
                game_over = msg == b"Game Over" or sending_msg == b"Game Over"
                print(f"[*] Sending {sending_msg}\n[*] Recieved {msg}")
        except Exception as error:
            print(f"[!] Error Encountered\n[!] {error}")
        finally:
            self.client.close()

if __name__ == "__main__":
    client = GameClient()
    client.connect(IP, PORT)
    client.game_loop()
