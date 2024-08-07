import socket
from threading import Thread
import sys

class ChatServer:
    def __init__(self, ip = "127.0.0.1", host=9090) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip
        self.host_address = host
        self.socket.bind((ip, host))
        self.client_connections = {}
        
    def listen(self)->None:
        self.socket.listen()
        
    def accept(self):
        while True:
            connection, address = self.socket.accept()
            print(f"client {address} connected!")
            self.client_connections[address] = connection
            thread = Thread(target=self.handle_connection, args=(connection, address))
            thread.start()
        
    def broad_cast(self, data, client_address):
        for add, conn in self.client_connections.items():
            if add != client_address :
                conn.sendall(f"{client_address}:{data}".encode())
                
    def handle_connection(self, client_connection:str, client_address:str):
        while True:
            data = client_connection.recv(1024)
            data = data.decode()  
            if data == "q" or data == "quit":
                del self.client_connections[client_address]
                self.broad_cast(f"{client_address} left the chat!", client_address)
                sys.exit()
            else:
                print(f"{client_address}: {data}")
                self.broad_cast(data, client_address)
        self.close()
        
    def close(self):
        self.socket.close()