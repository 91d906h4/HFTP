# Import modules.
import socket

from ._crypto import *
from ._error import error
from ._utils import get_time

def handshake(server_socket: socket.socket) -> str:
    # Get welcome message.
    print(f"[{get_time()}] <<< Get \"Welcome message\".")
    welcome_message = server_socket.recv(1024).decode()
    if not welcome_message: error(code="001", end=True)
    else: print(welcome_message)

    # Get server RSA public key.
    print(f"[{get_time()}] <<< Get Server RSA public key.")
    server_public_key = server_socket.recv(1024).decode()

    # Generate RSA Keypair.
    generate_keypair(1024)
    client_public_key = open("./keys/public_key.pem").read()
    client_private_key = open("./keys/private_key.pem").read()

    # Send RSA public key.
    print(f"[{get_time()}] >>> Send RSA public key.")
    encrypt_send(server_socket, client_public_key.encode(), server_public_key)

    # Get random number.
    print(f"[{get_time()}] <<< Recieved random number.")
    ans = decrypt_receive(server_socket, client_private_key)

    # Send back random number.
    print(f"[{get_time()}] >>> Send random number.")
    server_socket.send(str(ans).encode())

    # Get accept/denined message.
    response = server_socket.recv(1024).decode()
    if not response.startswith("201"):
        print(f"[{get_time()}] <<< Connection denied.")
        print("Server denied the connection. Please try again later.")
        exit(-1)
    else:
        print(f"[{get_time()}] <<< Connection accepted.")

    return server_public_key