#!/usr/bin/python3
# -*- coding: utf-8 -*-
from mpu6050.mpu6050 import mpu6050
def init():
    mpu = mpu6050(0x68) 
    return mpu

if __name__ == '__main__':
    mpu = init()