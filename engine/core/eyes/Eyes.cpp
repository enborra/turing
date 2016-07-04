#include <Arduino.h>
#include "Eyes.h"


/*
--------------------------------------------------------
PUBLIC FUNCTIONS
--------------------------------------------------------
*/


Eyes::Eyes(){
	/* Do nothing */
}

void Eyes::init(){
	_pin_pixel = 3;
	_pixels = Adafruit_NeoPixel(7, _pin_pixel, NEO_GRB + NEO_KHZ800);
	_pixels.begin();
	_pixels.show();
}

void Eyes::update(long brightness){
	_pixels.setPixelColor(0, brightness, brightness, brightness);
	_pixels.setPixelColor(1, brightness, brightness, brightness);
	_pixels.setPixelColor(2, brightness, brightness, brightness);
	_pixels.setPixelColor(3, brightness, brightness, brightness);
	_pixels.setPixelColor(4, brightness, brightness, brightness);
	_pixels.setPixelColor(5, brightness, brightness, brightness);
	_pixels.setPixelColor(6, brightness, brightness, brightness);

	_pixels.show();
}