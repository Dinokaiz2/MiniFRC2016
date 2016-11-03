/*
        Default Robot Code for MiniFRC 2016

        Accepts input from the default MiniFRC Driver Station over Bluetooth
        to drive a robot with two motors: one for the left and one for the right.
        Requires the Adafruit Motor Shield v1 along with its corresponding library
        which can be found here: https://learn.adafruit.com/adafruit-motor-shield/library-install

        Default wiring for this program:
        * Bluetooth to analog 0 and 1 (corresponding to 14 and 15 in the code)
        * Left motor to motor port 1
        * Right motor to motor port 3

	Created 11/02/16
	By the TerrorBytes FRC 4561
*/

#include <SoftwareSerial.h>
#include <AFMotor.h>

const int leftMotorPort = 1; // Port number for the left motor on the Adafruit motor shield
const int rightMotorPort = 3; // Port number for the right motor on the Adafruit motor shield
const int bluetoothTxPin = 14; // Analog input for Bluetooth Tx pin
const int bluetoothRxPin = 15; // Analon input for Bluetooth Rx pin

SoftwareSerial bluetooth(bluetoothTxPin, bluetoothRxPin); // Construct the bluetooth module
AF_DCMotor leftMotor(leftMotorPort); // Construct the left motor
AF_DCMotor rightMotor(rightMotorPort); // Construct the right motor

int turn = 0; // The direction the robot is turning. 1 = counterclockwise, -1 = clockwise
int velocity = 0; // The direction the robot is moving. 1 = forward, -1 = backwards

void setup() {
  bluetooth.begin(9600); // Start accepting data over bluetooth
  driveRight(0); // Make sure the left motor is stopped
  driveLeft(0); // Make sure the right motor is stopped
}

void loop() {
  while (bluetooth.available() > 0) { // Check if any data has been sent
    turn = bluetooth.parseInt(); // Get the first integer from the data
    velocity = bluetooth.parseInt(); // Get the second integer from the data
	
    // If you've edited the Driver Station to send extra data, you should
    // to do more calls to bluetooth.parseInt() here to get the data.
    // For example, if you have a number that you want to set the speed of
    // a robot's arm to that you're sending from the Driver Station, you can
    // get it here by doing:
    // arm_speed = bluetooth.parseInt();
    // You should declare the arm_speed variable where the turn and velocity
    // variables are declared above the setup method.
    	
    if (bluetooth.read() == 'a') { // Failsafe to ensure data isn't desynced
      if (velocity == 0 && turn == 0) { // Break
        driveRight(0);
        driveLeft(0);
      }
      else if (velocity == 1 && turn == 0) { // Forward
        driveRight(255);
        driveLeft(255);
      }
      else if (velocity == -1 && turn == 0) { // Backward
        driveRight(-255);
        driveLeft(-255);
      }
      else if (velocity == 0 && turn == 1) { // Rotate left on the spot
        driveRight(255);
        driveLeft(-255);
      }
      else if (velocity == 0 && turn == -1) { // Rotate right on the sport
        driveRight(-255);
        driveLeft(255);
      }
      else if (velocity == -1 && turn == -1) { // Arc back right
        driveRight(-127);
        driveLeft(-255);
      }
      else if (velocity == -1 && turn == 1) { // Arc back left
        driveRight(-255);
        driveLeft(-127);
      }
      else if (velocity == 1 && turn == -1) { // Arc forward right
        driveRight(127);
        driveLeft(255);
      }
      else if (velocity == 1 && turn == 1) { // Arc forward left
        driveRight(255);
        driveLeft(127);
      }
    }
  }
  // If servos and motors are updated too quickly, they sometimes don't work right.
  delay(50);
}

/** 
  Sets the right motor to a power.
  
  @param motorSpeed what to set the motor power to.
*/
void driveRight(int motorPower) {
  rightMotor.run((motorPower >= 0) ? FORWARD : BACKWARD);
  rightMotor.setSpeed(abs(motorPower)); 
}

/** 
  Sets the left motor to a power.
  
  @param motorSpeed what to set the motor power to.
*/
void driveLeft(int motorPower) {
  leftMotor.run((motorPower >= 0) ? FORWARD : BACKWARD);
  leftMotor.setSpeed(abs(motorPower));
}



