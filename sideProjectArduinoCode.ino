#include <Servo.h>
#include <LiquidCrystal.h>

#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;


int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;
bool counterStart = false;
String receivedString;
int prevVals[numOfValsRec] = {0,0,0,0,0};

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servoThumb.attach(12);
  servoIndex.attach(8);
  servoMiddle.attach(9);
  servoRing.attach(10);
  servoPinky.attach(11);
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
        }

    for (int i = 0; i<5; i++)
    {
      lcd.print(valsRec[i]);
      lcd.print(",");
    }


  if (valsRec[0] != prevVals[0])
    {
      if (valsRec[0] - prevVals[0] > 0) 
      {
        servoIndex.write(180);
        delay(abs(valsRec[0] - prevVals[0]) * 1000);
        servoIndex.write(90);
        prevVals[0] = valsRec[0];
      }
      if (valsRec[0] - prevVals[0] < 0) 
      {
        servoIndex.write(0);
        delay(abs(valsRec[0] - prevVals[0])*1000);
        servoIndex.write(90);
        prevVals[0] = valsRec[0];
      }
    }
}
