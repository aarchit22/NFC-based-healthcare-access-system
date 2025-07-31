import os
from cryptography.fernet import Fernet

def generate_key(uid):
    # Ensure the keys directory exists
    if not os.path.exists("keys"):
        os.makedirs("keys")

    key = Fernet.generate_key()
    with open(f"keys/{uid}.key", "wb") as f:
        f.write(key)
    return key
