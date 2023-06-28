#include <AccelStepper.h>
#include <MultiStepper.h>

float xpos = 0; //position of car relative to (0,0) corner in cm
float ypos = 0; 
int maxSpeed = 10000; //max speed of wheels
// int trigger1 = 2;
// int echo1 = 3;
// int trigger2 = 4;
// int echo2 = 5;
float wheelCircum = 128.0/5.0; //circumference of the wheels in cm
float targetx = 160;
float targety = 175;
float duration1, distance1, duration2, distance2;
int count = 0;
AccelStepper stepper1(1,19,9);
AccelStepper stepper2(1,20,10);
AccelStepper stepper3(1,21,11);
AccelStepper stepper4(1,22,12);
MultiStepper steppersControl;
long gotoposition[4];

void setup() {
  stepper1.setMaxSpeed(maxSpeed);
  stepper2.setMaxSpeed(maxSpeed);
  stepper3.setMaxSpeed(maxSpeed);
  stepper4.setMaxSpeed(maxSpeed);
  steppersControl.addStepper(stepper1);
  steppersControl.addStepper(stepper2);
  steppersControl.addStepper(stepper3);
  steppersControl.addStepper(stepper4);

  delay(1000);
}

void loop() {

  //if (Serial.available() == 0) {
  int xsteps = (int) ((targetx-xpos)/wheelCircum * 200 * 8) * 50/46;
  int ysteps = (int) ((targety-ypos)/wheelCircum * 200 * 8);
  int steps12 = (int) ((xsteps + ysteps));
  int steps03 = (int) ((ysteps - xsteps));
  gotoposition[0] = steps03;
  gotoposition[1] = steps12;
  gotoposition[2] = steps12;
  gotoposition[3] = steps03;
  steppersControl.moveTo(gotoposition);
  steppersControl.runSpeedToPosition();
  count++;
  if (count > 0 && count < 5) {

    if (count == 1) {
      delay(500);
      targetx = -75;
      targety = -50;

    }
    else if (count == 2) {
      delay(500);
      targetx = -50;
      targety = 0;
    }
    else if (count == 3) {
      delay(500);
      targetx = 0;
      targety = -75;
    }
    else if (count == 4) {
      delay(500);
      targetx = 30;
      targety = 75;
    }
    stepper1.setCurrentPosition(0);
    stepper2.setCurrentPosition(0);
    stepper3.setCurrentPosition(0);
    stepper4.setCurrentPosition(0);
  }
  //}



  //char incomingByte;
  // std::cout << "poggers" << std::endl;
  // if (Serial.available() > 0) {
  //   incomingByte = Serial.read();
  //   Serial.print("USB received: ");
  //   Serial.println(incomingByte);
  // }


  // char serialIn = Serial.read();
  // //cout << (int)serialIn << endl;
  // //int serialIn = Serial.read();
  // if (serialIn != 0) {
  //   //targety = serialIn / (wheelCircum * 1600);
  // }
  
  // // if (Serial.available() > 0) {
  // //   ypos = 0;
  // //   xpos = 0;
  // //   targety = Serial.read();
  // //   targety = targety / wheelCircum * 1600.0;
  // //   Serial.print(targety);
  // //   // Serial.end();
  // //   // Serial.begin(9600);
  // // }
}

void getpos() {
  /*digitalWrite(trigger1, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigger1, LOW);
  duration1 = pulseIn(echo1, HIGH);
  delayMicroseconds(30);
  digitalWrite(trigger2, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigger2, LOW);
  duration2 = pulseIn(echo2, HIGH);
  distance1 = 0.017 *duration1;
  distance2 = 0.017 * duration2;
  xpos = 0;
  ypos = 0;*/
}
