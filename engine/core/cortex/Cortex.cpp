/*
----------------------------------------------------------------------------------------------------
DEPENDENCY INCLUDES
----------------------------------------------------------------------------------------------------
*/

/* System includes */

#include <Arduino.h>
#include <Wire.h>

/* Third party includes */

#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

/* Class includes */

#include "Cortex.h"
#include "../optics/Eye.h"
#include "../foreman/Foreman.h"
#include "../motor/MotorController.h"
#include "../sensor_monitor/SensorMonitor.h"


/*
----------------------------------------------------------------------------------------------------
PROPERTY DEFINITIONS
----------------------------------------------------------------------------------------------------
*/


Foreman Cortex::_time;


/*
----------------------------------------------------------------------------------------------------
PUBLIC FUNCTIONS
----------------------------------------------------------------------------------------------------
*/


Cortex::Cortex(){
	/* Do nothing */
}

void Cortex::init(){
    Serial.begin(115200);
    Serial.println("[CORTEX] Starting...");
    Serial.println("");

    pinMode(13, OUTPUT);

    Serial.println("[CORTEX] Booting...");

    Eye::init();

	Foreman::init();
	Foreman::subscribe_frame(update_frame);
	Foreman::subscribe_half_second(update_half_second);
	Foreman::subscribe_second(update_second);

    SensorMonitor::init();
}

void Cortex::update(){
    float val = (exp(sin(millis()/4000.0*PI)) - 0.36787944)*108.0;

    Eye::update(val);
	Foreman::update();
}


/*
----------------------------------------------------------------------------------------------------
TIMER FUNCTIONS
----------------------------------------------------------------------------------------------------
*/


void Cortex::update_second(){
    // Serial.println("[ENGINE] second elapsed.");
}

void Cortex::update_half_second(){
	// Serial.println("[ENGINE] half second elapsed.");
}

void Cortex::update_frame(){
	long centimeters = SensorMonitor::get_proximity_front();
	// long brightness = 100 - centimeters*8;

	if( ((centimeters>5) && (centimeters<10)) || (centimeters > 14) ){
		MotorController::stop();
	} else if( centimeters > 10){
		MotorController::move(true);
	} else if( centimeters < 5 ){
		MotorController::move(false);
	}
}
