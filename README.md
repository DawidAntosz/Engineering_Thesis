# **Control system for a four-legged walking robot**

### Description: 
  The present diploma thesis describes the implementation of a four-legged walking robot
control system. The scope of the work includes the realization of the mechanical
construction, the execution of electrical connections, as well as the development of control
software that supervises the robot's movements. A Banana Pi mini-computer was used as
the central unit. Servomechanisms were employed to control the movement of the legs at the
hip and knee joints. Wireless technology in the ISM band, utilizing the nRF24L01 module, was
used for remote control of the robot. One of the design challenges was to design a power
supply system that had to provide sufficient power due to the significant number of motors.
Regarding the solution to the inverse kinematics problem in determining the position of one
leg of the robot in Cartesian coordinates, the Newton-Raphson method was applied, utilizing
equations obtained from Denavit-Hartenberg notation. The robot's locomotion control
algorithm is based on enforcing trajectories of successive robot legs, stored in the form of an
array containing a specified number of points in Cartesian coordinate system, which are then
converted into servo drive settings. During motion, the content of the array is modified based
on data obtained from a MEMS sensor. The end result is the correct functioning of the
implemented walking robot, which means its ability to move to achieve a specified position,
as well as continuous remote communication with the robot to change its position and
control algorithm parameters.

# **Movie: [youtu.be/dEax441fGrM](https://youtu.be/dEax441fGrM)**

<p align="center">
  <img src="https://github.com/DawidAntosz/Engineering_Thesis/assets/64035334/f6a7cb09-c753-4d9c-98a2-0d1e41522f38" />
</p>

<p align="center">
  <img src="https://github.com/DawidAntosz/Engineering_Thesis/assets/64035334/70e9648c-989d-4ad9-84d6-992535753293" />
</p>

![Robot](https://github.com/DawidAntosz/Engineering_Thesis/assets/64035334/6e0ff65d-6f60-419e-a3c6-b79172660ee6)

