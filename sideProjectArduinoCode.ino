#include <Servo.h>           //imports servo library
#include <LiquidCrystal.h>   //imprts LCD library
#include <Chrono.h>          //imports chrono library

#define numOfValsRec 8
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;
Servo servoWrist;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;
bool counterStart = false;
String receivedString;
int prevVals[numOfValsRec] = {2,2,2,2,2,0,0,0};

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

int indexSpinTime = 500;
int middleSpinTime = 600;
int ringSpinTime = 600;
int pinkySpinTime = 500;
int thumbSpinTime = 350;

int indexOpenSpinTime = 357;
int middleOpenSpinTime = 450;
int ringOpenSpinTime = 485;
int pinkyOpenSpinTime = 335;
int thumbOpenSpinTime = 255;

int indexShouldSpinFor;
int middleShouldSpinFor;
int ringShouldSpinFor;
int pinkyShouldSpinFor;
int thumbShouldSpinFor;

Chrono startIndex,startMiddle,startRing,startPinky,startThumb;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servoWrist.attach(13);
  lcd.begin(4,32);
}

void receiveData() {
  while(Serial.available())
  {
    char c = Serial.read();

    if (c=='$') {
      counterStart = true;
    }

    if (counterStart = true) {
      if (counter < stringLength) {
        receivedString = String(receivedString+c);
        counter++;
      }
      if (counter>= stringLength){
        for(int i = 0; i<numOfValsRec; i++){
          int num = (i*digitsPerValRec)+1;
          valsRec[i] = receivedString.substring(num,num+digitsPerValRec).toInt();
        } 
        valsRec[5] = (valsRec[5] *100) + (valsRec[6]*10) + (valsRec[7]);
        
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  receiveData();

    if (valsRec[0] - prevVals[0] > 0) 
      {
        servoIndex.attach(8);
        servoIndex.write(180);
        startIndex.restart();
        indexShouldSpinFor = (indexOpenSpinTime*abs(valsRec[0] - prevVals[0]));
        prevVals[0] = valsRec[0];
      }

    if (valsRec[0] - prevVals[0] < 0) 
      {
        servoIndex.attach(8);
        servoIndex.write(0);
        startIndex.restart();
        indexShouldSpinFor = (indexSpinTime*abs(valsRec[0] - prevVals[0]));
        prevVals[0] = valsRec[0];
      }
    


    if (valsRec[1] - prevVals[1] > 0) 
      {
        servoMiddle.attach(7);
        servoMiddle.write(180);
        startMiddle.restart();
        middleShouldSpinFor = (middleOpenSpinTime*abs(valsRec[1] - prevVals[1]));
        prevVals[1] = valsRec[1];
      }

    if (valsRec[1] - prevVals[1] < 0) 
      {
        servoMiddle.attach(7);
        servoMiddle.write(0);
        startMiddle.restart();
        middleShouldSpinFor = (middleSpinTime*abs(valsRec[1] - prevVals[1]));
        prevVals[1] = valsRec[1];
      }

    if (valsRec[2] - prevVals[2] > 0) 
      {
        servoRing.attach(10);
        servoRing.write(180);
        startRing.restart();
        ringShouldSpinFor = (ringOpenSpinTime*abs(valsRec[2] - prevVals[2]));
        prevVals[2] = valsRec[2];
      }

    if (valsRec[2] - prevVals[2] < 0) 
      {
        servoRing.attach(10);
        servoRing.write(0);
        startRing.restart();
        ringShouldSpinFor = (ringSpinTime*abs(valsRec[2] - prevVals[2]));
        prevVals[2] = valsRec[2];
      }

    if (valsRec[3] - prevVals[3] > 0) 
      {
        servoPinky.attach(11);
        servoPinky.write(180);
        startPinky.restart();
        pinkyShouldSpinFor = (pinkyOpenSpinTime*abs(valsRec[3] - prevVals[3]));
        prevVals[3] = valsRec[3];
      }

    if (valsRec[3] - prevVals[3] < 0) 
      {
        servoPinky.attach(11);
        servoPinky.write(0);
        startPinky.restart();
        pinkyShouldSpinFor = (pinkySpinTime*abs(valsRec[3] - prevVals[3]));
        prevVals[3] = valsRec[3];
      }

    if (valsRec[4] - prevVals[4] > 0) 
      {
        servoThumb.attach(12);
        servoThumb.write(180);
        startThumb.restart();
        thumbShouldSpinFor = (thumbOpenSpinTime*abs(valsRec[4] - prevVals[4]));
        prevVals[4] = valsRec[4];
      }

    if (valsRec[4] - prevVals[4] < 0) 
      {
        servoThumb.attach(12);
        servoThumb.write(0);
        startThumb.restart();
        thumbShouldSpinFor = (thumbSpinTime*abs(valsRec[4] - prevVals[4]));
        prevVals[4] = valsRec[4];
      }


    servoWrist.write(valsRec[5]);

    while (servoIndex.attached() | servoMiddle.attached() | servoRing.attached() | servoPinky.attached() | servoThumb.attached() )
    {
      if (startIndex.hasPassed(indexShouldSpinFor))
      {
        servoIndex.write(90);
        servoIndex.detach();
      }
      
      if (startMiddle.hasPassed(middleShouldSpinFor))
      {
        servoMiddle.write(90);
        servoMiddle.detach();
      }

      if (startRing.hasPassed(ringShouldSpinFor))
      {
        servoRing.write(90);
        servoRing.detach();
      }

      if (startPinky.hasPassed(pinkyShouldSpinFor))
      {
        servoPinky.write(90);
        servoPinky.detach();
      }

      if (startThumb.hasPassed(thumbShouldSpinFor))
      {
        servoThumb.write(90);
        servoThumb.detach();
      }
    }




}