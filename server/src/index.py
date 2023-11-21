# Import modules.
import socket

from src._crypto import *
from src._handshake import handshake

# Server index.
def index(client_connection: socket.socket, client_address: str) -> None:
    client_public_key = handshake(client_connection)

    server_public_key = open("./keys/public_key.pem").read()
    server_private_key = open("./keys/private_key.pem").read()

    request = "any"

    while request:
        request = decrypt_receive(client_connection, server_private_key, decode=True)
        print(request)

    # Close connection.
    client_connection.close()