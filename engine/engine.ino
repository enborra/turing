/*
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

TURING ENGINE

The Turing engine drives all primary functions of the robot that are hardware-
bound.

	Motors: all primative functions of the wheel motors are controlled from
	Turing Engine - driving forward, backward, drive-turning, sharp-pivoting.

	Sensors: gyroscope functions (tilt/pan/accelerometer) and luminosoty / lux
	detection is done from Turing Engine.

All functional control is driven from Cortex, the base application logic
controller of the application.

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
*/


#include "core/cortex/Cortex.h"


/*
--------------------------------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------------------------------
*/


void setup(void){
	Cortex::init();
}

void loop(void){
	Cortex::update();
}
