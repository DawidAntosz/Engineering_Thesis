#!/usr/bin/python
# -*- coding: utf-8 -*-

from ServoController import ServoController
from Leg import Leg
from time import sleep
import numpy as np


class RobotMovement:
  def __init__(self):
    self.controller = ServoController()

    self.Leg1 = Leg([2,1,0], self.controller, 'L')
    self.Leg2 = Leg([3,4,5], self.controller, 'R')
    self.Leg3 = Leg([8,7,6], self.controller, 'L')
    self.Leg4 = Leg([9,10,11], self.controller, 'R')
    self.Legs_tab = [self.Leg1, self.Leg2, self.Leg3, self.Leg4]
    self.legPair1 = [self.Leg1, self.Leg4]
    self.legPair2 = [self.Leg2, self.Leg3]

    self.length_max = max(len(self.Leg1.theta_T1),len(self.Leg1.theta_T2)) 
    self.step = int(max(len(self.Leg1.theta_T1),len(self.Leg1.theta_T2)) // min(len(self.Leg1.theta_T1),len(self.Leg1.theta_T2))) 

    self.iteration_count = 4
    self.ready_flag = 1
    self.Robot_isStanding = False
    self.Traces = {
      "T_start": 0,
      "T1": 1,
      "T2": 2,
      "T3": 3,
      "T4": 4,
      "T5": 5,
      "T6": 6
    }

  def update_trace(self, angle_x):
    if self.ready_flag == 1:
      d1 = 43.5 # dimension of half body in "X" robot axis
      l1 = 75.5
      X_correct = (d1+l1) - ((d1+l1) * np.cos(np.radians(angle_x)))
      X_correct = int(X_correct)
      if angle_x < 0:
        X_correct = X_correct * (-1)

      for leg in self.Legs_tab:
        leg.update_PointTrace(X_correct)
    else:
      return None

  def Defoult_TraceSet(self):
    for leg in self.Legs_tab:
        leg.default_trace()

  def reset_ready_flag(self):
    self.ready_flag = 1

  def setPairLegs(self, pair:int, thetaTrace_num: int, iterator:int, reversTab: bool):
    if pair == 1:
      self.Leg1.Trace_select(thetaTrace_num, iterator, reversTab)
      self.Leg4.Trace_select(thetaTrace_num, iterator, reversTab)
    elif pair == 2:
      self.Leg2.Trace_select(thetaTrace_num, iterator, reversTab)
      self.Leg3.Trace_select(thetaTrace_num, iterator, reversTab)
    else:
      print("Invalid pair value")
  
  def MoveFun(self, trace_order: list, reversTab: bool):
    if len(trace_order) == 11:
      toggle = True
      for n in range(self.iteration_count):
        short_iter = 0
        for long_iter in range(self.length_max):
          if (long_iter % self.step == 0) and (long_iter != 0):
            short_iter  += 1
          if (n == 0):
            self.setPairLegs(1, trace_order[0], long_iter, reversTab)
            sleep(0.005) # more time need (only one pair leg operate to fast)- jerking 
          elif (n == 1):
            self.setPairLegs(1, trace_order[1], short_iter, reversTab)
            self.setPairLegs(2, trace_order[2], long_iter, reversTab)
          elif (n == self.iteration_count - 1):
            if (self.iteration_count % 2 == 0):
              self.setPairLegs(2, trace_order[3], long_iter, reversTab)
              self.setPairLegs(1, trace_order[4], short_iter, reversTab)
            else:
              self.setPairLegs(2, trace_order[5], short_iter, reversTab)
              self.setPairLegs(1, trace_order[6], long_iter, reversTab)
          else:
            if toggle:
              self.setPairLegs(1, trace_order[7], long_iter, reversTab)
              self.setPairLegs(2, trace_order[8], short_iter, reversTab)
            else:
              self.setPairLegs(1, trace_order[9], short_iter, reversTab)
              self.setPairLegs(2, trace_order[10], long_iter, reversTab)
        toggle = not toggle
    else:
      print("Invalid trace order")

  def GoForward(self):
    self.ready_flag = 0
    order_trace = [1,5,1,4,2,2,4,6,5,5,6]
    self.MoveFun(order_trace, False)
    self.reset_ready_flag()

  def GoBackward(self):
    self.ready_flag = 0
    order_trace = [4,5,4,1,3,3,1,6,5,5,6]
    self.MoveFun(order_trace, True)
    self.reset_ready_flag()

  def setPairLegs_turning(self, pair:int, thetaTrace_num1: int, thetaTrace_num2: int, iterator:int, reversTab1:bool = False, reversTab2:bool = True):
    if pair == 1:
      self.Leg1.Trace_select(thetaTrace_num1, iterator, reversTab1)
      self.Leg4.Trace_select(thetaTrace_num2, iterator, reversTab2)
    elif pair == 2:
      self.Leg2.Trace_select(thetaTrace_num2, iterator, reversTab2)
      self.Leg3.Trace_select(thetaTrace_num1, iterator, reversTab1)
    else:
      print("Invalid pair value")

  def GoRight(self):
    self.ready_flag = 0
    toggle = True
    for n in range(self.iteration_count):
      short_iter = 0
      for long_iter in range(self.length_max):
        if (long_iter % self.step == 0) and (long_iter != 0):
          short_iter += 1
        if (n == 0):
          self.setPairLegs_turning(1, 1, 4, long_iter, False, True)
          sleep(0.005)
        elif (n == 1):
          self.setPairLegs_turning(1, 5, 5, short_iter, False, True)
          self.setPairLegs_turning(2, 1, 4, long_iter, False, True)
        elif (n == self.iteration_count - 1):
          if (self.iteration_count % 2 == 0):
            self.setPairLegs_turning(2, 4, 1, long_iter, False, True)
            self.setPairLegs_turning(1, 2, 3, short_iter, False, True)
          else:
            self.setPairLegs_turning(2, 2, 3, short_iter, False, True)
            self.setPairLegs_turning(1, 4, 1, long_iter, False, True)
        else:
          if toggle:
            self.setPairLegs_turning(1, 6, 6, long_iter, False, True)
            self.setPairLegs_turning(2, 5, 5, short_iter, False, True)
          else:
            self.setPairLegs_turning(1, 5, 5, short_iter, False, True)
            self.setPairLegs_turning(2, 6, 6, long_iter, False, True)
      toggle = not toggle
    self.reset_ready_flag()

  def GoLeft(self):
    self.ready_flag = 0
    toggle = True
    for n in range(self.iteration_count):
      short_iter = 0
      for long_iter in range(self.length_max):
        if (long_iter % self.step == 0) and (long_iter != 0):
          short_iter += 1
        if (n == 0):
          self.setPairLegs_turning(1, 4, 1, long_iter, True, False)
          sleep(0.005)
        elif (n == 1):
          self.setPairLegs_turning(1, 5, 5, short_iter, True, False)
          self.setPairLegs_turning(2, 4, 1, long_iter, True, False)
        elif (n == self.iteration_count - 1):
          if (self.iteration_count % 2 == 0):
            self.setPairLegs_turning(2, 1, 4, long_iter, True, False)
            self.setPairLegs_turning(1, 3, 2, short_iter, True, False)
          else:
            self.setPairLegs_turning(2, 3, 2, short_iter, True, False)
            self.setPairLegs_turning(1, 1, 4, long_iter, True, False)
        else:
          if toggle:
            self.setPairLegs_turning(1, 6, 6, long_iter, True, False)
            self.setPairLegs_turning(2, 5, 5, short_iter, True, False)
          else:
            self.setPairLegs_turning(1, 5, 5, short_iter, True, False)
            self.setPairLegs_turning(2, 6, 6, long_iter, True, False)
      toggle = not toggle
    self.reset_ready_flag()

  def Default_position(self):
    sleep(1)
    self.Leg1.SetLeg([0, 0, 0])
    self.Leg2.SetLeg([0, 0, 0])
    self.Leg3.SetLeg([0, 0, 0])
    self.Leg4.SetLeg([0, 0, 0])
    sleep(1)
  
  def GoStartPosition(self):
    for i in range(len(self.Leg1.StartTrace)):
      for leg in self.Legs_tab:
        leg.Trace_select(self.Traces["T_start"], i, False)
        sleep(0.005)
    self.Robot_isStanding = True

  def Turn_off(self):
    for i in range(len(self.Leg1.StartTrace)):
      for leg in self.Legs_tab:
        leg.Trace_select(self.Traces["T_start"], i, True)
        sleep(0.005)
    self.Robot_isStanding = False

  def Robot_Reset(self):
    self.controller.Controller_reset()

  def ServoTune(self):
    self.controller.set_angle(0,180)
    self.controller.set_angle(1,90)
    self.controller.set_angle(2,0)
    self.controller.set_angle(3,0)
    self.controller.set_angle(4,90)
    self.controller.set_angle(5,180)
    self.controller.set_angle(6,180)
    self.controller.set_angle(7,90)
    self.controller.set_angle(8,0)
    self.controller.set_angle(9,0)
    self.controller.set_angle(10,90)
    self.controller.set_angle(11,180)

  def test(self):          
    from Generate_Trace import Generate_trace, Point
    P_1 = Point(80, 240, -50) 
    P_2 = Point(80, 180, 0) 
    P_3 = Point(80, 100, 150) 
    P_4 = Point(80, 190, 190)
    T1 = Generate_trace(P_1, P_2)
    T2 = Generate_trace(P_2, P_3)
    T3 = Generate_trace(P_3, P_4)
    T4 = Generate_trace(P_4, P_1)
    theta_T1 = self.nr_method.main_process(T1.trace)
    theta_T2 = self.nr_method.main_process(T2.trace)
    theta_T3 = self.nr_method.main_process(T3.trace)
    theta_T4 = self.nr_method.main_process(T4.trace)
    for Theta in [theta_T1, theta_T2, theta_T3, theta_T4]:
      for theta in Theta:
        self.Leg4.SetLeg(theta)
        sleep(0.01)
      sleep(1)



def main():
  Robot = RobotMovement()
  Robot.Default_position()
  Robot.GoStartPosition()
  Robot.GoForward()
  sleep(1)
  Robot.GoLeft()
  sleep(1)
  Robot.GoRight()
  sleep(1)
  Robot.GoBackward()
  sleep(1)
  Robot.Turn_off()

  



if __name__ == '__main__':
  main()