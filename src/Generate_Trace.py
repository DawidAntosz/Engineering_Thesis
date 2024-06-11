#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import copy

class Point:
    def __init__(self, x_, y_, z_):
        self.x = x_
        self.y = y_
        self.z = z_
    
    @classmethod
    def from_list(cls, lst):
        if isinstance(lst, list) and len(lst) == 3:
            return cls(lst[0], lst[1], lst[2])
        else:
            raise ValueError("Input list must contain three elements")
        
        
class Generate_trace:
    def __init__(self, P1:Point, P2:Point, step:int = 20):
        
        if isinstance(P1, Point):
            self.P1 = copy.copy(P1)
        elif isinstance(P1, list):
            self.P1 = Point.from_list(P1)
        else:
            raise ValueError("Invalid type for P1")

        if isinstance(P2, Point):
            self.P2 = copy.copy(P2)
        elif isinstance(P2, list):
            self.P2 = Point.from_list(P2)
        else:
            raise ValueError("Invalid type for P2")

        self.trace = []
        self.step = step
        
        self.step_x = 0
        self.step_y = 0
        self.step_z = 0
        
        self.generate_trace()
            
    def step_count(self):
        difrent_x = np.abs(self.P1.x - self.P2.x)
        difrent_y = np.abs(self.P1.y - self.P2.y)
        difrent_z = np.abs(self.P1.z - self.P2.z)
        self.step_x = difrent_x / self.step
        self.step_y = difrent_y / self.step
        self.step_z = difrent_z / self.step
        
    def comparison(self, x1, x2, var:str = 'sss'):
        if var == 'x':
            if (x1 < x2):
                x  = x1 + self.step_x
            if (x1 > x2):
                x  = x1 - self.step_x
            if (x1 == x2):
                x  = x1
            return x
        if var == 'y':
            if (x1 < x2):
                x  = x1 + self.step_y
            if (x1 > x2):
                x  = x1 - self.step_y
            if (x1 == x2):
                x  = x1
            return x
        if var == 'z':
            if (x1 < x2):
                x  = x1 + self.step_z
            if (x1 > x2):
                x  = x1 - self.step_z
            if (x1 == x2):
                x  = x1
            return x
        else:
            print('error in comparison fun - generator')
        
    def generate_trace(self):
        
        self.step_count()
        
        self.trace.append([self.P1.x, self.P1.y, self.P1.z])
        
        iteration = 0
        while (iteration < self.step):
            iteration += 1 
            
            x = self.comparison(self.P1.x, self.P2.x, 'x')
            y = self.comparison(self.P1.y, self.P2.y, 'y')
            z = self.comparison(self.P1.z, self.P2.z, 'z')
                      
            x = round(x, 2)
            y = round(y, 2)
            z = round(z, 2)
                
            self.P1.x = x
            self.P1.y = y
            self.P1.z = z
            
            self.trace.append([x,y,z])
            
        return self.trace