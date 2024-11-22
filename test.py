import os
import subprocess
import sys
import serial
import time
import keyboard  # Import the keyboard library

def upload_firmware(firmware_file):
    # Check if the firmware file exists
    if not os.path.exists(firmware_file):
        print(f"Error: Firmware file {firmware_file} not found.")
        sys.exit(1)

    # Provide the full path to STM32_Programmer_CLI.exe
    stm32_programmer_path = r'C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe'  # Adjust this path if necessary

    # STM32CubeProgrammer CLI command to upload firmware
    command = [
        stm32_programmer_path,
        '-c', 'port=SWD',  # Using SWD (Serial Wire Debug) interface
        '-w', firmware_file, '0x08000000',  # Write firmware to 0x08000000
        '-rst'  # Reset the MCU after programming
    ]

    try:
        # Run the command using subprocess
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print output using 'replace' to handle decoding errors
        print(result.stdout.decode(errors='replace'))  # or use errors='ignore' to skip errors
        print("Firmware upload successful!")

    except subprocess.CalledProcessError as e:
        print("Error occurred while uploading firmware:")
        print(e.stderr.decode(errors='replace'))  # Handle decoding errors in error output
        sys.exit(1)

def send_serial_command(port, command):
    # Open the serial port
    with serial.Serial(port, 256000, timeout=1) as ser:
        time.sleep(0.5)  # Wait for the serial connection to initialize
        command_with_newline = command + '\n\r'  # Add newline and carriage return
        ser.write(command_with_newline.encode('utf-8'))  # Send the command
        time.sleep(0.5)  # Give the device time to respond
        response = ser.read(ser.in_waiting or 1)  # Read available response
        print(f"Response for '{command}': {response.decode('utf-8', errors='replace')}")  # Print the response

if __name__ == "__main__":
    # Replace 'firmware.bin' with the path to your actual firmware file
    firmware_path = 'firmware.bin'

    # List of commands to send
    commands_to_send = ['#Default', '#Info']

    print("Press 's' to upload firmware and send serial commands.")
    
    while True:
        if keyboard.is_pressed('s'):  # Check if 's' key is pressed
            # Upload the firmware
            upload_firmware(firmware_path)
            time.sleep(0.5)

            # Connect to the serial port and send commands
            for command in commands_to_send:
                send_serial_command('COM3', command)
                time.sleep(0.1)

            send_serial_command('COM3', '#Cal')

            print("Process completed. Press 's' to run again or Ctrl+C to exit.")
