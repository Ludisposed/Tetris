#!/usr/bin/python3

# Action => Consequence
MSG = {b"Line Finished": b"Add Line", 
       b"Game Over": b"Game Over"}

import socket

class TetrisServer:
    def __init__(self, ip="localhost", port=9090):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        print(f"[*] Server is listening on {ip}:{port}")
        self.server.listen(2)
        self.clients = self.get_clients()

    def get_clients(self):
        print("[*] Waiting for players....")
        clients, client_id = {}, 0
        while client_id < 2:
            conn, addr = self.server.accept()
            print(f"[*] Connection from {addr}, CleintID {client_id}")
            clients[client_id] = conn
            client_id += 1
        return clients

    def start_game(self):
        game_over = False
        try:
            while not game_over:
                for client_id in self.clients.keys():
                    msg = self.clients[client_id].recv(1024)
                    if msg:
                        print(f"[*] Recieved {msg}")
                        client_id = int(not client_id)
                        self.clients[client_id].send(MSG[msg])
                        print(f"[*] Send to other client {MSG[msg]}")
                        game_over = msg == b"Game Over"
        except KeyboardInterrupt:
            print("[!] Exiting")
        except Exception as error:
            print(f"[!] Debugging Error\n[!] {error}")
        finally:
            self.close()

    def close(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print("[*] Server has shutdown")

if __name__ == "__main__":
    t_server = TetrisServer()
    t_server.start_game()
