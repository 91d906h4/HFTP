# Import modules.
import socket
import random

from ._crypto import *
from ._utils import get_time

def handshake(client_connection: socket.socket) -> str:
    # Received connection.
    print(f"[{get_time()}] <<< Client Connection.")

    # Send welcome message.
    print(f"[{get_time()}] >>> Send \"Welcome Message\".")
    client_connection.send("200 Welcome to HFTP server.".encode())

    # Generate RSA keypairs.
    generate_keypair(1024)

    # Send RSA public key.
    print(f"[{get_time()}] >>> Send RSA public key.")
    server_public_key = open("./keys/public_key.pem").read()
    server_private_key = open("./keys/private_key.pem").read()
    client_connection.send(str(server_public_key).encode())

    # Get client RSA public key.
    print(f"[{get_time()}] <<< Received client RSA public key.")
    client_public_key = decrypt_receive(client_connection, server_private_key, decode=True)

    # Send random number.
    print(f"[{get_time()}] >>> Send random number.")
    ans = str(random.randint(0, 10000000))
    encrypt_send(client_connection, ans.encode(), client_public_key)

    # Get random number from client.
    print(f"[{get_time()}] <<< Get random number response.")
    c_ans = client_connection.recv(1024).decode()
    if ans == c_ans:
        print(f"[{get_time()}] >>> Connection accepted.")
        client_connection.send("201 Accept".encode())
    else:
        print(f"[{get_time()}] >>> Connection denied.")
        client_connection.send("301 Denied".encode())

    return client_public_key