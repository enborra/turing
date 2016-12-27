#ifndef Foreman_h
#define Foreman_h

	#include "../timer/Timer.h"
	

	class Foreman {
		protected:
			static Timer _timer;
			static bool _is_initialized;
			static int _current_callback_count_frame;
			static int _current_callback_count_half_second;
			static int _current_callback_count_second;
			static void (* _callbacks_frame[10])();
			static void (* _callbacks_half_second[10])();
			static void (* _callbacks_second[10])();

		public:
			static void init();
			static void update();
			static void frame_handler();
			static void half_second_handler();
			static void second_handler();
			static void subscribe_frame(void(* frame_handler)());
			static void subscribe_half_second(void(* half_second_handler)());
			static void subscribe_second(void(* second_handler)());
	};

#endif