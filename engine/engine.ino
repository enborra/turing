#include <Arduino.h>
#include "core/foreman/Foreman.h"
#include "core/sensor_monitor/SensorMonitor.h"
#include "core/eyes/Eyes.h"


SensorMonitor _sensor_manager;
Eyes _eyes;
Foreman _time;


/*
--------------------------------------------------------------------------------
CORE PROCESSOR FUNCTIONS
--------------------------------------------------------------------------------
*/

void setup(void){
	Serial.begin(115200);
	Serial.println("[ENGINE] Starting...");
	Serial.println("");

	_sensor_manager.init();
	_eyes.init();

	Foreman::init();
	Foreman::subscribe_frame(update_frame);
	Foreman::subscribe_half_second(update_half_second);
	Foreman::subscribe_second(update_second);
}

void loop(void){
	Foreman::update();
}


/*
--------------------------------------------------------------------------------
TIMER FUNCTIONS
--------------------------------------------------------------------------------
*/


void update_second(){
    // Serial.println("[ENGINE] second elapsed.");
}

void update_half_second(){
	// Serial.println("[ENGINE] half second elapsed.");
}

void update_frame(){
	long centimeters = _sensor_manager.get_proximity_front();
	long brightness = 100 - centimeters*3;

	if( brightness < 0 ){
		brightness = 0;
	} else if( brightness >= 90 ){
		Serial.println( _sensor_manager.get_temperature() );
	}

	_eyes.update(brightness);
}
