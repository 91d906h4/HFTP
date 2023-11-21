# Import modules.
import time
import json
import socket

from src._crypto import *
from src._handshake import handshake

# Server index.
def index(client_connection: socket.socket, client_address: str) -> None:
    # Handshake.
    client_public_key = handshake(client_connection)

    server_public_key = open("./keys/public_key.pem").read()
    server_private_key = open("./keys/private_key.pem").read()

    request = "any"

    while request:
        # Get header.
        header = decrypt_receive(client_connection, server_private_key, decode=True)
        header = header.split()

        match header[0]:
            # Get file from client.
            case "SEND":
                try:
                    print(f"Receive file \"{header[1]}\".")

                    # Get file contents.
                    with open(header[1], "wb") as f:
                        data = decrypt_receive(client_connection, server_private_key, decode=False)
                        f.write(data)

                    # Send successed message.
                    encrypt_send(client_connection, "202 File received successfully.".encode(), client_public_key)

                except:
                    # Send failed message.
                    print(f"failed to receive file \"{header[1]}\".")
                    encrypt_send(client_connection, "302 Failed to receive file.".encode(), client_public_key)

            case "LOGIN":
                username, password = header[1:3]

                # Send successed message.
                encrypt_send(client_connection, "304 Permission denined.".encode(), client_public_key)

            case _: continue

    # Close connection.
    client_connection.close()