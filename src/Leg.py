#!/usr/bin/python
# -*- coding: utf-8 -*-
from ServoController import ServoController
from typing import List
from NR_Method import NewtonRaphson
from Generate_Trace import Generate_trace
import numpy as np
from time import sleep
from copy import deepcopy

class Leg:
  def __init__(self, port: List[int], controller: ServoController, side: str):
    self.controller = controller
    self.SerwoPort1 = port[0]
    self.SerwoPort2 = port[1]
    self.SerwoPort3 = port[2]
    self.side = side
    self.prev_angle1 = 0
    self.prev_angle2 = 0
    self.prev_angle3 = 0
    self.corrected_angle = 0
    self.nr_method = NewtonRaphson()
    ''' ======= START points ======= '''
    self.P1_start = [75, 119.25, -40]
    self.P1 = [75, 150, -40]
    ''' ============================ '''
    ''' === Forward trace points === '''
    self.P2 = [75, 120, -20]
    self.P3 = [60, 120, 0]
    self.P4 = [60, 140, 10]
    self.P5 = [60, 140, -70]
    self.P6 = [60, 120, -60]
    self.P7 = [60, 120, -50]
    self.Points = [self.P1, self.P2, self.P3, self.P4, self.P5, self.P6, self.P7]
    self.StartTrace = []
    self.theta_T1 = []
    self.theta_T2 = []
    self.theta_T3 = []
    self.theta_T4 = []
    self.theta_T5 = []
    self.theta_T6 = []
    ''' ============================ '''
    self.generate_StartTrace()
    self.Init_TracePoint()

  def Restoring_Basic_Waypoints(self):
    self.Points = [self.P1, self.P2, self.P3, self.P4, self.P5,self.P6, self.P7]

  def default_trace(self):
    self.Points = [self.P1, self.P2, self.P3, self.P4, self.P5,self.P6, self.P7]
    self.updateTrace()
    theta_p1 = (self.theta_T1[0][0], self.theta_T1[0][1], self.theta_T1[0][2])
    self.SetLeg(theta_p1)

  def update_PointTrace(self, x_end):
    x_end = 2* x_end
    points_copy = deepcopy(self.Points)
  
    if self.side == 'R':
      for point in points_copy:
        point[1] += x_end

    if self.side == 'L':
      for point in points_copy:
        point[1] -= x_end
  
    self.Points = points_copy
    self.updateTrace()

    theta_p1 = (self.theta_T1[0][0], self.theta_T1[0][1], self.theta_T1[0][2])
    self.SetLeg(theta_p1)
    self.Restoring_Basic_Waypoints()


  def updateTrace(self):
    T1 = Generate_trace(self.Points[0], self.Points[1]).trace + Generate_trace(self.Points[1], self.Points[2]).trace + Generate_trace(self.Points[2], self.Points[3]).trace
    T2 = Generate_trace(self.Points[3], self.Points[0]).trace
    T3 = Generate_trace(self.Points[0], self.Points[4]).trace
    T4 = Generate_trace(self.Points[4], self.Points[5]).trace + Generate_trace(self.Points[5], self.Points[6]).trace + Generate_trace(self.Points[6], self.Points[0]).trace
    T5 = Generate_trace(self.Points[3], self.Points[4]).trace
    T6 = Generate_trace(self.Points[4], self.Points[5]).trace + Generate_trace(self.Points[5], self.Points[2]).trace + Generate_trace(self.Points[2], self.Points[3]).trace
    self.theta_T1 = self.nr_method.main_process(T1)
    self.theta_T2 = self.nr_method.main_process(T2)
    self.theta_T3 = self.nr_method.main_process(T3)
    self.theta_T4 = self.nr_method.main_process(T4)
    self.theta_T5 = self.nr_method.main_process(T5)
    self.theta_T6 = self.nr_method.main_process(T6)

  def generate_StartTrace(self):
    start_position = np.array([0, 0, 0])
    target_position = np.array([90, 0, 0])
    step = 20
    for i in range(1, step + 1):
      interpolated_point = start_position + (target_position - start_position) * (i / step)
      rounded_point = [round(value, 1) for value in interpolated_point]
      self.StartTrace.append(rounded_point)
    start_position = target_position
    target_position = np.array([90, 10, 40])
    for i in range(1, step + 1):
      interpolated_point = start_position + (target_position - start_position) * (i / step)
      rounded_point = [round(value, 1) for value in interpolated_point]
      self.StartTrace.append(rounded_point)
    T1_stand = Generate_trace(self.P1_start, self.P1)
    theta_T1Stand = self.nr_method.main_process(T1_stand.trace)
    self.StartTrace += theta_T1Stand

  def Init_TracePoint(self):
    T1 = Generate_trace(self.P1, self.P2).trace + Generate_trace(self.P2, self.P3).trace + Generate_trace(self.P3, self.P4).trace
    T2 = Generate_trace(self.P4, self.P1).trace
    T3 = Generate_trace(self.P1, self.P5).trace
    T4 = Generate_trace(self.P5, self.P6).trace + Generate_trace(self.P6, self.P7).trace + Generate_trace(self.P7, self.P1).trace
    T5 = Generate_trace(self.P4, self.P5).trace
    T6 = Generate_trace(self.P5, self.P6).trace + Generate_trace(self.P6, self.P3).trace + Generate_trace(self.P3, self.P4).trace
    self.theta_T1 = self.nr_method.main_process(T1)
    self.theta_T2 = self.nr_method.main_process(T2)
    self.theta_T3 = self.nr_method.main_process(T3)
    self.theta_T4 = self.nr_method.main_process(T4)
    self.theta_T5 = self.nr_method.main_process(T5)
    self.theta_T6 = self.nr_method.main_process(T6)

  def Trace_select(self, thetaTrace_num: int, iterator:int, reversTab: bool):
    thetaTrace = None
    if thetaTrace_num == 0:
      thetaTrace = self.StartTrace
    elif thetaTrace_num == 1:
      thetaTrace = self.theta_T1
    elif thetaTrace_num == 2:
      thetaTrace = self.theta_T2
    elif thetaTrace_num == 3:
      thetaTrace = self.theta_T3
    elif thetaTrace_num == 4:
      thetaTrace = self.theta_T4
    elif thetaTrace_num == 5:
      thetaTrace = self.theta_T5
    elif thetaTrace_num == 6:
      thetaTrace = self.theta_T6
    else:
      print("Invalid thetaTrace_num value")
      return None    
    if reversTab:
      self.SetLeg(thetaTrace[::-1][iterator])
    else:
      self.SetLeg(thetaTrace[iterator])

  def SetLeg(self, value):
    angle1 = value[0]
    angle2 = value[1]
    angle3 = value[2]
    if angle1 < 60 and angle2 < 45:
      angle2 = 45
    if angle1 > 125 and (45 <angle2< 90):
      angle2 = 30 if abs(angle2 - 45) < abs(angle2 - 90) else 85
    if self.side == 'R':
      angle1 = 180 - angle1
      angle2 = 180 - angle2
      angle3 = angle3
    if self.side == 'L':
      angle1 = angle1
      angle2 = angle2
      angle3 = 180 - angle3
    # print(angle1,angle2,angle3)
    self.controller.set_angle(self.SerwoPort1, angle1)
    self.controller.set_angle(self.SerwoPort2, angle2)
    self.controller.set_angle(self.SerwoPort3, angle3)
    self.prev_angle1 = angle1
    self.prev_angle2 = angle2
    self.prev_angle3 = angle3







def main():
  controller = ServoController()
  leg1 = Leg([2,1,0], controller, 'L')
  leg2 = Leg([3,4,5], controller, 'R')
  leg3 = Leg([8,7,6], controller, 'L')
  leg4 = Leg([9,10,11], controller, 'R')
  leg2.SetLeg([180,90,0])


if __name__ == '__main__':
  main()