# Import modules.
import socket

from src._cli import *
from src._crypto import *
from src._handshake import handshake

# Get parameters from command line.
params = get_param()
HOST = params["host"]
PORT = params["port"]

try:
    # Create socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((HOST, PORT))

except Exception as e:
    # Quit if client start failed.
    print("Failed tp connect to server. Please check the error messages:")
    print(str(e))

    exit(-1)

# Handshake.
server_public_key = handshake(server_socket)

# Enter CLI mode.
cli(HOST, server_socket, server_public_key)

# Close socket.
server_socket.close()

print("\nGoodbye.\n")

exit(0)