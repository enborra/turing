#ifndef MotorController_h
#define MotorController_h




	class MotorController {
		protected:
			const static uint8_t MOTOR_DIRECTION_NONE;
			const static uint8_t MOTOR_DIRECTION_FORWARD;
			const static uint8_t MOTOR_DIRECTION_BACKWARD;

			static void _driveLeftWheel(boolean direction);
			static void _driveRightWheel(boolean direction);

		public:
			MotorController();

			static void init();
			static void update();
			static void move(boolean direction);
			static void stop();

			static void turnLeft();
			static void turnRight();
			static void pivotLeft();
			static void pivotRight();
	};

#endif
