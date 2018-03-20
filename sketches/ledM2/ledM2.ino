int step;

void setup() {
   // Set all the LED pins as outputs
   pinMode(RGB_GREEN, OUTPUT);
   pinMode(RGB_RED, OUTPUT);
   pinMode(RGB_BLUE, OUTPUT);
   pinMode(DS2, OUTPUT);
   pinMode(DS3, OUTPUT);
   pinMode(DS4, OUTPUT);
   pinMode(DS5, OUTPUT);
   pinMode(DS6, OUTPUT);

   step = 0;
}

void loop() {
   digitalWrite(RGB_GREEN, (step == 0)?LOW:HIGH);
   digitalWrite(RGB_RED, (step == 1)?LOW:HIGH);
   digitalWrite(RGB_BLUE, (step == 2)?LOW:HIGH);
   digitalWrite(DS2, (step == 3)?LOW:HIGH);
   digitalWrite(DS3, (step == 4)?LOW:HIGH);
   digitalWrite(DS4, (step == 5)?LOW:HIGH);
   digitalWrite(DS5, (step == 6)?LOW:HIGH);
   digitalWrite(DS6, (step == 7)?LOW:HIGH);
   step = (step + 1) % 8;
   delay(200);  
   if (step == 0) SerialUSB.println("Hello world!");
}
