#! /usr/bin/python2.7

import argparse
import serial
import serial.tools.list_ports
from subprocess import call

ARDUINO_PATH = "./Arduino/build/linux/work/arduino"
M2_HARDWARE_PATH = "macchina:sam:m2"
BAUDRATE = 115200

#sketches = {sketchName:pathToFile}
sketches = {'M2RET':'sketches/M2RET/M2RET.ino',
            'Serial':'sketches/CAN_SerialSender/CAN_SerialSender.ino',
            'DoS':'sketches/CAN_DOS/CAN_DOS.ino',
            'Test':'sketches/ledM2/ledM2.ino'}

parser = argparse.ArgumentParser(description='Flash the M2 and/or send CAN packets.',
    epilog="To send CAN packets, first make sure to upload the ATT[]#] binary (m2.py -u ATT[#]), then send messages using -m [message]. To use the reverse engineering tool, simply upload M2RET (m2.py -u M2RET) and open up SavvyCAN. Uploading only needs to be done once for switching modes, not per usage.")

parser.add_argument('-u', '--upload', dest='upload', choices=[s for s in sketches],
                    help='Choose which script to upload to the M2')

parser.add_argument('-p', '--port', dest='port', choices=[p[0] for p in list(serial.tools.list_ports.comports())],
                    help='Define the port to upload the script through')

parser.add_argument('-i', '--id', dest='id',
                    help='Arbitration ID: 3 hex chars, max = (0x)100')

parser.add_argument('-m','--msg','--message', dest='msg',
                    help='Message to send on CAN bus: 8 hex chars, max = (0x)FFFFFFFF')

parser.add_argument('-l','--listen', action='store_true', help='Listen to serial port indefinitely')

args = parser.parse_args()

#Set up serial port   #TODO: shit got weird when no ports are available, had to remove default line
ser = serial.Serial(args.port,BAUDRATE)

#Verify the ID and Message args
if args.id is not None:
    if args.msg is None:
        print("Error: ID missing accompanying Message")
    if not args.id in ["%03x" % i for i in range(0,4096)] and not args.id in ["%03X" % i for i in range(0,4096)]:
        print("ID must be between 0x000 and 0xFFF, with no leading '0x'")

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

def sendSerial(id,msg,port=0,time=5):
    try:
        ser = serial.Serial(port,BAUDRATE)
    except serial.SerialException:
        print("Couldn't connect to port: {}".format(port))
    else:
        #Sending serial data
        ser.write(id+msg)
        listenSerial(port,time)
        #ser.close()?

def verifyId(inputId):
    if not inputId in ["%03x" % i for i in range(0,4096)] and not args.id in ["%03X" % i for i in range(0,4096)]:
        print("ID must be between 0x000 and 0xFFF, with no leading '0x'")
        return False
    return True

def verifyMsg(inputMsg):
    try:
        int(inputMsg,16)
    except ValueError:
        print("Message must be a hexadecimal number")
        return False
    else:
        if not int(inputMsg,16) <= 0xFFFFFFFFFFFFFFFF:
            print("Message must be between 0x00000000 and 0xFFFFFFFFFFFFFFFF, with no leading '0x'")
            return False
    return True

def sendSignalM2RET(id,msg,port=0,can=0,time=5):
    if  not (verifyId(id) and verifyMsg(msg)):
        print "Message not sent."
        return

    msgSplit = ",".join([msg[i:i+2] for i in range(0, len(msg),2)])
    msgLen = len(msg)/2
    formatted = "CAN{}SEND=0x{},{},{}".format(can,id,msgLen,msgSplit)  #"CAN0SEND=ID,LEN,<BYTES SEPARATED BY COMMAS> - Ex: CAN0SEND=0x200,4,1,2,3,4"
    print "Sending: " + formatted
    try:
        ser = serial.Serial(port,BAUDRATE)
    except serial.SerialException:
        print("Couldn't connect to port: {}".format(port))
        return
    else:
        #Sending serial data
        ser.write(formatted)
        listenSerial(port,time)
        #ser.close()?



def listenSerial(port,time=0):
    #Listen to serial port
    ser = serial.Serial(port,BAUDRATE)
    if time == 0:
        print("Listening to serial port indefinitely:\n")
        while True:
            print ser.readline()
    else:
        print("Listening for {} seconds".format(time))

def uploadScript(script, port=0):
    #Uploading scripts
    caller = ARDUINO_PATH + " --board " + M2_HARDWARE_PATH + " --upload " + sketches.get(script)
    if port != 0:
        caller += " --port " + port
    call(caller, shell=True)
#Caller to Upload Script
if args.upload is not None:
    if args.port is not None:
        uploadScript(args.upload, args.port)
    else:
        uploadScript(args.upload)

if args.id is not None and args.msg is not None:
    if args.upload is not None:
        args.port = list(serial.tools.list_ports.comports())[0][0]
    sendSerial(args.id,args.msg,args.port)

if args.listen:
    listenSerial(args.port)
