from flask import Flask, request, Response, jsonify
import os
from Crypto.Hash import SHA3_256
import json

app = Flask(__name__)

key = os.environ['KEY']

if not os.path.exists("data"):
    os.makedirs("data")

@app.route('/')
def hello():
    return 'Grades API'

@app.route('/retrieve', methods=['POST'])
def retrieve():
    if not request.form['api_key']:
        return Response("Bad request", status=400)
    request_key = request.form['api_key']
    hashed_key = SHA3_256.new(data=request_key.encode("utf-8"))
    if hashed_key.hexdigest() == key:
        try:
            with open("data/grades.json", 'r') as file:
                grades_data = json.load(file)
            return jsonify(grades_data), 200
        except FileNotFoundError:
            return jsonify({'error': 'File not found'}), 404
        except json.JSONDecodeError:
            return jsonify({'error': 'Error decoding JSON'}), 500
    return Response("Invalid API key", status=401)


@app.route('/update', methods=['POST'])
def update():
    if 'file' not in request.files or not request.form['api_key']:
        return Response("Bad request", status=400)
    request_key = request.form['api_key']
    hashed_key = SHA3_256.new(data=request_key.encode("utf-8"))
    file = request.files['file']
    if hashed_key.hexdigest() == key:
        if file.filename == 'grades.json':
            file.save(os.path.join("data", file.filename))
            return Response("File saved successfully", status=200)
        return Response("Bad request", status=400)
    return Response("Invalid API key", status=401)


if __name__ == '__main__':
    app.run()