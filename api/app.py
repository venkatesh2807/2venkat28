from flask import Flask, request, jsonify, send_from_directory
import random
import time
import os

app = Flask(__name__)

def divide_and_conquer(arr):
    if len(arr) == 1:
        return arr[0], arr[0]
    if len(arr) == 2:
        return (max(arr), min(arr))
    
    mid = len(arr) // 2
    max1, min1 = divide_and_conquer(arr[:mid])
    max2, min2 = divide_and_conquer(arr[mid:])
    return max(max1, max2), min(min1, min2)

# Serve the frontend HTML file
@app.route('/')
def serve_frontend():
    return send_from_directory(os.getcwd(), './static/index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    sizes = data['sizes']
    results = []
    timeData = {'divideTimes': [], 'standardTimes': []}

    for size in sizes:
        random_numbers = [random.randint(1, 1000) for _ in range(size)]

        # Divide and Conquer
        start = time.time()
        max_dc, min_dc = divide_and_conquer(random_numbers)
        end = time.time()
        divide_time = (end - start) * 1000

        # Standard Method
        start = time.time()
        max_std, min_std = max(random_numbers), min(random_numbers)
        end = time.time()
        standard_time = (end - start) * 1000

        results.append({
            'size': size,
            'max': max_std,
            'min': min_std,
            'divideTime': divide_time,
            'standardTime': standard_time
        })

        timeData['divideTimes'].append(divide_time)
        timeData['standardTimes'].append(standard_time)

    return jsonify({'results': results, 'timeData': timeData})

if __name__ == '__main__':
    app.run(debug=True)
