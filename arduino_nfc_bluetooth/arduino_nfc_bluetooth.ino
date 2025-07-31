#include <Wire.h>
#include <Adafruit_PN532.h>
#include <SoftwareSerial.h>

// Define PN532 pins for I2C mode
#define PN532_IRQ   2   // Connect PN532 IRQ to Arduino digital pin 2
#define PN532_RESET 3   // Connect PN532 RESET to Arduino digital pin 3

// Create an instance for PN532 using I2C with IRQ and RESET
Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET, &Wire);

// Create a SoftwareSerial instance for the HC-05 Bluetooth
SoftwareSerial BT(10, 11); // RX, TX for HC-05

void setup(void) {
  Serial.begin(115200);
  BT.begin(9600); // HC-05 default baud rate
  
  Serial.println("Initializing PN532 (I2C mode)...");
  
  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.println("Didn't find PN53x board; check wiring!");
    while (1); // halt if the PN532 is not found
  }
  
  Serial.print("Found chip PN5");
  Serial.println((versiondata >> 24) & 0xFF, HEX);
  Serial.print("Firmware ver. ");
  Serial.print((versiondata >> 16) & 0xFF, DEC);
  Serial.print('.');
  Serial.println((versiondata >> 8) & 0xFF, DEC);
  
  // Configure PN532 to read RFID tags
  nfc.SAMConfig();
  Serial.println("PN532 is ready. Waiting for an NFC tag...");
}

void loop(void) {
  uint8_t uid[7];    // Buffer to store the UID
  uint8_t uidLength; // Length of the UID

  // Read an ISO14443A type tag (NFC tag or phone) using PN532
  if (nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength)) {
    Serial.print("Tag detected! UID: ");
    String uidStr = "";
    for (uint8_t i = 0; i < uidLength; i++) {
      if (uid[i] < 0x10) Serial.print("0");
      Serial.print(uid[i], HEX);
      uidStr += String(uid[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    
    // Acknowledge successful scan via Bluetooth
    BT.print("ACK: UID ");
    BT.println(uidStr);
    
    delay(2000); // Delay to avoid reading the same tag multiple times rapidly
  }
  
  // (Optional) Echo data between Serial Monitor and HC-05
  if (BT.available()) {
    char c = BT.read();
    Serial.write(c);
  }
  
  if (Serial.available()) {
    char c = Serial.read();
    BT.write(c);
  }
}
