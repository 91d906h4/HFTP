# Import modules.
import os
import sys
import socket

from ._utils import *
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
    PWD = "/"

    client_private_key = open("./keys/private_key.pem").read()

    while True:
        try:
            command = input("HFTP Client > ")
            command = command.split()

            match command[0]:
                case "help":
                    help_message(command)

                case "pwd":
                    print(f"{PWD}")

                case "ls":
                    # Send Header.
                    header = str(f"LS {PWD}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    print(f"{response}")

                case "cd":
                    # Send Header.
                    header = str(f"CD {command[1]}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    response = response.split()

                    # Response code handler.
                    match response[0]:
                        # If "cd" command executed successfully, then update PWD.
                        case "201": PWD = response[1]
                        case _: print(f"[{get_time()}] <<< Permission denied.")

                case "get":
                    # Send Header.
                    header = str(f"GET {PWD + "/" + command[1]}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    response = response.split()

                    # Response code handler.
                    match response[0]:
                        # If "cd" command executed successfully, then update PWD.
                        case "201":
                            print(f"[{get_time()}] <<< Received file.")
                            # Get file contents.
                            with open("./data/" + PWD + "/" + command[1], "wb") as f:
                                data = decrypt_receive(server_socket, client_private_key, decode=False)
                                f.write(data)

                        case _:
                            print(f"[{get_time()}] <<< Permission denied.")
                            decrypt_receive(server_socket, client_private_key, decode=True)

                case "sendf":
                    if not os.path.isfile("./data" + PWD + command[1]):
                        print(f"File \"{command[1]}\" not found.")
                        continue

                    print(f"Send file \"{command[1]}\" to server {server_address}...")

                    # Send Header.
                    header = str(f"SEND {command[1]}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Wait.
                    sleep(0.1)

                    # Send data.
                    encrypt_send(server_socket, open("./data" + PWD + command[1], "rb").read(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    response = response.split()

                    # Response code handler.
                    match response[0]:
                        case "202": print(f"[{get_time()}] <<< File received.")
                        case "304":
                            print(f"[{get_time()}] <<< Permission denied.")
                            print(f"Are you logged in?")
                        case _: print(f"[{get_time()}] <<< Failed to received file.")

                case "sendd":
                    if not os.path.isdir("./data" + PWD + command[1]):
                        print(f"Directory \"{command[1]}\" not found.")
                        continue

                    for filename in os.listdir("./data" + PWD + command[1]):
                        filename = command[1] + "/" + filename

                        print(f"Send file \"{filename}\" to server {server_address}...")

                        # Send Header.
                        header = str(f"SEND {filename}")
                        encrypt_send(server_socket, header.encode(), server_public_key)

                        # Wait.
                        sleep(0.1)

                        # Send data.
                        encrypt_send(server_socket, open("./data" + PWD + filename, "rb").read(), server_public_key)

                        # Get response.
                        response = decrypt_receive(server_socket, client_private_key, decode=True)
                        response = response.split()

                        # Response code handler.
                        match response[0]:
                            case "202": print(f"[{get_time()}] <<< File received.")
                            case "304":
                                print(f"[{get_time()}] <<< Permission denied.")
                                print(f"Are you logged in?")
                                # Break files iteration.
                                break
                            case _: print(f"[{get_time()}] <<< Failed to received file.")

                case "login":
                    username, password = command[1:3]
                    print(f"Login to server {server_address} as \"{username}\"...")

                    # Send header.
                    header = str(f"LOGIN {username} {password}")
                    encrypt_send(server_socket, header.encode(), server_public_key)

                    # Get response.
                    response = decrypt_receive(server_socket, client_private_key, decode=True)
                    response = response.split()

                    match response[0]:
                        case "204": print(f"[{get_time()}] <<< Login successfully.")
                        case "305": print(f"[{get_time()}] <<< Already logged in.")
                        case _:
                            print(f"[{get_time()}] <<< Permission denied.")
                            break

                case _:
                    print(f"Command \"{command[0]}\" not found.")
                    print(f"Please type \"help\" to get more information.")
                
            print()
        
        except KeyboardInterrupt: break
        except: continue