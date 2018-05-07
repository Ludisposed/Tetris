#!/usr/bin/python3

from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return send_from_directory('', "tetris.html")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == "__main__":
    app.run()

