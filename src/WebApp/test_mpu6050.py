#!/usr/bin/python
# -*- coding: utf-8 -*-
from mpu6050.mpu6050 import mpu6050

accel_data = {'x': [], 'y': [], 'z': []}
gyro_data = {'x': [], 'y': [], 'z': []}

work = True

def main():
  mpu = mpu6050(0x68)
  num_samples = 100
  while work:
    for _ in range(num_samples):
      accel_data_sample = mpu.get_accel_data()
      gyro_data_sample = mpu.get_gyro_data()
      accel_data['x'].append(accel_data_sample['x'])
      accel_data['y'].append(accel_data_sample['y'])
      accel_data['z'].append(accel_data_sample['z'])
      gyro_data['x'].append(gyro_data_sample['x'])
      gyro_data['y'].append(gyro_data_sample['y'])
      gyro_data['z'].append(gyro_data_sample['z'])


if __name__ == '__main__':
  main()