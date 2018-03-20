# M2


## Installation for Ubuntu 16.04
1. Clone the repository
2. Run `python setupM2.py`

## Usage
### Uploading Scripts
* Use the '-u' flag to select the script from available choices
* Optionally select the port using the '-p' flag (otherwise the port is auto-assigned)
* The M2RET script is designed to work with [SavvyCAN](https://github.com/collin80/SavvyCAN)
* The Test script simply tests all of the LEDs on the M2
* CAN_SerialSender is designed to send messages via serial to the CAN bus. The M2 simply takes an 11-character string, the first three being the arbitration ID and the next 8 being the message.


### Sending CAN Packets
* To send using CAN_SerialSender, set the Arbitration ID (ex. 0x0A8) and Message (ex. 0xDEADBEEF) like so: `./m2.py -i 0A8 -m DEADBEEF`
...* The CAN_SerialSender sketch can either be uploaded before or concurrently (``./m2.py -u Serial -i 0A8 -m DEADBEEF`)
