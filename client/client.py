# Import modules.
import socket

from src._cli import cli
from src._handshake import handshake

params = cli()
HOST = params["host"]
PORT = params["port"]

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((HOST, PORT))

except Exception as e:
    print("Failed tp connect to server. Please check the error messages:")
    print(str(e))

    exit(-1)

handshake(server_socket)

while True:
    try:
        filename = input('Input filename you want to send: ')
        fi = open(filename, "r")
        data = fi.read()
        if not data:
            break
        server_socket.send(str(len(data)).encode())
        server_socket.send(str(data).encode())
        server_socket.send("EOF".encode())
        fi.close()
    
    except KeyboardInterrupt: break
    except: continue
    
server_socket.send("EOF".encode())
server_socket.close()