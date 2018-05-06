#!/usr/bin/env python3

# Action => Consequence
MSG = {b"Line Finished": b"Add Line", 
       b"Game Over": b"Game Over"}

import socket
import logging

class TetrisServer:
    def __init__(self, ip="localhost", port=9090):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        logging.info(f"[*] Server is listening on {ip}:{port}")
        self.server.listen(2)
        self.clients = self.get_clients()

    def get_clients(self):
        logging.info("[*] Waiting for players....")
        clients, client_id = {}, 0
        while client_id < 2:
            conn, addr = self.server.accept()
            logging.info(f"[*] Connection from {addr}, CleintID {client_id}")
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
                        logging.info(f"[*] Recieved {msg}")
                        client_id = int(not client_id)
                        self.clients[client_id].send(MSG[msg])
                        logging.info(f"[*] Send to other client {MSG[msg]}")
                        game_over = msg == b"Game Over"
        except KeyboardInterrupt:
            logging.info("[!] Exiting")
        except Exception as error:
            logging.error(f"[!] Debugging Error\n[!] {error}")
        finally:
            self.close()

    def close(self):
        try:
            self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()
            logging.info("[*] Server has shutdown")
        except Exception as error:
            logging.error(f"[!] Debugging Error\n[!] {error}")

def logconfig():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='tetris_server.log',
                        filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == "__main__":
    logging.getLogger(__name__)
    logconfig()
    t_server = TetrisServer()
    t_server.start_game()
