#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Response


app = Flask(__name__)



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




def init():
  app.run(host='0.0.0.0', port=3000, debug=True)

if __name__ == '__main__':        
  init()