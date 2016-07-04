#ifndef Eyes_h
#define Eyes_h

	#include <Adafruit_NeoPixel.h>


	class Eyes {
		protected:
			int _pin_pixel;

			Adafruit_NeoPixel _pixels;

		public:
			Eyes();

			void init();
			void update(long brightness);
	};

#endif