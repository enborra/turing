#include <Arduino.h>

#include "../../config/Pins.h"
#include "MotorController.h"



/*
--------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------
*/

const uint8_t MotorController::MOTOR_DIRECTION_NONE = 0;
const uint8_t MotorController::MOTOR_DIRECTION_FORWARD = 1;
const uint8_t MotorController::MOTOR_DIRECTION_BACKWARD = 2;


MotorController::MotorController(){
	/* Do nothing */
}

void MotorController::init(){
  pinMode(PIN_CONFIG_MOTOR_1, OUTPUT);
  pinMode(PIN_CONFIG_MOTOR_2, OUTPUT);
  pinMode(PIN_CONFIG_MOTOR_3, OUTPUT);
  pinMode(PIN_CONFIG_MOTOR_4, OUTPUT);
  pinMode(PIN_CONFIG_MOTOR_PWM_B, OUTPUT);
  pinMode(PIN_CONFIG_MOTOR_PWM_A, OUTPUT);

  stop();
}

void MotorController::update(){
	/* Do nothing */
}

void MotorController::move(boolean direction){
  _driveLeftWheel(direction);
  _driveRightWheel(direction);
}

void MotorController::stop(){
	digitalWrite(PIN_CONFIG_MOTOR_1, LOW);
	digitalWrite(PIN_CONFIG_MOTOR_2, LOW);

	digitalWrite(PIN_CONFIG_MOTOR_3, LOW);
	digitalWrite(PIN_CONFIG_MOTOR_4, LOW);

	digitalWrite(PIN_CONFIG_MOTOR_PWM_B, LOW);
	digitalWrite(PIN_CONFIG_MOTOR_PWM_A, LOW);
}


void MotorController::turnLeft(){
  _driveLeftWheel(MOTOR_DIRECTION_NONE);
  _driveRightWheel(MOTOR_DIRECTION_FORWARD);
}

void MotorController::turnRight(){
  _driveLeftWheel(MOTOR_DIRECTION_FORWARD);
  _driveRightWheel(MOTOR_DIRECTION_NONE);
}

void MotorController::pivotLeft(){
  _driveLeftWheel(MOTOR_DIRECTION_BACKWARD);
  _driveRightWheel(MOTOR_DIRECTION_FORWARD);
}

void MotorController::pivotRight(){
  _driveLeftWheel(MOTOR_DIRECTION_FORWARD);
  _driveRightWheel(MOTOR_DIRECTION_BACKWARD);
}


/*
--------------------------------------------------------
PRIVATE FUNCTIONS
--------------------------------------------------------
*/


void MotorController::_driveLeftWheel(boolean direction){
  digitalWrite(PIN_CONFIG_MOTOR_PWM_A, HIGH);

  if( direction ){
    digitalWrite(PIN_CONFIG_MOTOR_1, HIGH);
    digitalWrite(PIN_CONFIG_MOTOR_2, LOW);

  } else {
    digitalWrite(PIN_CONFIG_MOTOR_1, LOW);
    digitalWrite(PIN_CONFIG_MOTOR_2, HIGH);

  }
}

void MotorController::_driveRightWheel(boolean direction){
  digitalWrite(PIN_CONFIG_MOTOR_PWM_B, HIGH);

  if( direction ){
    digitalWrite(PIN_CONFIG_MOTOR_3, LOW);
    digitalWrite(PIN_CONFIG_MOTOR_4, HIGH);

  } else {
    digitalWrite(PIN_CONFIG_MOTOR_3, HIGH);
    digitalWrite(PIN_CONFIG_MOTOR_4, LOW);
  }
}
