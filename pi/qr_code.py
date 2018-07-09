# USAGE
# python barcode_scanner_video.py

# import the necessary packages
import numpy as np
import argparse
import cv2
import imutils
import time

from imutils.video import VideoStream
from pyzbar import pyzbar
import serial

from path import get_path

DEV_NAME = '/dev/ttyACM0'
INPUT_FORMAT = "LD:{},RD:{},FD:{},SH:{},SV:{}"
COMMAND_FORMAT = "MF:{},MB:{},ML:{},MR:{},SH:{},SV:{};"
target_cords = [1, 5]


def read_serial_data(serial_device):
    """
        Method to receive data from bluetooth device.
    """
    data = ''
    bytes_to_read = serial_device.inWaiting()
    while bytes_to_read > 0:
        data += serial_device.read(bytes_to_read).decode()
        bytes_to_read = serial_device.inWaiting()
        time.sleep(0.1)
    return data


def decode_serial_data(data):
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


def turn_left():
    command = COMMAND_FORMAT.format(0, 0, 100, 0, 90, 90)
    return command


def turn_right():
    command = COMMAND_FORMAT.format(0, 0, 0, 100, 90, 90)
    return command


def move_back():
    command = COMMAND_FORMAT.format(0, 100, 0, 0, 90, 90)
    return command


def move_forward(value=100):
    command = COMMAND_FORMAT.format(value, 0, 0, 0, 90, 90)
    return command


def stop():
    command = COMMAND_FORMAT.format(0, 0, 0, 0, 90, 90)
    return command


def look_left(value=180):
    if value != 180:
        value = value + 90
    command = COMMAND_FORMAT.format(0, 0, 0, 0, value, 90)
    return command


def look_right(value=10):
    command = COMMAND_FORMAT.format(0, 0, 0, 0, value, 90)
    return command


def look_straight():
    command = COMMAND_FORMAT.format(0, 0, 0, 0, 90, 90)
    return command


def get_next_command(current_cords, target_cords):
    source = ",".join([str(x) for x in current_cords])
    destination = ",".join([str(x) for x in target_cords])
    path_list = get_path(source, destination)
    commands = []
    if not path_list:
        return stop()
    for path in path_list:
        if 'F' in path:
            print("path val", path)
            value = 100
            # value = int(path.replace('F', '0'))
            commands.append(move_forward(value))
            commands.append(look_left())
            commands.append(look_left())
            commands.append(look_left())

            commands.append(look_straight())

            commands.append(look_right())
            commands.append(look_right())
            commands.append(look_right())

        elif 'B' in path:
            commands.append(move_back())
        elif 'L' in path:
            commands.append(turn_left())
        elif 'R' in path:
            commands.append(turn_right())
    print(commands)
    return commands


def adjust_gamma(image, gamma=0.5):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


# Setup serial device
serial_device = serial.Serial(DEV_NAME, baudrate=9600)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=False).start()
time.sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()

# loop over the frames from the video stream
computed_command = None
loop_counter = 0
while True:
    current_barcode = None
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # reduce brightness
    frame = adjust_gamma(frame)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        # if barcodeData not in found:
        # csv.write("{},{}\n".format(datetime.datetime.now(),
        #                            barcodeData))
        # csv.flush()
        # current_barcode = barcodeData
        # found.add(barcodeData)
        current_barcode = barcodeData
        print('barcodedata: {}'.format(barcodeData))

    # show the output frame
    cv2.imshow("Scanner", frame)

    key = cv2.waitKey(1) & 0xFF

    if loop_counter > 2:
        loop_counter = 0
        # Read data from arduino
        if not computed_command:
            command = COMMAND_FORMAT.format(0, 0, 0, 0, 90, 90)
        elif isinstance(computed_command, list) and len(computed_command) > 0:
            command = computed_command.pop(0)
        else:
            command = computed_command
        print("Sending", command)
        serial_device.write(command.encode())
        # print("Reading from bot")
        data = read_serial_data(serial_device)
        sensors_data = {}
        if data:
            sensors_data = decode_serial_data(data)
            print(sensors_data)

        left_distance = sensors_data.get('left', 500)
        right_distance = sensors_data.get('right', 500)
        front_distance = sensors_data.get('front', 500)

        # computed_command = None
        if front_distance < 5:
            # if left_distance > 5:
            #     computed_command = turn_left()
            # elif right_distance > 5:
            #     computed_command = turn_right()
            # else:
            #     computed_command = move_back()
            computed_command = stop()
        else:
            pass
            # computed_command = move_forward()
    else:
        loop_counter += 1

    if current_barcode is not None:
        print(current_barcode)
        code_list = current_barcode.split(',')
        if len(code_list) == 2:
            cord_x = int(code_list[0])
            cord_y = int(code_list[1])
            computed_command = get_next_command([cord_x, cord_y], target_cords)
    else:
        pass

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
