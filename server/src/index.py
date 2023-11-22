# Import modules.
import os
import json
import socket

from src._crypto import *
from src._utils import get_time
from src._handshake import handshake

# Server index.
def index(client_connection: socket.socket, client_address: str) -> None:
    # Set the permission variable.
    # The thread will be closed if the username or password is wrong,
    # so we jest use a global variable to see if the user is logged in.
    PERMISSION = False

    PWD = "/"

    # Handshake.
    client_public_key = handshake(client_connection)

    server_public_key = open("./keys/public_key.pem").read()
    server_private_key = open("./keys/private_key.pem").read()

    while True:
        # Get header.
        header = decrypt_receive(client_connection, server_private_key, decode=True)
        header = header.split()

        if header[0] != "LOGIN" and not PERMISSION:
            encrypt_send(client_connection, "304 Permission denined.".encode(), client_public_key)
            continue

        match header[0]:
            case "SEND":
                try:
                    print(f"Receive file \"{header[1]}\".")

                    # Get file contents.
                    with open("./data/" + PWD + header[1], "wb") as f:
                        data = decrypt_receive(client_connection, server_private_key, decode=False)
                        f.write(data)

                    # Send successed message.
                    encrypt_send(client_connection, "202 File received successfully.".encode(), client_public_key)

                except:
                    # Send failed message.
                    print(f"failed to receive file \"{header[1]}\".")
                    encrypt_send(client_connection, "302 Failed to receive file.".encode(), client_public_key)

            case "LS":
                temp = ""
                for file in os.listdir("./data/" + PWD):
                    temp += PWD + file + "\n"
                temp = temp[:-1]

                encrypt_send(client_connection, temp.encode(), client_public_key)

            case "CD":
                if PWD == "/" and header[1] in "..": header[1] = ""

                if os.path.exists("./data/" + PWD + header[1]):
                    PWD += header[1]
                    encrypt_send(client_connection, "201 OK".encode(), client_public_key)
                else:
                    encrypt_send(client_connection, "304 Permission denined".encode(), client_public_key)

            case "LOGIN":
                # Skip if user already logged in.
                if PERMISSION:
                    encrypt_send(client_connection, "305 Already logged in.".encode(), client_public_key)
                    continue

                username, password = header[1:3]
                users = json.load(open("./user/user.json", "r"))
                
                if username not in users or password != users[username]["password"]:
                    encrypt_send(client_connection, "304 Permission denined.".encode(), client_public_key)

                    print(f"[{get_time()}] <<< Login failed. Close connection.")

                    # Close connection and exit if username or password is wrong.
                    client_connection.close()
                    exit(-1)

                # Send successed message.
                encrypt_send(client_connection, "204 Login successfully.".encode(), client_public_key)
                print(f"[{get_time()}] <<< User \"{username}\" login successfully from IP \"{client_address}\".")

                # Set the PERMISSION variable to True.
                # Notice that the PERMISSION can only be changed here.
                PERMISSION = True

            case _: continue

    # Close connection.
    client_connection.close()