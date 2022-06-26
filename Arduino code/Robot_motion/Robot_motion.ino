#include <Servo.h>

Servo myservo;  // create servo object to control a servo

#define MLa 5     //left motor 1st pin
#define MLb 6     //left motor 2nd pin
#define MRa 10    //right motor 1st pin
#define MRb 11    //right motor 2nd pin
void setup() 
{
  pinMode(MLa, OUTPUT);   
  pinMode(MLb, OUTPUT);   
  pinMode(MRa, OUTPUT);   
  pinMode(MRb, OUTPUT); 
  //pinMode(13, OUTPUT);
  Serial.begin(9600);
  myservo.attach(9);
  myservo.writeMicroseconds(1000);  
}



void loop() 
{  
    if (Serial.available() > 0) {
    char state = Serial.read();
    
    if (state == 'R' || state == 'r') {
    //Rotate robot in right direction
    digitalWrite(MLa, HIGH);    //Rotate left motor in fwd direction
    digitalWrite(MLb, LOW);     
    digitalWrite(MRa, LOW);     //Rotate right motor in back direction
    digitalWrite(MRb, HIGH);  
    //delay(2000);         //wait for 2 second//
    }
    
    if (state == 'L' || state == 'l') {
    //Rotate robot in left direction
    digitalWrite(MLa, LOW);      //Rotate left motor in fwd direction
    digitalWrite(MLb, HIGH);
    digitalWrite(MRa, HIGH);     //Rotate right motor in back direction
    digitalWrite(MRb, LOW);
    //delay(2000);         //wait for 2 second//
    }

    if (state == 'B' || state == 'b') {
    //Rotate both Motors in Backward Direction//
    digitalWrite(MLa, LOW);
    digitalWrite(MLb, HIGH);
    digitalWrite(MRa, LOW);
    digitalWrite(MRb, HIGH);
    //delay(2000);           //wait for 2 second//
    }

    if (state == 'F' || state == 'f'){
    //Rotate both Motors in Forward Direction//
    digitalWrite(MLa, HIGH);              
    digitalWrite(MLb, LOW);
    digitalWrite(MRa, HIGH);
    digitalWrite(MRb, LOW);
    //delay(2000);            //wait for 2 second//  
    }

    if (state == 'S' || state == 's'){
    //stop both the motors//
    digitalWrite(MLa, LOW);              
    digitalWrite(MLb, LOW);
    digitalWrite(MRa, LOW);
    digitalWrite(MRb, LOW);
    //delay(1000);    //wait for 1 second//
    }

    if (state == 'T' || state == 't') {
    //Rotate robot in soft left direction
    analogWrite(MLa, 0);      //Rotate left motor in fwd direction
    analogWrite(MLb, 200);
    analogWrite(MRa, 0);     //Rotate right motor in back direction
    analogWrite(MRb, 0);
    //delay(2000);         //wait for 2 second//
    }

    if (state == 'G' || state == 'g') {
    //Rotate robot in soft right direction
    analogWrite(MLa, 200);    //Rotate left motor in fwd direction
    analogWrite(MLb, 0);     
    analogWrite(MRa, 0);     //dont Rotate right motor
    analogWrite(MRb, 0);  
    //delay(2000);         //wait for 2 second//
    }
  
    if (state == 'E' || state == 'e') {
    myservo.writeMicroseconds(1000);
    }

    if (state == 'K' || state == 'k') {
    myservo.writeMicroseconds(1500);
    }
    
  }
  //delay(50); 
    
}
