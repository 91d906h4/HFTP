# Import modules.
import socket

from src._cli import cli
from src._crypto import *
from src._handshake import handshake

params = cli()
HOST = params["host"]
PORT = params["port"]

try:
    # Create socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((HOST, PORT))

except Exception as e:
    print("Failed tp connect to server. Please check the error messages:")
    print(str(e))

    exit(-1)

# Server handshake.
server_public_key = handshake(server_socket)

while True:
    try:
        filename = input('Input filename you want to send: ')

        f = open(filename, "rb")
        data = f.read()

        if not data: continue

        encrypt_send(server_socket, data, server_public_key)

        f.close()
    
    except KeyboardInterrupt: break
    except: continue
    
server_socket.send("EOF".encode())
server_socket.close()