#ifndef Eye_h
#define Eye_h

	#include <Adafruit_NeoPixel.h>


	class Eye {
		protected:
			static int _pin_pixel;
			static Adafruit_NeoPixel _pixels;

		public:
			Eye();

			static void init();
			static void update(long brightness);
	};

#endif
