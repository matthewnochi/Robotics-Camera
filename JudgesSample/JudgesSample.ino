
/*
Setup:
  5V to +
  GND to -

  IN1 to pin8
  IN2 to pin 9
  IN3 to pin 10
  IN4 to pin 11
 */

#include <Stepper.h>

const int stepsPerRevolution = 2048; 

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  // set the speed at 5 rpm:
  myStepper.setSpeed(5);

  // initialize the serial port:
  Serial.begin(9600);
  while (!Serial) {}
  Serial.println("Type 'left' or 'right' in the Serial Monitor to call a task.");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read input until newline
    input.trim();

    if (input == "left") {
      left();
    } else if (input == "right") {
      right();
    } else {
      Serial.println("Invalid command. Type 'left' or 'right'.");
    }
  }
  
}

void left() {
  myStepper.step(-(stepsPerRevolution/4));
}

void right() {
  myStepper.step(stepsPerRevolution/4);
}

