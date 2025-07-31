import os
from cryptography.fernet import Fernet
from keygen import generate_key
import json

def register_patient(uid, data):
    # Clean the UID to remove any prefixes
    cleaned_uid = uid.replace("ACK: UID ", "").strip()

    # Check if the UID is already registered
    key_file = f"keys/{cleaned_uid}.key"
    if os.path.exists(key_file):
        print(f"Error: A patient is already registered with UID {cleaned_uid}.")
        return

    print("Generating key...")
    key = generate_key(cleaned_uid)
    fernet = Fernet(key)

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    # Encrypt and store the patient's data
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(f"data/{cleaned_uid}.bin", "wb") as f:
        f.write(encrypted_data)
    print(f"Patient {cleaned_uid} registered successfully.")