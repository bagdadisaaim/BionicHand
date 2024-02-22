#include <Servo.h>
#include <LiquidCrystal.h>

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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servoThumb.attach(12);
  servoIndex.attach(8);
  servoMiddle.attach(9);
  servoRing.attach(10);
  servoPinky.attach(11);
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

    if ((valsRec[0] != prevVals[0]) | (valsRec[1] != prevVals[1]) | (valsRec[2] != prevVals[2]) | (valsRec[3] != prevVals[3]) | (valsRec[4] != prevVals[4]))
        {
          lcd.clear();
          for (int i = 0; i<6; i++)
          {
            lcd.print(valsRec[i]);
            lcd.print(",");
          }
        }


  if (valsRec[0] != prevVals[0])
    {
      if (valsRec[0] - prevVals[0] > 0) 
      {
        servoIndex.write(180);
        delay(abs(valsRec[0] - prevVals[0]) * 450);
        servoIndex.write(90);
        prevVals[0] = valsRec[0];
      }
      if (valsRec[0] - prevVals[0] < 0) 
      {
        servoIndex.write(0);
        delay(abs(valsRec[0] - prevVals[0])*450);
        servoIndex.write(90);
        prevVals[0] = valsRec[0];
      }
    }

    if (valsRec[1] != prevVals[1])
    {
      if (valsRec[1] - prevVals[1] > 0) 
      {
        servoMiddle.write(180);
        delay(abs(valsRec[1] - prevVals[1]) * 500);
        servoMiddle.write(90);
        prevVals[1] = valsRec[1];
      }
      if (valsRec[1] - prevVals[1] < 0) 
      {
        servoMiddle.write(0);
        delay(abs(valsRec[1] - prevVals[1])*500);
        servoMiddle.write(90);
        prevVals[1] = valsRec[1];
      }
    }

    if (valsRec[2] != prevVals[2])
    {
      if (valsRec[2] - prevVals[2] > 0) 
      {
        servoRing.write(180);
        delay(abs(valsRec[2] - prevVals[2]) * 500);
        servoRing.write(90);
        prevVals[2] = valsRec[2];
      }
      if (valsRec[2] - prevVals[2] < 0) 
      {
        servoRing.write(0);
        delay(abs(valsRec[2] - prevVals[2])*500);
        servoRing.write(90);
        prevVals[2] = valsRec[2];
      }
    }

    if (valsRec[3] != prevVals[3])
    {
      if (valsRec[3] - prevVals[3] > 0) 
      {
        servoPinky.write(180);
        delay(abs(valsRec[3] - prevVals[3]) * 500);
        servoPinky.write(90);
        prevVals[3] = valsRec[3];
      }
      if (valsRec[3] - prevVals[3] < 0) 
      {
        servoPinky.write(0);
        delay(abs(valsRec[3] - prevVals[3])*500);
        servoPinky.write(90);
        prevVals[3] = valsRec[3];
      }
    }

    if (valsRec[4] != prevVals[4])
    {
      if (valsRec[4] - prevVals[4] > 0) 
      {
        servoThumb.write(180);
        delay(abs(valsRec[4] - prevVals[4]) * 500);
        servoThumb.write(90);
        prevVals[4] = valsRec[4];
      }
      if (valsRec[4] - prevVals[4] < 0) 
      {
        servoThumb.write(0);
        delay(abs(valsRec[4] - prevVals[4])*500);
        servoThumb.write(90);
        prevVals[4] = valsRec[4];
      }
    }

    servoWrist.write(valsRec[5]);

    
}
