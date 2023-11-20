# Import modules.
import rsa

class crypt:
    def __init__(self, bits: int=2048) -> None:
        self.public_key, self.private_key = rsa.newkeys(bits)

    def encrypt(self, message: str, public_key: dict) -> bytes:
        return rsa.encrypt(message, public_key)

    def decrypt(self, message: str) -> str:
        return rsa.decrypt(message, self.private_key).decode()