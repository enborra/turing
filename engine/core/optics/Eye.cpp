/* Third party includes */

#include <Arduino.h>

/* Class includes */

#include "Eye.h"


/*
--------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------
*/


int Eye::_pin_pixel;
Adafruit_NeoPixel Eye::_pixels;


Eye::Eye(){
	/* Do nothing */
}

void Eye::init(){
	_pin_pixel = 3;
	_pixels = Adafruit_NeoPixel(7, _pin_pixel, NEO_GRB + NEO_KHZ800);
	_pixels.begin();
	_pixels.show();
}

void Eye::update(long brightness){
	_pixels.setPixelColor(0, brightness, brightness, brightness);
	_pixels.setPixelColor(1, brightness, brightness, brightness);
	_pixels.setPixelColor(2, brightness, brightness, brightness);
	_pixels.setPixelColor(3, brightness, brightness, brightness);
	_pixels.setPixelColor(4, brightness, brightness, brightness);
	_pixels.setPixelColor(5, brightness, brightness, brightness);
	_pixels.setPixelColor(6, brightness, brightness, brightness);

	_pixels.show();
}
