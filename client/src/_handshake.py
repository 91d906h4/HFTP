# Import modules.
import rsa
import socket

from ._error import error
from ._crypto import crypt

class PK:
    def __init__(self, n, e) -> None:
        self.n = ""
        self.e = ""

def handshake(server_socket: socket.socket) -> None:
    # Get welcome message.
    welcome_message = server_socket.recv(1024).decode()
    if not welcome_message: error(code="001", end=True)

    # Get server RSA public key.
    server_public_key = server_socket.recv(1024).decode()

    n, e = server_public_key[10:-1].split(", ")
    print(server_public_key)
    server_public_key = rsa.PublicKey(int(n), int(e))

    # Generate RSA Keypair.
    CRYPTER = crypt(1024)

    # Send RSA public key.
    server_socket.send(CRYPTER.encrypt(str(CRYPTER.private_key).encode(), server_public_key))