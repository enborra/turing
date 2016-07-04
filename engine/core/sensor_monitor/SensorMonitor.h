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
			Adafruit_10DOF _dof;
			Adafruit_LSM303_Accel_Unified _accel;
			Adafruit_LSM303_Mag_Unified _mag;
			Adafruit_BMP085_Unified _bmp;
			Adafruit_TSL2561_Unified _tsl;

			float _sea_level_pressure;

			void _update_acceleration();
			void _update_compass();
			void _update_altitude();
			void _update_lux();
			void _update_distance();

			long _microsecondsToInches(long microseconds);
			long _microsecondsToCentimeters(long microseconds);
			long _microsecondsToFeet(long microseconds);


		public:
			SensorMonitor();

			void init();
			void update();

			long get_proximity_front();
			long get_temperature();
	};

#endif