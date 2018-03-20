#! /usr/bin/python2.7

import argparse
import serial
import serial.tools.list_ports
from subprocess import call


CURRENT_DIR = "/home/daniel/Desktop/autopen2/CAN"
ARDUINO_PATH = "./Arduino/build/linux/work/arduino"
ARDUINO_LIBS = "~/Arduino"
ARDUINO_HARDWARE_PATH = "macchina:sam:m2"
BAUDRATE = 115200

#sketches = {sketchName:pathToFile}
sketches = {'M2RET':'{}/M2RET/M2RET.ino'.format(ARDUINO_LIBS),
            'Serial':'{}/CAN_SerialSender/CAN_SerialSender.ino'.format(ARDUINO_LIBS),
            'DoS':'{}/CAN_DOS/CAN_DOS.ino'.format(ARDUINO_LIBS),
            'Test':'{}/ledM2/ledM2.ino'.format(ARDUINO_LIBS)}

parser = argparse.ArgumentParser(description='Flash the M2 and/or send CAN packets.',
    epilog="To send CAN packets, first make sure to upload the ATT[]#] binary (m2.py -u ATT[#]), then send messages using -m [message]. To use the reverse engineering tool, simply upload M2RET (m2.py -u M2RET) and open up SavvyCAN. Uploading only needs to be done once for switching modes, not per usage.")

parser.add_argument('-u', '--upload', dest='upload', choices=[s for s in sketches],
                    help='Choose which script to upload to the M2')

parser.add_argument('-p', '--port', dest='port', choices=[p[0] for p in list(serial.tools.list_ports.comports())],
                    default= list(serial.tools.list_ports.comports())[0][0],
                    help='Define the port to upload the script through')

parser.add_argument('-i', '--id', dest='id',
                    help='Arbitration ID: 3 hex chars, max = (0x)100')

parser.add_argument('-m','--msg','--message', dest='msg',
                    help='Message to send on CAN bus: 8 hex chars, max = (0x)FFFFFFFF')

parser.add_argument('-l','--listen', action='store_true', help='Listen to serial port indefinitely')

args = parser.parse_args()

#Set up serial port
ser = serial.Serial(args.port,BAUDRATE)

#Verify the ID and Message args
if args.id is not None:
    if args.msg is None:
        print("Error: ID missing accompanying Message")
    if not args.id in ["%03x" % i for i in range(0,257)] and not args.id in ["%03X" % i for i in range(0,257)]:
        print("ID must be between 0x000 and 0x100, with no leading '0x'")

if args.msg is not None:
    if args.id is None:
        print("Error: Message missing accompanying ID")
    try:
        int(args.msg,16)
    except ValueError:
        print("MSG must be between 0x00000000 and 0xFFFFFFFF, with no leading '0x'")
    else:
        if not int(args.msg,16) <= 0xFFFFFFFF:
            print("MSG must be between 0x00000000 and 0xFFFFFFFF, with no leading '0x'")

#Uploading scripts
if args.upload is not None:
    caller = ARDUINO_PATH + " --board " + ARDUINO_HARDWARE_PATH + " --upload " + sketches.get(args.upload) +" --port " + args.port
    call(caller, shell=True)

#Sending serial data
if args.id is not None and args.msg is not None:
    if args.upload is not None:
        args.port = list(serial.tools.list_ports.comports())[0][0]
        ser = serial.Serial(args.port,BAUDRATE)
    ser.write(args.id+args.msg)

#Listen to serial port
if args.listen:
    print("Listening to serial port indefinitely:\n")
    while True:
        print ser.readline()
