#ifndef SensorMonitor_h
#define SensorMonitor_h

	#include <Wire.h>
	#include <Adafruit_Sensor.h>
	#include <Adafruit_LSM303_U.h>
	#include <Adafruit_BMP085_U.h>
	#include <Adafruit_L3GD20_U.h>
	#include <Adafruit_10DOF.h>
	#include <Adafruit_TSL2561_U.h>


	class SensorMonitor {
		protected:
			static Adafruit_10DOF _dof;
			static Adafruit_LSM303_Accel_Unified _accel;
			static Adafruit_LSM303_Mag_Unified _mag;
			static Adafruit_BMP085_Unified _bmp;
			static Adafruit_TSL2561_Unified _tsl;

			static float _sea_level_pressure;

			static void _update_acceleration();
			static void _update_compass();
			static void _update_altitude();
			static void _update_lux();
			static void _update_distance();

			static long _microsecondsToInches(long microseconds);
			static long _microsecondsToCentimeters(long microseconds);
			static long _microsecondsToFeet(long microseconds);


		public:
			SensorMonitor();

			static void init();
			static void update();

			static long get_proximity_front();
			static long get_temperature();
	};

#endif
