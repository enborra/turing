#include <Arduino.h>
#include "../../config/I2C.h"
#include "SensorMonitor.h"


/*
----------------------------------------------------------------------------------------------------
PUBLIC FUNCTIONS
----------------------------------------------------------------------------------------------------
*/


Adafruit_LSM303_Accel_Unified	SensorMonitor::_accel(CONFIG_I2C_LSM303_ACCEL);
Adafruit_LSM303_Mag_Unified		SensorMonitor::_mag(CONFIG_I2C_LSM303_COMPASS);
Adafruit_BMP085_Unified			SensorMonitor::_bmp(CONFIG_I2C_BMP085_BAROMETRIC);
Adafruit_TSL2561_Unified		SensorMonitor::_tsl(TSL2561_ADDR_FLOAT, CONFIG_I2C_TSL2561_LUX);
Adafruit_10DOF					SensorMonitor::_dof;
float							SensorMonitor::_sea_level_pressure;


SensorMonitor::SensorMonitor(){
	/* Do nothing */
}

void SensorMonitor::init(){
	_sea_level_pressure = SENSORS_PRESSURE_SEALEVELHPA;

	if( !_accel.begin() ){
		Serial.println(F("[SENSOR] Ooops, no LSM303 detected ... Check your wiring!"));
	}

	if( !_mag.begin() ){
		Serial.println("[SENSOR] Ooops, no LSM303 detected ... Check your wiring!");
	}

	if( !_bmp.begin() ){
		Serial.println("[SENSOR] Ooops, no BMP180 detected ... Check your wiring!");
	}

	_tsl.enableAutoRange(true);
	_tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);

	if( !_tsl.begin() ){
	    Serial.print("[SENSOR] Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
	}
}

void SensorMonitor::update(){
	Serial.println("[SENSOR] Updating..");

	_update_acceleration();
	_update_compass();
	_update_altitude();
	_update_lux();
	_update_distance();

	Serial.println();
}

void SensorMonitor::_update_acceleration(){
	sensors_event_t accel_event;
	sensors_vec_t   orientation;

	_accel.getEvent(&accel_event);

	if( _dof.accelGetOrientation(&accel_event, &orientation) ){
		Serial.print(F("[SENSOR] Roll: "));
		Serial.print(orientation.roll);
		Serial.println(F("; "));
		Serial.print(F("[SENSOR] Pitch: "));
		Serial.print(orientation.pitch);
		Serial.println(F("; "));
	}
}

void SensorMonitor::_update_compass(){
	sensors_event_t mag_event;
	sensors_vec_t orientation;

	_mag.getEvent(&mag_event);

	if( _dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation) ){
		Serial.print(F("[SENSOR] Heading: "));
		Serial.print(orientation.heading);
		Serial.println(F("; "));
	}
}

void SensorMonitor::_update_altitude(){
	get_temperature();
}

void SensorMonitor::_update_lux(){
	sensors_event_t event;
	_tsl.getEvent(&event);

	if( event.light ){
		Serial.print("[SENSOR] Lux: ");
		Serial.println(event.light);
	} else {
		Serial.println("[SENSOR] Sensor overload");
	}

	// sensor_t sensor;
	//
	// tsl.getSensor(&sensor);
	// Serial.println("------------------------------------");
	// Serial.print  ("Sensor:       "); Serial.println(sensor.name);
	// Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
	// Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
	// Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" lux");
	// Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" lux");
	// Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" lux");
	// Serial.println("------------------------------------");
	// Serial.println("");
}

void SensorMonitor::_update_distance(){
	long duration;
	long feet;
	long cm;
	long inches;


	duration = get_proximity_front();

	Serial.print("[SENSOR] Microseconds away: ");
	Serial.println(duration);

	cm = _microsecondsToCentimeters(duration);
	inches = _microsecondsToInches(duration);
	feet = _microsecondsToFeet(duration);

	Serial.print("[SENSOR] Centimeters: ");
	Serial.println(cm);

	Serial.print("[SENSOR] Inches:  ");
	Serial.println(inches);

	Serial.print("[SENSOR] Feet:  ");
	Serial.println(feet);
}

long SensorMonitor::get_proximity_front(){
	int pin = 5;
	long duration;
	long inches;
	long feet;
	long cm;


	pinMode(pin, OUTPUT);
	digitalWrite(pin, LOW);
	delayMicroseconds(2);
	digitalWrite(pin, HIGH);
	delayMicroseconds(5);
	digitalWrite(pin, LOW);

	pinMode(pin, INPUT);
	duration = pulseIn(pin, HIGH);

	return _microsecondsToCentimeters(duration);
}

long SensorMonitor::get_temperature(){
	float temperature;

	sensors_event_t bmp_event;
	_bmp.getEvent(&bmp_event);

	if (bmp_event.pressure){
		/* Get ambient temperature in Celcius */

		_bmp.getTemperature(&temperature);

		/* Convert atmospheric pressure, SLP and temp to altitude    */

		// Serial.print(F("Alt: "));
		// Serial.print(_bmp.pressureToAltitude(_sea_level_pressure, bmp_event.pressure, temperature));
		// Serial.println(F(" m; "));

		// Serial.print(F("Temp: "));
		// Serial.print(temperature);
		// Serial.println(F(" C."));
	}

	return temperature;
}

long SensorMonitor::_microsecondsToInches(long microseconds) {
  /*
	  According to Parallax's datasheet for the PING))), there are
	  73.746 microseconds per inch (i.e. sound travels at 1130 feet per
	  second).  This gives the distance travelled by the ping, outbound
	  and return, so we divide by 2 to get the distance of the obstacle.
	  See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  */

  return microseconds / 74 / 2;
}

long SensorMonitor::_microsecondsToCentimeters(long microseconds) {
  /*
	  The speed of sound is 340 m/s or 29 microseconds per centimeter.
	  The ping travels out and back, so to find the distance of the
	  object we take half of the distance travelled.
  */

  return microseconds / 29 / 2;
}

long SensorMonitor::_microsecondsToFeet(long microseconds){
	return microseconds / 74 / 2 / 12;
}
