import os
import json
from cryptography.fernet import Fernet

def add_medical_records(uid):
    # Clean the UID to remove any prefixes
    cleaned_uid = uid.replace("ACK: UID ", "").strip()

    # Check if the key file exists
    key_file = f"keys/{cleaned_uid}.key"
    if not os.path.exists(key_file):
        print(f"No patient registered with UID {cleaned_uid}.")
        return

    # Check if the data file exists
    data_file = f"data/{cleaned_uid}.bin"
    if not os.path.exists(data_file):
        print(f"No medical records found for UID {cleaned_uid}.")
        return

    # Decrypt the existing data
    try:
        with open(key_file, "rb") as f:
            key = f.read()
        cipher = Fernet(key)

        with open(data_file, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = json.loads(cipher.decrypt(encrypted_data).decode())
    except Exception as e:
        print(f"Error decrypting data: {e}")
        return

    # Display existing data
    print(f"Existing Medical Records for UID {cleaned_uid}: {decrypted_data}")

    # Add new medical records
    new_disease = input("Enter new diagnosis info: ")
    if "additional_records" not in decrypted_data:
        decrypted_data["additional_records"] = []
    decrypted_data["additional_records"].append(new_disease)

    # Re-encrypt and save the updated data
    try:
        updated_data = cipher.encrypt(json.dumps(decrypted_data).encode())
        with open(data_file, "wb") as f:
            f.write(updated_data)
        print(f"New medical records added for UID {cleaned_uid}.")
    except Exception as e:
        print(f"Error saving updated data: {e}")