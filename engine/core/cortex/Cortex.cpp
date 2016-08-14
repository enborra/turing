#include <Arduino.h>

#include "Cortex.h"
#include "../eyes/Eye.h"
#include "../motor/MotorController.h"
#include "../foreman/Foreman.h"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include "../sensor_monitor/SensorMonitor.h"



/*
--------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------
*/

SensorMonitor Cortex::_sensor_manager;
Adafruit_TSL2561_Unified Cortex::tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);
Foreman Cortex::_time;


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


    /* Initialise the sensor */
	if(!tsl.begin())
	{
		/* There was a problem detecting the ADXL345 ... check your connections */
		Serial.println("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
		while(1);
	}

	/* Display some basic information on this sensor */
	displaySensorDetails();

	// /* Setup the sensor gain and integration time */
	configureSensor();

	/* We're ready to go! */
	Serial.println("");


	_sensor_manager.init();
}

void Cortex::update(){
    float val = (exp(sin(millis()/4000.0*PI)) - 0.36787944)*108.0;

    Eye::update(val);


	Foreman::update();
}




void Cortex::displaySensorDetails(void)
{
  sensor_t sensor;
  tsl.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" lux");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" lux");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" lux");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void Cortex::configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  // tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  tsl.enableAutoRange(true);            /* Auto-gain ... switches automatically between 1x and 16x */

  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */

  /* Update these values depending on what you've set above! */
  Serial.println("------------------------------------");
  Serial.print  ("Gain:         "); Serial.println("Auto");
  Serial.print  ("Timing:       "); Serial.println("13 ms");
  Serial.println("------------------------------------");
}


/*
--------------------------------------------------------------------------------
TIMER FUNCTIONS
--------------------------------------------------------------------------------
*/


void Cortex::update_second(){
    // Serial.println("[ENGINE] second elapsed.");
}

void Cortex::update_half_second(){
	// Serial.println("[ENGINE] half second elapsed.");
}

void Cortex::update_frame(){
	long centimeters = _sensor_manager.get_proximity_front();
	// long brightness = 100 - centimeters*8;

	if( ((centimeters>5) && (centimeters<10)) || (centimeters > 14) ){
		MotorController::stop();
	} else if( centimeters > 10){
		MotorController::move(true);
	} else if( centimeters < 5 ){
		MotorController::move(false);
	}
}
