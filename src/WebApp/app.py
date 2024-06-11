#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Response

import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

from mpu6050.mpu6050 import mpu6050
import threading
import time
accel_data = {'x': [], 'y': [], 'z': []}
gyro_data = {'x': [], 'y': [], 'z': []}
mpu = mpu6050(0x68)
data_lock = threading.Lock()

def get_sensor_data():
    global accel_data, gyro_data
    MAX_MEASUREMENTS = 100
    while True:
        accel_data_sample = mpu.get_accel_data()
        gyro_data_sample = mpu.get_gyro_data()

        if len(accel_data['x']) >= MAX_MEASUREMENTS:
            accel_data['x'].pop(0)
            accel_data['y'].pop(0)
            accel_data['z'].pop(0)
            gyro_data['x'].pop(0)
            gyro_data['y'].pop(0)
            gyro_data['z'].pop(0)
        
        with data_lock:
            accel_data['x'].append(accel_data_sample['x'])
            accel_data['y'].append(accel_data_sample['y'])
            accel_data['z'].append(accel_data_sample['z'])
            gyro_data['x'].append(gyro_data_sample['x'])
            gyro_data['y'].append(gyro_data_sample['y'])
            gyro_data['z'].append(gyro_data_sample['z'])
        

data_thread = threading.Thread(target=get_sensor_data)
data_thread.daemon = True
data_thread.start()

app = Flask(__name__)
fig, (axis_accel, axis_gyro) = plt.subplots(1, 2, figsize=(12, 7), subplot_kw={'projection': '3d'})


@app.route('/')
def index():
    return render_template('index.html')    


@app.route('/perform_action', methods=['POST'])
def perform_action():
    try:
        data = request.get_json()
        action = data.get('action')
        iteration_count = data.get('iterationCount')

        print(action)

        response_data = {'status': 'success', 'message': 'Action performed successfully'}
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/update_slider', methods=['POST'])
def update_slider():
    try:
        data = request.get_json()
        slider_value = data.get('sliderValue')

        print(f"Received slider value: {slider_value}")

        response_data = {'status': 'success', 'message': 'Slider value updated successfully'}
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# def create_figure():
#     fig = Figure(figsize=(12, 7))
#     axis_accel = fig.add_subplot(1, 2, 1, projection='3d')
#     # axis_accel.plot(range(len(accel_data['x'])), accel_data['x'])
#     axis_accel.scatter(range(len(accel_data['x'])), accel_data['x'], accel_data['y'], c='r', marker='o', label='X')
#     axis_accel.scatter(range(len(accel_data['x'])), accel_data['x'], accel_data['z'], c='g', marker='o', label='Y')
#     axis_accel.scatter(range(len(accel_data['x'])), accel_data['y'], accel_data['z'], c='b', marker='o', label='Z')
#     axis_accel.set_title('Accelerometer Data')
#     axis_accel.set_xlabel('Sample')
#     axis_accel.set_ylabel('Acceleration (X)')

#     axis_gyro = fig.add_subplot(1, 2, 2, projection='3d')
#     # axis_gyro.plot(range(len(gyro_data['x'])), gyro_data['x'])
#     axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['x'], gyro_data['y'], c='r', marker='o', label='X')
#     axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['x'], gyro_data['z'], c='g', marker='o', label='Y')
#     axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['y'], gyro_data['z'], c='b', marker='o', label='Z')
#     axis_gyro.set_title('Gyroscope Data')
#     axis_gyro.set_xlabel('Sample')
#     axis_gyro.set_ylabel('Angular Velocity (X)')
#     return fig


def update(frame):
    with data_lock:
        axis_accel.clear()
        axis_accel.scatter(range(len(accel_data['x'])), accel_data['x'], accel_data['y'], c='r', marker='o', label='X')
        axis_accel.scatter(range(len(accel_data['x'])), accel_data['x'], accel_data['z'], c='g', marker='o', label='Y')
        axis_accel.scatter(range(len(accel_data['x'])), accel_data['y'], accel_data['z'], c='b', marker='o', label='Z')
        axis_accel.set_title(f'Accelerometer Data - Frame {frame}')
        axis_accel.set_xlabel('Sample')
        axis_accel.set_ylabel('Acceleration (X)')
        axis_accel.legend()

        axis_gyro.clear()
        axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['x'], gyro_data['y'], c='r', marker='o', label='X')
        axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['x'], gyro_data['z'], c='g', marker='o', label='Y')
        axis_gyro.scatter(range(len(gyro_data['x'])), gyro_data['y'], gyro_data['z'], c='b', marker='o', label='Z')
        axis_gyro.set_title(f'Gyroscope Data - Frame {frame}')
        axis_gyro.set_xlabel('Sample')
        axis_gyro.set_ylabel('Angular Velocity (X)')
        axis_gyro.legend()

@app.route('/plot.png')
def plot_png():
    anim = FuncAnimation(fig, update, frames=None, interval=1000)
    output = io.BytesIO()
    anim.save(output, format='png')
    return Response(output.getvalue(), mimetype='image/png')



if __name__ == '__main__':        
    app.run(host='0.0.0.0', port=3000, debug=True)