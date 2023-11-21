# Import modules.
import os
import sys
import socket

from time import sleep
from ._utils import get_time

from ._crypto import *

def get_param() -> dict:
    params = {
        "host": "127.0.0.1",
        "port": 22
    }

    for param in sys.argv[1:]:
        if param.startswith("--host="):
            params["host"] = param[7:]
        elif param.startswith("--port="):
            params["port"] = int(param[7:])

    return params

def cli(server_address: str, server_socket: socket.socket, server_public_key: str) -> None:
    client_private_key = open("./keys/private_key.pem").read()

    while True:
        try:
            command = input("HFTP Client > ")
            command = command.split()

            match command[0]:
                case "help":
                    print(f"help\tShow this help message.")

                case "sendf":
                    if not os.path.isfile(command[1]):
                        print(f"File \"{command[1]}\" not found.")
                    else:
                        print(f"Send file \"{command[1]}\" to server {server_address}...")

                        # Send Header.
                        header = str(f"SEND {command[1]}")
                        encrypt_send(server_socket, header.encode(), server_public_key)

                        # Wait.
                        sleep(0.1)

                        # Send data.
                        encrypt_send(server_socket, open(command[1], "rb").read(), server_public_key)

                        # Get response.
                        response = decrypt_receive(server_socket, client_private_key, decode=True)
                        if response.startswith("202"):
                            print(f"[{get_time()}] <<< File received.")
                        else:
                            print(f"[{get_time()}] <<< Failed to received file.")

                case "login":
                    username, password = command[1:3]
                    print(f"Login to server {server_address} as \"{username}\"...")

                    # Send header.
                    header = str(f"LOGIN {username} {password}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    if response.startswith("204"):
                        print(f"[{get_time()}] <<< Login successfully.")
                    else:
                        print(f"[{get_time()}] <<< Permission denied.")

                case _:
                    print(f"Command \"{command[0]}\" not found.")
                    print(f"Please type \"help\" to get more information.")
                
            print()
        
        except KeyboardInterrupt: break
        except: continue