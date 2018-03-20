/*
  MCP2515 CAN Interface Using SPI
  
  Author: David Harding
  
  Created: 11/08/2010
  Modified: 6/26/12 by RechargeCar Inc.
  
  For further information see:
  
  http://ww1.microchip.com/downloads/en/DeviceDoc/21801e.pdf
  http://en.wikipedia.org/wiki/CAN_bus

  The MCP2515 Library files also contain important information.
  
  This sketch is configured to work with the 'Macchina' Automotive Interface board 
  manufactured by RechargeCar Inc. CS_PIN and INT_PIN are specific to this board.
  
  This sketch shows the most basic of steps to send and receive CAN messages.
  
  NOTE!!!  If you use this sketch to test on a live system I suggest that you comment out the
  send messages lines unless you are certain that they will have no detrimental effect! 


  This example code is in the public domain.
  
*/

#include <SPI.h>
#include <MCP2515_sw_can.h>

// Pin definitions specific to how the MCP2515 is wired up.
#define CS_PIN    85
#define INT_PIN    84

// Create CAN object with pins as defined
SWcan CAN(CS_PIN, INT_PIN);

void CANHandler() {
	CAN.intHandler();
}

void setup() {
	Serial.begin(115200);
	
	Serial.println("Initializing ...");

	// Set up SPI Communication
	// dataMode can be SPI_MODE0 or SPI_MODE3 only for MCP2515
	SPI.setClockDivider(SPI_CLOCK_DIV2);
	SPI.setDataMode(SPI_MODE0);
	SPI.setBitOrder(MSBFIRST);
	SPI.begin();
	
	// Initialize MCP2515 CAN controller at the specified speed and clock frequency
	// (Note:  This is the oscillator attached to the MCP2515, not the Arduino oscillator)
	//speed in KHz, clock in MHz
	CAN.setupSW(250);
	
	attachInterrupt(6, CANHandler, FALLING);
	CAN.InitFilters(false);
	CAN.SetRXMask(MASK0, 0x7F0, 0); //match all but bottom four bits
	CAN.SetRXFilter(FILTER0, 0x100, 0); //allows 0x100 - 0x10F
	//So, this code will only accept frames with ID of 0x100 - 0x10F. All other frames
	//will be ignored.

	Serial.println("Ready ...");
}

byte i=0;

// CAN message frame (actually just the parts that are exposed by the MCP2515 RX/TX buffers)
Frame message;

void loop() {
	
	if (CAN.GetRXFrame(message)) {
		// Print message
		Serial.print("ID: ");
		Serial.println(message.id,HEX);
		Serial.print("Extended: ");
		if(message.extended) {
			Serial.println("Yes");
		} else {
			Serial.println("No");
		}
		Serial.print("Length: ");
		Serial.println(message.length,DEC);
		for(i=0;i<message.length;i++) {
			Serial.print(message.data.byte[i],HEX);
			Serial.print(" ");
		}
		Serial.println();
		Serial.println();

		// Send out a return message for each one received
		// Simply increment message id and data bytes to show proper transmission
		// Note: this will double the traffic on the network (provided it passes the filter above)
		message.id++;
		for(i=0;i<message.length;i++) {
			message.data.byte[i]++;
		}
		CAN.EnqueueTX(message);
	}
}
