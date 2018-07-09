import serial
import time
from path import get_path

DEV_NAME = '/dev/ttyACM0'
INPUT_FORMAT = "LD:{},RD:{},FD:{},SH:{},SV:{}"
COMMAND_FORMAT = "MF:{},MB:{},ML:{},MR:{},SH:{},SV:{};"
target_cords = [1, 5]


class Car(object):

    def __init__(self):
        # Setup serial device
        self.serial_device = serial.Serial(DEV_NAME, baudrate=9600)

    def read_serial_data(self):
        """
            Method to receive data from bluetooth device.
        """
        data = ''
        bytes_to_read = self.serial_device.inWaiting()
        while bytes_to_read > 0:
            data += self.serial_device.read(bytes_to_read).decode()
            bytes_to_read = self.serial_device.inWaiting()
            time.sleep(0.1)
        return data

    def decode_serial_data(self, data):
        sensors = {
            'left': 500,
            'right': 500,
            'front': 500,
            'servo_h': None,
            'servo_v': None
        }
        data = data.strip()
        # print(data)
        data_list = data.split(',')
        # print(data_list)
        for word in data_list:
            new_list = word.split(':')
            # print(new_list)
            if len(new_list) > 1:
                sensor = new_list[0]
                value = int(new_list[1].strip())
                if 'LD' in sensor:
                    sensors['left'] = value
                elif 'RD' in sensor:
                    sensors['right'] = value
                elif 'FD' in sensor:
                    sensors['front'] = value
                elif 'SH' in sensor:
                    sensors['servo_h'] = value
                elif 'SV' in sensor:
                    sensors['servo_v'] = value
        return sensors

    def turn_left(self):
        command = COMMAND_FORMAT.format(0, 0, 100, 0, 90, 90)
        return command

    def turn_right(self):
        command = COMMAND_FORMAT.format(0, 0, 0, 100, 90, 90)
        return command

    def move_back(self):
        command = COMMAND_FORMAT.format(0, 100, 0, 0, 90, 90)
        return command

    def move_forward(self, value=100):
        command = COMMAND_FORMAT.format(value, 0, 0, 0, 90, 90)
        return command

    def stop(self):
        command = COMMAND_FORMAT.format(0, 0, 0, 0, 90, 90)
        return command

    def look_left(self, value=180):
        if value != 180:
            value = value + 90
        command = COMMAND_FORMAT.format(0, 0, 0, 0, value, 90)
        return command

    def look_right(self, value=10):
        command = COMMAND_FORMAT.format(0, 0, 0, 0, value, 90)
        return command

    def look_straight(self):
        command = COMMAND_FORMAT.format(0, 0, 0, 0, 90, 90)
        return command

    def get_next_command(self, current_cords, target_cords):
        source = ",".join([str(x) for x in current_cords])
        destination = ",".join([str(x) for x in target_cords])
        path_list = get_path(source, destination)
        commands = []
        if not path_list:
            return False, [self.stop()]
        for path in path_list:
            if 'F' in path:
                print("path val", path)
                value = 100
                # value = int(path.replace('F', '0'))
                commands.append(self.move_forward(value))
                commands.append(self.look_left())
                commands.append(self.look_left())
                commands.append(self.look_left())

                commands.append(self.look_straight())

                commands.append(self.look_right())
                commands.append(self.look_right())
                commands.append(self.look_right())

            elif 'B' in path:
                commands.append(self.move_back())
            elif 'L' in path:
                commands.append(self.turn_left())
            elif 'R' in path:
                commands.append(self.turn_right())
        print(commands)
        return True, commands

    def control(self, barcodes):
        computed_commands = []
        for current_code in barcodes:
            print(current_code)
            code_list = current_code.split(',')
            if len(code_list) == 2:
                cord_x = int(code_list[0])
                cord_y = int(code_list[1])
                status, computed_commands = self.get_next_command([cord_x, cord_y], target_cords)
        for command in computed_commands:
            self.send_command(command)

    def get_commands(self, barcodes):
        computed_commands = []
        status = True
        for current_code in barcodes:
            print(current_code)
            code_list = current_code.split(',')
            if len(code_list) == 2:
                cord_x = int(code_list[0])
                cord_y = int(code_list[1])
                status, computed_commands = self.get_next_command([cord_x, cord_y], target_cords)
        return status, computed_commands

    def send_command(self, command):
        print("Sending", command)
        self.serial_device.write(command.encode())
        # print("Reading from bot")
        data = self.read_serial_data()
        sensors_data = {}
        if data:
            sensors_data = self.decode_serial_data(data)
            print("Read", sensors_data)
        return sensors_data
