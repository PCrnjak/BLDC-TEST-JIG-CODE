#include <Arduino.h>

// Define the pin connected to the output (LED or other device)
const int outputPin = 8;
String inputString = "";  // Variable to store incoming serial data
bool stringComplete = false;  // Flag to indicate if the input string is complete

void setup() {
  // Set the output pin to output mode
  pinMode(outputPin, OUTPUT);

  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);

  // Make sure the pin starts low
  digitalWrite(outputPin, LOW);
}

void loop() {
  // Check if the input string is complete
  if (stringComplete) {
    // Check if the input is "high\n\r"
    if (inputString == "high\n\r") {
      digitalWrite(outputPin, HIGH);  // Set pin 8 high
      Serial.println("Pin 8 set to HIGH");
    }
    // Check if the input is "low\n\r"
    else if (inputString == "low\n\r") {
      digitalWrite(outputPin, LOW);  // Set pin 8 low
      Serial.println("Pin 8 set to LOW");
    }

    // Clear the input string
    inputString = "";
    stringComplete = false;  // Reset the flag
  }

  // Read serial data if available
  if (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    Serial.println(inChar);
    inputString += inChar;  // Append the incoming character to the string

    // Check if the string is complete (ends with \n\r)
    if (inputString.endsWith("\n\r")) {
      stringComplete = true;
    }
  }
}