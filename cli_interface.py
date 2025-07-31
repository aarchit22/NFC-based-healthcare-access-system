import os
from register_patient import register_patient
from view_data import view_data
from grant_access import grant_access
from bluetooth_listener import wait_for_uid
from add_records import add_medical_records  

def menu():
    while True:
        print("\n=== Smart Healthcare CLI ===")
        print("1. Register New Patient")
        print("2. View Patient Data")
        print("3. Add Medical Records")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            uid = wait_for_uid()
            cleaned_uid = uid.replace("ACK: UID ", "").strip()
            # Check if the patient is already registered by checking for the key file
            if os.path.exists(f"keys/{cleaned_uid}.key"):
                print(f"Patient with UID {cleaned_uid} is already registered.")
            else:
                name = input("Enter patient name: ")
                age = input("Enter patient age: ")
                disease = input("Enter diagnosis info: ")
                data = {"name": name, "age": age, "disease": disease}
                register_patient(uid, data)

        elif choice == "2":
            uid = wait_for_uid()  # Get UID via Bluetooth
            if grant_access(uid):  # Only view data if access is granted
                view_data(uid)  # View patient data

        elif choice == "3":
            uid = wait_for_uid()  # Get UID via Bluetooth
            if grant_access(uid):  # Grant access for the scanned UID
                add_medical_records(uid)  # Add additional medical records

        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()