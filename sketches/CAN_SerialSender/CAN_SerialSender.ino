//Listens for serial ID and MSG and sends it over the CAN bus.
//The message must be sent as one continuous string of hex chars with ID in the first 3 places and MSG in the last 8.
//Ex. To send as ID 0x123 the message 0xDEADBEEF, input "123DEADBEEF"

#include "variant.h"
#include <due_can.h>

//Leave defined if you use native port, comment if using programming port
#define Serial SerialUSB

void setup()
{

  Serial.begin(115200);

  // Initialize CAN0 and CAN1, Set the proper baud rates here
  Can0.begin(CAN_BPS_500K);
  Can1.begin(CAN_BPS_500K);
  //Can0.beginAutoSpeed();
  //Can1.beginAutoSpeed();


  Can0.watchFor();

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void sendData(int id, int msg)
{
	CAN_FRAME outgoing;
	outgoing.id = id;
	outgoing.extended = false;
	outgoing.priority = 0; //0-15 lower is higher priority
      outgoing.data.high = msg;

	Can0.sendFrame(outgoing);
}

void loop(){
  CAN_FRAME incoming;
  static unsigned long lastTime = 0;

  if (Can0.available() > 0) {
	Can0.read(incoming);
	Can1.sendFrame(incoming);
   }
  if (Can1.available() > 0) {
	Can1.read(incoming);
	Can0.sendFrame(incoming);
  }

  if (Serial.available() > 0) {
    // read the incoming message:
    const char * payload = Serial.readString().c_str();
    char id[4];
    char msg[8];
    strncpy(id,payload,sizeof(id)-1);
    id[3] = '\0';  //because strncpy didn't null terminate id
    strncpy(msg,payload+3,sizeof(msg));

    int idNum = (int)strtol(id, NULL, 16);
    int msgNum = (int)strtol(msg, NULL, 16);
    sendData(idNum, msgNum);

    Serial.print("ID: ");
    Serial.println(idNum);
    Serial.print("MSG: ");
    Serial.println(msgNum);
  }
}
