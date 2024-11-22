import os
import subprocess
import sys
import serial
import time
import keyboard  # Import the keyboard library
import Spectral_BLDC as Spectral

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
        return response.decode('utf-8', errors='replace')  # Return the response

def monitor_calibration(port):
    with serial.Serial(port, 256000, timeout=1) as ser:
        print("Monitoring for calibration success...")
        start_time = time.time()
        while time.time() - start_time < 45:  # Monitor for 30 seconds
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting or 1).decode('utf-8', errors='replace')
                print(response)  # Print any responses received
                if "success!" in response:
                    print("Calibration successful!")
                    return True
        print("Calibration did not complete in the expected timeframe.")
        return False

if __name__ == "__main__":

    Communication1 = Spectral.CanCommunication(bustype='slcan', channel='COM30', bitrate=1000000)
    Motor1 = Spectral.SpectralCAN(node_id=0, communication=Communication1)


    # Replace 'COM3' with your Arduino's serial port
    port = 'COM29'
    baudrate = 9600                                                                                                                                        
    # Open the serial connection to the Arduino
    ser = serial.Serial(port, baudrate, timeout=1)

    # Replace 'firmware.bin' with the path to your actual firmware file       
    firmware_path = 'firmware.bin'

    # List of commands to send
    commands_to_send = ['#Default', '#Info', '#Cal']  # Added #Cal command
    commands_to_send2 = ['#Term 0', '#Calibrated 0', '#Save']  # Added #Cal command
    print("Press 's' to upload firmware and send serial commands.")
    
    while True:
        if keyboard.is_pressed('s'):  # Check if 's' key is pressed

            ser.write(b'high\n\r')  # Send the 'high' commands
            print("Sent: high")
            time.sleep(1)  # Wait for 1 second

            # Upload the firmware
            upload_firmware(firmware_path)
            time.sleep(0.2)

            # Connect to the serial port and send commands
            for command in commands_to_send:
                response = send_serial_command('COM31', command)
                print(f"Response for '{command}': {response}")
                time.sleep(0.1)

            # Monitor for calibration success after sending #Cal
            if monitor_calibration('COM31'):
                print("Calibration Process completed.")
                for command in commands_to_send2:
                    response = send_serial_command('COM31', command)
                    print(f"Response for '{command}': {response}")
                    time.sleep(0.1)


                Motor1.Send_Respond_Device_Info()

                message, UnpackedMessageID = Communication1.receive_can_messages(timeout=0.2) 

                if message is not None:
                    print(f"Message is: {message}")
                    print(f"Node ID is : {UnpackedMessageID.node_id}")
                    print(f"Message ID is: {UnpackedMessageID.command_id}")
                    print(f"Error bit is: {UnpackedMessageID.error_bit}")
                    print(f"Message length is: {message.dlc}")
                    print(f"Is is remote frame: {message.is_remote_frame}")
                    print(f"Timestamp is: {message.timestamp}")
                    print(f"CAN is working!")
                    Motor1.UnpackData(message,UnpackedMessageID)
                else:
                    print("No message after timeout period!")
                print("")

                print("All is good! Press 's' to run again or Ctrl+C to exit.")

            else:
                print("#################################################################################")
                print("#################################################################################")
                print("Process completed with calibration issues. Press 's' to run again or Ctrl+C to exit.")
                print("#################################################################################")  
                print("#################################################################################")
                print("#################################################################################")

            ser.write(b'low\n\r')  # Send the 'low' command
            print("Sent: low")
            time.sleep(1)  # Wait for 1 second
        