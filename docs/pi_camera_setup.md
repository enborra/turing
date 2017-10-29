





Documentation at https://www.raspberrypi.org/documentation/usage/camera/python/README.md


1. Run sudo raspi-config and choose in the menu to enable the pi camera, then reboot

2. Install camera libs
    - sudo apt-get update
    - For python2.x: sudo apt-get install python-picamera
    - For python3.x: sudo apt-get install python3-picamera


## Sample app:

import picamera

camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

## Various camera settings and their defaults

camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

camera.capture('image.jpg')
