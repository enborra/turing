#include <Arduino.h>
#include "Foreman.h"

#include "../timer/Timer.h"



bool 	Foreman::_is_initialized = false;
Timer 	Foreman::_timer;
int		Foreman::_current_callback_count_frame = 0;
int 	Foreman::_current_callback_count_half_second = 0;
int 	Foreman::_current_callback_count_second = 0;
void (* Foreman::_callbacks_frame[10])();
void (* Foreman::_callbacks_half_second[10])();
void (* Foreman::_callbacks_second[10])();


/*
--------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------
*/


void Foreman::init(){
	Serial.println("[FOREMAN] Initializing...");

	_timer.every(1000, second_handler);
	_timer.every(1000/2, half_second_handler);
	_timer.every(1000/30, frame_handler);

	_is_initialized = true;
}


void Foreman::update(){
	_timer.update();
}

void Foreman::frame_handler(){
	for( int i=0; i<10; i++ ){
		if( _callbacks_frame[i] ){
			_callbacks_frame[i]();
		}
	}
}

void Foreman::half_second_handler(){
	for( int i=0; i<10; i++ ){
		if( _callbacks_half_second[i] ){
			_callbacks_half_second[i]();
		}
	}
}

void Foreman::second_handler(){
	for( int i=0; i<10; i++ ){
		if( _callbacks_second[i] ){
			_callbacks_second[i]();
		}
	}
}



void Foreman::subscribe_frame(void(* frame_handler)()){
	Serial.println("[FOREMAN] Subscribing to frame handler.");

	_callbacks_frame[0] = frame_handler;
	_current_callback_count_frame += 1;
}

void Foreman::subscribe_second(void(* second_handler)()){
	Serial.println("[FOREMAN] Subscribing to second handler.");

	_callbacks_second[0] = second_handler;
	_current_callback_count_second += 1;
}

void Foreman::subscribe_half_second(void(* half_second_handler)()){
	Serial.println("[FOREMAN] Subscribing to half second handler.");

	_callbacks_half_second[0] = half_second_handler;
	_current_callback_count_half_second += 1;
}



