# Import modules.
import os
import rsa
import socket

class crypt:
    def encrypt(self, message: str, public_key: str) -> bytes:
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        return rsa.encrypt(message, public_key)

    def decrypt(self, message: str, private_key: str) -> str:
        private_key = rsa.PrivateKey.load_pkcs1(private_key)
        return rsa.decrypt(message, private_key)

def generate_keypair(bits: int=2048) -> None:
    public_key, private_key = rsa.newkeys(bits)

    if not os.path.exists("./keys/public_key.pem"):
        with open("./keys/public_key.pem", "wb") as f: f.write(public_key.save_pkcs1("PEM"))
        with open("./keys/private_key.pem", "wb") as f: f.write(private_key.save_pkcs1("PEM"))

def encrypt_send(sockets: socket.socket, data: bytes, public_key: str) -> bool:
    offset = 0
    chunck = 117

    while offset < len(data):
        temp = crypt().encrypt(data[offset:offset+chunck], public_key)
        sockets.send(temp)

        offset += chunck

    sockets.send("EOF".encode())

    return True

def decrypt_receive(sockets: socket.socket, private_key: str, decode: bool=True) -> str|bytes:
    data = bytearray()
    offset = 0
    chunck = 128

    if decode: result = ""
    else: result = bytearray()

    while "EOF" not in str(data): data += sockets.recv(1024)
    data = data[:-3]

    while offset < len(data):
        try:
            d = crypt().decrypt(data[offset:offset+chunck], private_key)
        except Exception as e:
            print(str(e))

        if decode: result += d.decode()
        else: result += d

        offset += chunck

    return result