# Import modules.
import socket
import threading

from src.index import index

try:
    # Create socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 22))
    server_socket.listen(1)

    # Server starting message.
    print(f"Thank you for using HFPT Server.")
    print(f"Press CTRL-C to stop server...")

except Exception as e:
    # Quit if server start failed.
    print(f"Server start failed. Here's the error messages:")
    print(str(e))

    exit(-1)

# Run server.
while True:
    try:
        # Accept client connections.
        client_connection, client_address = server_socket.accept()

        # Start new thread.
        threading.Thread(target=index, args=(client_connection, client_address[0], )).start()

    except KeyboardInterrupt: break
    except: continue

# Close socket and exit.
server_socket.close()

print("Server shutdown successfully.")

exit(0)