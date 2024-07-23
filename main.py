from flask import Flask, request, Response
import os
from Crypto.Hash import SHA3_256

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
        return Response("Valid key", status=200)
    return Response("Invalid API key", status=401)


@app.route('/update', methods=['POST'])
def update():
    if 'file' not in request.files:
        return Response("File not found", status=400)
    file = request.files['file']
    if file.filename == 'grades.json':
        file.save(os.path.join("data", file.filename))
        return Response("File saved successfully", status=200)
    return Response("Bad request", status=400)


if __name__ == '__main__':
    app.run()