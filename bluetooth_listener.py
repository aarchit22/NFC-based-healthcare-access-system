import serial
import time

def wait_for_uid():
    # Wait until the Bluetooth connection is available.
    while True:
        try:
            print("Waiting for Bluetooth connection to HC05 on COM10...")
            ser = serial.Serial('COM10', 9600, timeout=10)
            break  # If the port opened successfully, exit the loop.
        except serial.serialutil.SerialException as e:
            print("Bluetooth not connected. Retrying in 5 seconds...")
            time.sleep(5)
    
    # Now wait for an NFC tag to be scanned.
    while True:
        line = ser.readline().decode().strip()
        if line:
            print(f"✅ Tag Scanned! Received UID: {line}")
            return line
        else:
            print("⚠️ No UID received. Make sure the NFC tag is close enough.")