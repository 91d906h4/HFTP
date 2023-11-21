# Import modules.
import os
import sys
import socket

from time import sleep

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
                        print(f"Send file \"{command[1]}\" to server {server_address}.")

                        # Send Header.
                        header = str(f"SEND {command[1]}")
                        encrypt_send(server_socket, header.encode(), server_public_key)

                        # Wait.
                        sleep(0.1)

                        # Send data.
                        encrypt_send(server_socket, open(command[1], "rb").read(), server_public_key)

                case _:
                    print(f"Command \"{command[0]}\" not found.")
                    print(f"Please type \"help\" to get more information.")
                
            print()
        
        except KeyboardInterrupt: break
        except: continue