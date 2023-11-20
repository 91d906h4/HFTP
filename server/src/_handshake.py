# Import modules.
import socket

from ._crypto import crypt

def handshake(client_connection: socket.socket) -> None:
    # Send welcome message.
    client_connection.send("200 Welcome to HFTP server.".encode())

    # Generate RSA keypairs.
    CRYPTER = crypt(1024)

    # Send RSA public key.
    client_connection.send(str(CRYPTER.public_key).encode())

    # Get client RSA public key.
    client_public_key = client_connection.recv(1024).decode()
    print(client_public_key)