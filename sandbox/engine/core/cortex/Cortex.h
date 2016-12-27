#ifndef Cortex_h
#define Cortex_h

    #include <Adafruit_Sensor.h>
    #include <Adafruit_TSL2561_U.h>
    #include "../sensor_monitor/SensorMonitor.h"
    #include "../foreman/Foreman.h"


	class Cortex {
		protected:
            static SensorMonitor _sensor_manager;
            static Adafruit_TSL2561_Unified tsl;
            static Foreman _time;

            static void configureSensor();
            static void displaySensorDetails();
            static void update_half_second();
            static void update_frame();
            static void update_second();


		public:
			Cortex();

			static void init();
			static void update();

	};

#endif
