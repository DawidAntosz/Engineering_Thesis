#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
from mpu6050.mpu6050 import mpu6050
import math
from time import sleep

from RobotMovement import RobotMovement
from _getch_unix import _Getch

def run_mpu6050_mainProcess(mpu, Robot):
  while True:
    accel_data_sample = mpu.get_accel_data()
    axis_y = accel_data_sample['y']
    axis_z = accel_data_sample['z']
    angle_x =  math.degrees(math.atan2(-axis_y, -axis_z))
    
    hysteresis_range = (-12, 12)
    if angle_x < hysteresis_range[0] or angle_x > hysteresis_range[1]:
      Robot.update_trace(angle_x)
    
    sleep(0.5)

def main():
  try:
    getch = _Getch()
    Robot = RobotMovement()

    mpu = mpu6050(0x68)
    mpu_thread = threading.Thread(target=run_mpu6050_mainProcess, args=(mpu, Robot), daemon=True)
    mpu_thread.start()

    text_menu = "=======================\n\
      Select function:\n\
          'w' - Go Forward\n\
          's' - Go Backward\n\
          'a' - Go Left\n\
          'd' - Go Right\n\
          'y' - Stand up\n\
          'h' - Sit down\n\n\n\
              'z' - Quick \n"  
    print(text_menu)

    x = getch()

    while x != 'z':
      if Robot.ready_flag and Robot.Robot_isStanding:
        if x == 'w':
          Robot.GoForward()
        if x == 's':
          Robot.GoBackward()
        if x == 'a':
          Robot.GoLeft()
        if x == 'd':
          Robot.GoRight()
        if x == 'h':
          Robot.Defoult_TraceSet()
          Robot.Turn_off()
      else:
        if x == 'y':
          Robot.GoStartPosition()
        if x == 'h':
          Robot.Turn_off()
        if x == 'p':
          Robot.Robot_isStanding == True
        else:
          print("The robot is not ready")

      x = getch()

    if Robot.Robot_isStanding:
      Robot.Turn_off()
    mpu_thread.join()

  except Exception as e:
      print(f"Error: {e}")
  finally:
      mpu_thread.join()









if __name__ == '__main__':
  main()