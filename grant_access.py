import time
import json
import os

def grant_access(uid):
    # Clean the UID to remove any prefixes
    cleaned_uid = uid.replace("ACK: UID ", "").strip()
    
    # Check if the patient is registered by verifying the key file exists
    key_file = f"keys/{cleaned_uid}.key"
    if not os.path.exists(key_file):
        print(f"No patient registered with UID {cleaned_uid}.")
        return False  # indicate failure

    # Ensure the cache directory exists
    os.makedirs("cache", exist_ok=True)
    
    access_data = {"uid": cleaned_uid, "timestamp": time.time()}
    with open(f"cache/{cleaned_uid}.access", "w") as f:
        json.dump(access_data, f)
    print(f"Access granted to UID {cleaned_uid} for 6 hours.")
    return True  # indicate success