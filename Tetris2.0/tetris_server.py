#!/usr/bin/python3

import socket

class TetrisServer:
    def __init__(self, ip="localhost", port=9090):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        print(f"[*] Server is listening on {ip}:{port}")
        self.server.listen(2)
        self.clients = []

    def get_clients(self):
        print("[*] Waiting for players....")
        while len(self.clients) < 2:
            conn, addr = self.server.accept()
            print(f"[*] Connection from {addr}")
            self.clients.append(conn)

    def recv(self, conn):
        msg = conn.recv(1024)
        return msg

    def send(self, conn, msg):
        conn.sendall(msg.encode())

    def start_game(self):
        try:
            while True:
                for conn in self.clients:
                    msg = self.recv(conn)
                    if msg:
                        print(f"[*] Recieved message: {msg}")
                        self.send(conn, "I have recieved you")
                        print("[*] Send reply")
        except KeyboardInterrupt as error:
            print("here has KeyboardInterrupt")
            print(error)
        except Exception as error:
            print("some else error")
            print(error)

    def close(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print("[*] Server has shutdown")

if __name__ == "__main__":
    t_server = TetrisServer()
    t_server.get_clients()
    t_server.start_game()
    t_server.close()
