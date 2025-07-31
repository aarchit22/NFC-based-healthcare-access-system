import os
import json
from cryptography.fernet import Fernet
import time

def view_data(uid):
    # Clean the UID to remove any prefixes
    cleaned_uid = uid.replace("ACK: UID ", "").strip()

    # Check if the key file exists
    key_file = f"keys/{cleaned_uid}.key"
    if not os.path.exists(key_file):
        print(f"No patient registered with UID {cleaned_uid}.")
        return

    # Check if access is granted
    access_file = f"cache/{cleaned_uid}.access"
    if not os.path.exists(access_file):
        print("Access not granted.")
        return

    # Verify access time
    with open(access_file, "r") as f:
        access_data = json.load(f)
        if time.time() - access_data["timestamp"] > 6 * 3600:
            print("Access expired.")
            return

    # Decrypt and display patient data
    try:
        with open(key_file, "rb") as f:
            key = f.read()
        cipher = Fernet(key)

        with open(f"data/{cleaned_uid}.bin", "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data).decode()
        print(f"Patient Data for UID {cleaned_uid}: {decrypted_data}")
    except FileNotFoundError as e:
        print(f"Error: {e}")