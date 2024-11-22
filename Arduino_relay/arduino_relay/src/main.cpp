#include <Arduino.h>

// Define the pin connected to the output (LED or other device)
const int outputPin = A0;
String inputString = "";  // Variable to store incoming serial data
bool stringComplete = false;  // Flag to indicate if the input string is complete

void setup() {
  // Set the output pin to output mode
  pinMode(outputPin, OUTPUT);

  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);

  // Make sure the pin starts low
  digitalWrite(outputPin, LOW);
  Serial.println("Enter 'high' or 'low' to control pin 8");
}

void loop() {
  // Check if the input string is complete
  if (stringComplete) {
    // Remove any trailing newline or carriage return characters
    inputString.trim();

    // Check if the input is "high"
    if (inputString.equals("high")) {
      digitalWrite(outputPin, HIGH);  // Set pin 8 high
      Serial.println("Pin 8 set to HIGH");
    }
    // Check if the input is "low"
    else if (inputString.equals("low")) {
      digitalWrite(outputPin, LOW);  // Set pin 8 low
      Serial.println("Pin 8 set to LOW");
    } else {
      Serial.println("Unknown command. Please enter 'high' or 'low'.");
    }

    // Clear the input string
    inputString = "";
    stringComplete = false;  // Reset the flag
  }

  // Read serial data if available
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    // Check if the last received character is newline or carriage return
    if (inChar == '\n' || inChar == '\r') {
      stringComplete = true;
    }
  }
}