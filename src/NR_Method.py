#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from Generate_Trace import Generate_trace, Point

from numpy import sin
from numpy import cos
from numpy import pi

class NewtonRaphson():
    def __init__(self):
        self.N_max = 100
        self.Error = 0.1
        self.Min_change = 0.01
        
        self.x_target, self.y_target, self.z_target = (0, 0, 0)
        self.theta1, self.theta2, self.theta3 = (0,0,0)        

        self.errors_x = []
        self.errors_y = []
        self.errors_z = []

        self.theta_start = (np.radians(0), np.radians(-60), np.radians(60))
        self.update_thetaStart(self.theta_start)
        self.prev_solution = (0,0,0)    

        # Leg parameter  -units: [mm]    
        l1 = 75.5
        h1 = 32.5
        l2 = 92.35
        h2 = 30.15
        l3 = 190
        self.equation_x = lambda theta1, theta2, theta3: ( l1*cos(theta1) - l2*sin(theta1)*cos(theta2) + l3*sin(theta1)*sin(theta2)*sin(theta3) - l3*sin(theta1)*cos(theta2)*cos(theta3)  )
        self.equation_y = lambda theta1, theta2, theta3: ( l1*sin(theta1) + l2*cos(theta1)*cos(theta2) - l3*sin(theta2)*sin(theta3)*cos(theta1) + l3*cos(theta1)*cos(theta2)*cos(theta3)  )
        self.equation_z = lambda theta1, theta2, theta3: ( l2*sin(theta2) + l3*sin(theta2)*cos(theta3) + l3*sin(theta3)*cos(theta2) )


    def main_process(self, trace):
        theta_trace = []
        for xyz_target in trace:
            self.update_target(xyz_target)
            theta = self.NR_calculate()
            theta_trace.append(theta)
            # self.update_thetaStart(self.theta_start)
        return theta_trace

    def update_target(self, xyz_target):
        self.x_target, self.y_target, self.z_target = xyz_target

    def update_thetaStart(self, theta_start):
        if theta_start is None:
            return
        self.theta1, self.theta2, self.theta3 = theta_start
    
    def countXYZ_fromTheta(self, theta):
        th1, th2, th3 = theta
        th1 = th1 - 90
        th2 = th2 - 150 
        th3 = 180 - th3
        th1_rad = np.radians(th1)
        th2_rad = np.radians(th2)
        th3_rad = np.radians(th3)
        x = self.equation_x(th1_rad, th2_rad, th3_rad)
        y = self.equation_y(th1_rad, th2_rad, th3_rad)
        z = self.equation_z(th1_rad, th2_rad, th3_rad)
        return (x,y,z)
    
    def countTheta_forPoint(self, xyz_target):
        self.update_thetaStart(self.theta_start)
        self.update_target(xyz_target)
        return self.NR_calculate()



    '''   ======   ALGORITHM MATH FUNCTION   ======   '''
    def calculate_error(self, theta):
        error_x = self.x_target - self.equation_x(theta[0], theta[1], theta[2])
        error_y = self.y_target - self.equation_y(theta[0], theta[1], theta[2])
        error_z = self.z_target - self.equation_z(theta[0], theta[1], theta[2])
        self.errors_x.append(error_x)
        self.errors_y.append(error_y)
        self.errors_z.append(error_z)
        return (error_x, error_y, error_z)

    def Jacobian_matrix(self, theta1, theta2, theta3):
        epsilon = 1e-6  # Przyrost
        dx_dtheta1 = (self.equation_x(theta1 + epsilon, theta2, theta3) - self.equation_x(theta1, theta2, theta3)) / epsilon
        dx_dtheta2 = (self.equation_x(theta1, theta2 + epsilon, theta3) - self.equation_x(theta1, theta2, theta3)) / epsilon
        dx_dtheta3 = (self.equation_x(theta1, theta2, theta3 + epsilon) - self.equation_x(theta1, theta2, theta3)) / epsilon
        dy_dtheta1 = (self.equation_y(theta1 + epsilon, theta2, theta3) - self.equation_y(theta1, theta2, theta3)) / epsilon
        dy_dtheta2 = (self.equation_y(theta1, theta2 + epsilon, theta3) - self.equation_y(theta1, theta2, theta3)) / epsilon
        dy_dtheta3 = (self.equation_y(theta1, theta2, theta3 + epsilon) - self.equation_y(theta1, theta2, theta3)) / epsilon
        dz_dtheta1 = (self.equation_z(theta1 + epsilon, theta2, theta3) - self.equation_z(theta1, theta2, theta3)) / epsilon
        dz_dtheta2 = (self.equation_z(theta1, theta2 + epsilon, theta3) - self.equation_z(theta1, theta2, theta3)) / epsilon
        dz_dtheta3 = (self.equation_z(theta1, theta2, theta3 + epsilon) - self.equation_z(theta1, theta2, theta3)) / epsilon
        J = np.array([
            [dx_dtheta1, dx_dtheta2, dx_dtheta3],
            [dy_dtheta1, dy_dtheta2, dy_dtheta3],
            [dz_dtheta1, dz_dtheta2, dz_dtheta3]
        ])
        return J
    
    def NR_calculate(self):
        iteration = 0
        while(iteration <= self.N_max-1):
            iteration += 1
            _Xn = np.array([[self.theta1], 
                            [self.theta2], 
                            [self.theta3]])
            _Fn = np.array([[self.equation_x(self.theta1, self.theta2, self.theta3) - self.x_target], 
                            [self.equation_y(self.theta1, self.theta2, self.theta3) - self.y_target], 
                            [self.equation_z(self.theta1, self.theta2, self.theta3) - self.z_target]])
            J = self.Jacobian_matrix(self.theta1, self.theta2, self.theta3).astype('float64')
            J_inverse = np.linalg.inv(J)

            result = _Xn - (J_inverse @ _Fn)
            
            
            self.theta1 = result[0][0]
            self.theta2 = result[1][0]
            self.theta3 = result[2][0]

            # self.theta1 = result[0][0]% np.pi
            # self.theta2 = result[1][0]% np.pi
            # self.theta3 = result[2][0]% np.pi

            # self.theta1 = np.clip(result[0][0], np.radians(-90), np.radians(90))
            # self.theta2 = np.clip(result[1][0], np.radians(-150), np.radians(30))
            # self.theta3 = np.clip(result[2][0], np.radians(0), np.radians(180))

            theta = (self.theta1, self.theta2, self.theta3)

            error = self.calculate_error(theta)

            if all(abs(err) < self.Error for err in error):
                break

        return self.Convert_forServo()

    def Convert_forServo(self):

        # return (self.theta1, self.theta2, self.theta3)

        th1, th2, th3 = self.convertTh_servo()
        
        if not (0 <= th1 <= 180 and 0 <= th2 <= 180 and 0 <= th3 <= 180):
            return self.optimizesolver_NR()
        
        result = (round(th1, 1), round(th2, 1), round(th3, 1))
        return result
    
    def convertTh_servo(self):
        th1 = np.degrees(self.theta1) + 90
        th2 = np.degrees(self.theta2) + 150
        th3 = 180 - np.abs(np.degrees(self.theta3))
        return (th1, th2, th3)

    def optimizesolver_NR(self):
        from scipy.optimize import fsolve

        def equations(theta):
            return [
                self.equation_x(theta[0], theta[1], theta[2]) - self.x_target,
                self.equation_y(theta[0], theta[1], theta[2]) - self.y_target,
                self.equation_z(theta[0], theta[1], theta[2]) - self.z_target
            ]

        theta_solution = fsolve(equations, self.theta_start)
        self.theta1, self.theta2, self.theta3 = theta_solution
        th1, th2, th3 = self.convertTh_servo()
        if not (0 <= th1 <= 180 and 0 <= th2 <= 180 and 0 <= th3 <= 180):
            return self.prev_solution
        
        self.prev_solution = (round(th1, 1), round(th2, 1), round(th3, 1))
        return (round(th1, 1), round(th2, 1), round(th3, 1))


def main():   
    P_1 = Point(80, 240, -50) 
    P_2 = Point(80, 180, 0) 

    T1 = Generate_trace(P_1, P_2)

    nr_method = NewtonRaphson()
    theta_T1 = nr_method.main_process(T1.trace)
    print(theta_T1)



if __name__ == '__main__':
    main()