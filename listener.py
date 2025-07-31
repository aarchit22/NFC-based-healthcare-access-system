import serial
from grant_access import grant_access

def listen_bluetooth(port):
    ser = serial.Serial(port, 9600)
    print("Listening for UID...")

    while True:
        if ser.in_waiting:
            uid = ser.readline().decode().strip()
            print(f"Received UID: {uid}")
            grant_access(uid)
