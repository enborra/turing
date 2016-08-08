#include <Arduino.h>
#include "core/foreman/Foreman.h"
#include "core/sensor_monitor/SensorMonitor.h"
#include "core/eyes/Eyes.h"


/* Lux sensor bits */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

/* -- -- -- */


SensorMonitor _sensor_manager;
Eyes _eyes;
Foreman _time;




#define MOTOR_PWM_A A0
#define MOTOR_PWM_B A1

#define MOTOR_1 6
#define MOTOR_2 7
#define MOTOR_3 8  // working
#define MOTOR_4 9  // working





/*
--------------------------------------------------------------------------------
CORE PROCESSOR FUNCTIONS
--------------------------------------------------------------------------------
*/

void setup(void){
	Serial.begin(115200);
	Serial.println("[ENGINE] Starting...");
	Serial.println("");






	pinMode(13, OUTPUT);

  pinMode(MOTOR_1, OUTPUT);
  digitalWrite(MOTOR_1, LOW);

  pinMode(MOTOR_2, OUTPUT);
  digitalWrite(MOTOR_2, LOW);

  pinMode(MOTOR_3, OUTPUT);
  digitalWrite(MOTOR_3, LOW);

  pinMode(MOTOR_4, OUTPUT);
  digitalWrite(MOTOR_4, LOW);

  pinMode(MOTOR_PWM_B, OUTPUT);
  digitalWrite(MOTOR_PWM_B, LOW);

  pinMode(MOTOR_PWM_A, OUTPUT);
  digitalWrite(MOTOR_PWM_A, LOW);

//  Serial.begin(115200);
  Serial.println("[MOTOR] Booting...");



	/* Initialise the sensor */
  if(!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  /* Display some basic information on this sensor */
  displaySensorDetails();

  /* Setup the sensor gain and integration time */
  configureSensor();

  /* We're ready to go! */
  Serial.println("");


	_sensor_manager.init();
	_eyes.init();

	Foreman::init();
	Foreman::subscribe_frame(update_frame);
	Foreman::subscribe_half_second(update_half_second);
	Foreman::subscribe_second(update_second);
}

int drive_counter = 0;

void loop(void){

  if( drive_counter < 30*1000 ){
		if( drive_counter == 0 ){
			moveMotor(true);

			/* Get a new sensor event */
			sensors_event_t event;
			tsl.getEvent(&event);

			/* Display the results (light is measured in lux) */
			if (event.light){
				Serial.print(event.light); Serial.println(" lux");
			} else {
				/* If event.light = 0 lux the sensor is probably saturated
					 and no reliable data could be generated! */
				Serial.println("Sensor overload");
			}
		} else if( drive_counter == 10*1000 ){
			moveMotor(false);
		} else if( drive_counter > 20*1000 ){
			stopMotor();
		}


		drive_counter += 1;
  } else {
		drive_counter = 0;
	}

	// Serial.println(drive_counter);


//	digitalWrite(13, HIGH);
//  delay(100);
//  digitalWrite(13, LOW);
//
  // moveMotor(true, 1400);
//  digitalWrite(13, LOW);
//
////  delay(1000);
//
  // moveMotor(false, 1400);
//  digitalWrite(13, LOW);



	Foreman::update();
}


/*
--------------------------------------------------------------------------------
TIMER FUNCTIONS
--------------------------------------------------------------------------------
*/




void displaySensorDetails(void)
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

void configureSensor(void)
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



void moveMotor(boolean direction){
  digitalWrite(MOTOR_PWM_B, HIGH);
  digitalWrite(MOTOR_PWM_A, HIGH);

  if( direction ){
    digitalWrite(MOTOR_1, HIGH);
    digitalWrite(MOTOR_2, LOW);

    digitalWrite(MOTOR_3, LOW);
    digitalWrite(MOTOR_4, HIGH);
  } else {
    digitalWrite(MOTOR_1, LOW);
    digitalWrite(MOTOR_2, HIGH);

    digitalWrite(MOTOR_3, HIGH);
    digitalWrite(MOTOR_4, LOW);
  }

  // digitalWrite(MOTOR_1, LOW);
  // digitalWrite(MOTOR_2, LOW);
	//
  // digitalWrite(MOTOR_3, LOW);
  // digitalWrite(MOTOR_4, LOW);
	//
  // digitalWrite(MOTOR_PWM_B, LOW);
  // digitalWrite(MOTOR_PWM_A, LOW);
}

void stopMotor(){
	digitalWrite(MOTOR_1, LOW);
	digitalWrite(MOTOR_2, LOW);

	digitalWrite(MOTOR_3, LOW);
	digitalWrite(MOTOR_4, LOW);

	digitalWrite(MOTOR_PWM_B, LOW);
	digitalWrite(MOTOR_PWM_A, LOW);
}


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
