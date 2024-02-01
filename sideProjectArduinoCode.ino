#define numOfValsRec 5;
#define digitsPerValsRec 3;

#include <Servo.h>

Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;
Servo thumbServo;

int positions[] = {90,90,90,90,90};
int lastindexpos = 90;



void setup() {
  // put your setup code here, to run once:
  indexServo.attach(9);
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available())
  {
    indexServo.write(90);

    String fingerpositions ="";
    fingerpositions = Serial.readStringUntil('\n');
    //Serial.println(fingerpositions);
    
    //convert string to array
    for (int i = 0; i<(fingerpositions.length()) ;i++){
      int index = fingerpositions.indexOf(","); // finds the next commA
      positions[i] = atol(fingerpositions.substring(0,index).c_str()); //extracts the number
      fingerpositions = fingerpositions.substring(index+1); //removes the number from the string
    }
    
    for (int i = 0; i<5; i++)
    {
      Serial.println(positions[i]);
    }

    if (fingerpositions[0] > lastindexpos) 
    {
    indexServo.write(positions[0]); 
    fingerpositions[0] = lastindexpos;
    }
    if (fingerpositions[0] < lastindexpos) 
    {
    indexServo.write(positions[180]); 
    fingerpositions[0] = lastindexpos;
    }
    if (fingerpositions[0] = lastindexpos)
    {
      indexServo.write(positions[90]); 
    }


    middleServo.write(positions[1]); 
    ringServo.write(positions[2]); 
    pinkyServo.write(positions[3]); 
    thumbServo.write(positions[4]); 
  }
}
