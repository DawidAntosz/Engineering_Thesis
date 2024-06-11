#!/usr/bin/python
# -*- coding: utf-8 -*-

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo


class ServoController:
  def __init__(self, frequency = 48.48):
    self.pca = PCA9685(busio.I2C(SCL, SDA))
    self.pca.frequency = frequency
    self.servo_motors = [servo.Servo(channel, min_pulse=400, max_pulse=2400) for channel in self.pca.channels]

  def set_angle(self, channel, angle):
    if 0 <= channel < len(self.servo_motors):
      self.servo_motors[channel].angle = angle
    
  def Controller_reset(self):
    self.pca.reset()

  def __del__(self):
    self.pca.reset()
    self.pca.deinit()


if __name__ == '__main__':
    try:  
        controller = ServoController()
        controller.set_angle(3, 0)
        controller.set_angle(4, 90)
        controller.set_angle(5, 180)

    except KeyboardInterrupt:
        controller.stop()







# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2350)
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# servo7 = servo.Servo(pca.channels[7], min_pulse=400, max_pulse=2400)
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2400)

# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of

# range, but the default is to use 180 degrees. You can specify the expected range if you wish:

# servo7 = servo.Servo(pca.channels[7], actuation_range=135)

