import serial
import time

# Replace 'COM3' with your Arduino's serial port
port = 'COM8'
baudrate = 9600

# Open the serial connection to the Arduino
ser = serial.Serial(port, baudrate, timeout=1)                                                                                                                                                                                                                                                                                                                           
  
# Wait for the serial connection to initialize
time.sleep(2)

# Continuously send 'high' and 'low' commands to the Arduino every second
while True:
    ser.write(b'high\n\r')  # Send the 'high' command
    print("Sent: high")
    time.sleep(1)  # Wait for 1 second

    ser.write(b'low\n\r')  # Send the 'low' command
    print("Sent: low")
    time.sleep(1)  # Wait for 1 second             